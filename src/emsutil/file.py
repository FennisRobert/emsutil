from __future__ import annotations
import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, isspmatrix
from numbers import Number
import msgpack
import msgpack_numpy as m

m.patch()


class Saveable:
    save_fields: list[str] = None
    skip_fields: list[str] = None
    _registry = dict()
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls
        
    @classmethod
    def is_saveable(cls, obj) -> bool:
        if not isinstance(obj, dict):
            return False
        if '__SAVEABLE__' in obj:
            return True
    
    def pack(self) -> dict:
        if self.skip_fields is None:
            skip = []
        else:
            skip = self.skip_fields
            
        if self.save_fields is None:
            data = dict()
            data['__CLASS__'] = self.__class__.__name__
            data['__SAVEABLE__'] = True
            data['__FIELDS__'] = {key: value for key, value in self.__dict__.items()
                                  if '__' not in key and key not in skip}
            return data
        else:
            data = dict()
            data['__CLASS__'] = self.__class__.__name__
            data['__SAVEABLE__'] = True
            data['__FIELDS__'] = {key: value for key, value in self.__dict__.items() if key in self.save_fields and key not in skip}
            return data
    
    @staticmethod
    def unpack(data: dict, collection: dict, _memo: dict | None = None, _obj_id: int | None = None) -> Saveable:
        cls = Saveable._registry[data['__CLASS__']]
        fields = data['__FIELDS__']
        obj = cls.__new__(cls)
        if _memo is not None and _obj_id is not None:
            # Registered before its fields are unpacked, so a reference back to this object resolves to it
            _memo[_obj_id] = obj
        for field, value in fields.items():
            setattr(obj, field, _unpack_data(value, collection, _memo))
        return obj
    
def _is_set(data) -> bool:
    if not isinstance(data, dict):
        return False
    if '__ISSET__' in data:
        return True
    
def _pack_set(data) -> dict:
    return {
        '__ISSET__': True,
        '__DATA__': list(data)
    }

def _is_type(data) -> bool:
    if not isinstance(data, dict):
        return False
    if '__CLASS_TYPE__' in data:
        return True

def _pack_type(data) -> dict:
    return {
        '__CLASS_TYPE__': True,
        '__CLASS_NAME__': f"{data.__module__}.{data.__qualname__}"
    }

def _is_saved(data) -> bool:
    if not isinstance(data, dict):
        return False
    if '__SAVED_OBJ__' in data:
        return True

def _pack_saved(data) -> dict:
    return {
        '__SAVED_OBJ__': True,
        '__OBJ_ID__': id(data)
    }

def _unpack_saved(data: dict) -> int:
    return data['__OBJ_ID__']

def _unpack_type(data: dict):
    class_name = data['__CLASS_NAME__']
    module_name, _, cls_name = class_name.rpartition('.')
    module = __import__(module_name, fromlist=[cls_name])
    cls = getattr(module, cls_name)
    return cls

def _unpack_set(data: dict) -> set:
    return set(data['__DATA__'])

def _pack_object(obj, _obj_collector: dict = None) -> dict:
    try:
        if obj is None:
            return obj
        if isinstance(obj, (str, Number, np.ndarray, bool)):
            return obj
        elif isinstance(obj, set):
            return _pack_set(obj)
        elif isspmatrix(obj):
            return obj
        elif isinstance(obj, list):
            return [_pack_object(item, _obj_collector) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(_pack_object(item, _obj_collector) for item in obj)
        elif isinstance(obj, dict):
            return {key: _pack_object(value, _obj_collector) for key, value in obj.items()}
        elif isinstance(obj, Saveable):
            if id(obj) in _obj_collector:
                return _obj_collector[id(obj)]['reference']
            data = _pack_saved(obj)
            # Registered before its fields are packed, so a reference back to this object (a cycle) stops here
            entry = _obj_collector[data['__OBJ_ID__']] = {'reference': data}
            entry['object'] = _pack_object(obj.pack(), _obj_collector)
            return data
        elif isinstance(obj, type):
            return _pack_type(obj)
        else:
            print(f'Trying to unpack {obj} of type {type(obj)}')
            raise TypeError(f"Cannot pack object of type {type(obj)}")
    except TypeError as e:
        print(f'Error during packing of a property of {obj} of type {type(obj)}')
        raise e
_SCALARS = (str, int, float, complex, bool, bytes, np.generic)


def _unpack_data(data, _obj_collection, _memo: dict | None = None):
    """Rebuilds packed data. _memo maps the id of every saved object to its rebuilt object, so an object that is
    referenced several times (e.g. the mesh of every field solution) is rebuilt once and stays shared, as it was
    when it was saved."""
    if _memo is None:
        _memo = {}
    # The most common types first: scalars and plain containers make up nearly all of the data
    if data is None or isinstance(data, _SCALARS):
        return data
    if isinstance(data, np.ndarray):
        return data.copy()
    if isinstance(data, tuple):
        return tuple(_unpack_data(item, _obj_collection, _memo) for item in data)
    if isinstance(data, list):
        return [_unpack_data(item, _obj_collection, _memo) for item in data]
    if isinstance(data, dict):
        if '__SAVED_OBJ__' in data:
            obj_id = _unpack_saved(data)
            if obj_id not in _memo:
                saved_data = _obj_collection[obj_id]['object']
                if Saveable.is_saveable(saved_data):
                    # Saveable.unpack puts the object in _memo itself, before unpacking its fields
                    Saveable.unpack(saved_data, _obj_collection, _memo, obj_id)
                else:
                    _memo[obj_id] = _unpack_data(saved_data, _obj_collection, _memo)
            return _memo[obj_id]
        if '__SAVEABLE__' in data:
            return Saveable.unpack(data, _obj_collection, _memo)
        if '__CLASS_TYPE__' in data:
            return _unpack_type(data)
        if '__ISSET__' in data:
            return _unpack_set(data)
        return {key: _unpack_data(value, _obj_collection, _memo) for key, value in data.items()}
    if isinstance(data, Number) or isspmatrix(data):
        return data
    raise TypeError(f"Cannot unpack data of type {type(data)}")

def save_object(filename: str, data: dict):
    """Saves a class to a file using msgpack serialization.

    Args:
        filename (str): The filename for the final object
        data (dict): The data to store
    """
    obj_collector = dict()
    dataset = _pack_object(data, obj_collector)
    save_dict = {
        'data': dataset,
        'objects':  obj_collector
    }
    
    with open(filename, 'wb') as f:
        f.write(msgpack.packb(save_dict, use_bin_type=True))

def load_object(filename: str) -> dict:
    """Loads a class from a file using msgpack serialization.

    Args:
        filename (str): The filename of the dataset to load

    Returns:
        dict: The dict() object with the loaded data.
    """
    with open(filename, 'rb') as f:
        loaded = msgpack.unpackb(f.read(), raw=False, strict_map_key=False, use_list=False)
    
    data = loaded['data']
    obj_collection = loaded['objects']
    return _unpack_data(data, obj_collection)

