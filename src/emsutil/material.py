# EMergeCommon is an open source Python EM simulation toolbox.
# Copyright (C) 2025  Robert Fennis.

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, see
# <https://www.gnu.org/licenses/>.

from __future__ import annotations
import numpy as np
from typing import Callable
import inspect
from .file import Saveable

C0 = 299792458


def num_args(func):
    sig = inspect.signature(func)
    return sum(
        1
        for p in sig.parameters.values()
        if p.default is inspect._empty and p.kind in (
            p.POSITIONAL_ONLY,
            p.POSITIONAL_OR_KEYWORD,
            p.KEYWORD_ONLY
        )
    )
    
def _to_mat(value: float | complex | int | np.ndarray) -> np.ndarray:
    if np.isscalar(value):
        return np.eye(3)*value
    if value.shape in ((3,), (3,1), (1,3)):
        return np.diag(np.ravel(value))
    if value.shape == (3,3):
        return value
    else:
        return ValueError(f'Trying to parse {value} as a material property tensor but it cant be identified as scalar, vector or matrix')

class MatProperty(Saveable):
    _freq_dependent: bool = False
    _coord_dependent: bool = False
    _pickle_exclude = {"_func","_fmax"}
    skip_fields = ("_func","_fmax")
    """The MatProperty class is an interface for EMerge to deal with frequency and coordinate dependent material properties
    """
    
    def __init__(self, value: float | complex | int | np.ndarray):
        self._value: np.ndarray = _to_mat(value)
        
        self._x: np.ndarray = np.array([], dtype=np.float64)
        self._y: np.ndarray = np.array([], dtype=np.float64)
        self._z: np.ndarray = np.array([], dtype=np.float64)
        
        self._fmax = lambda f: value
        
    def __call__(self, f: float, data: np.ndarray, coords: np.ndarray, ids: np.ndarray) -> np.ndarray:
        # Separate tensors from scalars
        data[:,:,ids] = np.repeat(self._value[:,:,np.newaxis], ids.shape[0], axis=2)
        return data

    @property
    def value(self) -> float:
        return self._value[0,0]
    
    def scalar(self, f: float):
        return self._value[0,0]
    
    def __getstate__(self):
        state = self.__dict__.copy()
        for k in self._pickle_exclude:
            state.pop(k, None)
        
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        for k in self._pickle_exclude:
            setattr(self, k, None)
    
class FreqDependent(MatProperty, Saveable):
    _freq_dependent: bool = True
    _coord_dependent: bool = False
    skip_fields = ("_func","_fmax")
    def __init__(self, 
                 scalar: Callable | None = None,
                 vector: Callable | None = None,
                 matrix: Callable | None = None):
        """Creates a frequency dependent property object.
        
        If the property is defined as a scalar value, use the "scalar" argument
        If the property is a diagonal rank-2 tensor, use the "vector" argument                   
        If the property is a full rank-2 tensor, use the "matrix" argument

        The max_value property must be set to tell EMerge how height this value can get 
        as it will be used to define the discretization of the mesh.
        
        Args:
            scalar (Callable | None, optional): The scalar value function returning a float/complex. Defaults to None.
            vector (Callable | None, optional): The diagonal rank-2 tensor function returning a (3,) array. Defaults to None.
            matrix (Callable | None, optional): The rank-2 tensor function returning a (3,3) array. Defaults to None.

        """
        if scalar is not None:
            def _func(f: float) -> np.ndarray:
                return np.eye(3)*scalar(f)
        if vector is not None:
            def _func(f: float) -> np.ndarray:
                return np.diag(np.ravel(vector(f)))
        
        if matrix is not None:
            _func = matrix

        self._func: Callable = _func
        
        self._fmax: Callable = lambda f: np.max(np.ravel(self._func(f)))

    def __call__(self, f: float, data: np.ndarray, coords: np.ndarray, ids: np.ndarray) -> np.ndarray:
        # Separate (3,3) tensors and scalars
        data[:,:,ids] = np.repeat(self._func(f)[:,:,np.newaxis], ids.shape[0], axis=2)
        return data
    
    @property
    def value(self) -> float:
        raise ValueError('Frequency dependent material properties have no fixed value. Use the scalar(f) method to get the value at a specific frequency.')
    
    def scalar(self, f: float):
        return self._func(f)[0,0]
    
class CoordDependent(MatProperty,Saveable):
    _freq_dependent: bool = False
    _coord_dependent: bool = True
    skip_fields = ("_func","_fmax")
    def __init__(self, 
                 max_value: float,
                 scalar: Callable | None = None,
                 vector: Callable | None = None,
                 matrix: Callable | None = None,
                 ):
        """Creates a coordinate dependent property object.
        
        If the property is defined as a scalar value, use the "scalar" argument.
        
        If the property is a diagonal rank-2 tensor, use the "vector" argument.
        
        If the property is a full rank-2 tensor, use the "matrix" argument.
        

        The max_value property must be set to tell EMerge how height this value can get 
        as it will be used to define the discretization of the mesh.
        
        Args:
            max_value (float): The heighest value of the material property
            scalar (Callable | None, optional): The scalar value function returning a float/complex. Defaults to None.
            vector (Callable | None, optional): The diagonal rank-2 tensor function returning a (3,) array. Defaults to None.
            matrix (Callable | None, optional): The rank-2 tensor function returning a (3,3) array. Defaults to None.
            
        """
        
        if scalar is not None:
            def _func(x, y, z) -> np.ndarray:
                return np.eye(3)[:, :, None] * scalar(x,y,z)[None, None, :]
        
        if vector is not None:
            def _func(x, y, z) -> np.ndarray:
                N = x.shape[0]
                out = np.zeros((3, 3, N), dtype=vector(0,0,0).dtype)
                idx = np.arange(3)
                out[idx, idx, :] = vector(x,y,z)
                return out
        if matrix is not None:
            _func = matrix

        self._func: Callable = _func
        
        self._values: np.ndarray = None
        self._fmax: Callable = lambda f: max_value
   
    def __call__(self, f: float, data: np.ndarray, coords: np.ndarray, ids: np.ndarray) -> np.ndarray:
        xs = coords[0,ids]
        ys = coords[1,ids]
        zs = coords[2,ids]
        data[:,:,ids] = self._func(xs, ys, zs)
        return data

    @property
    def value(self) -> float:
        return self._func(0,0,0)[0,0]
    
    def scalar(self, f: float):
        return self._func(0,0,0)[0,0]
    
class FreqCoordDependent(MatProperty, Saveable):
    _freq_dependent: bool = True
    _coord_dependent: bool = True
    skip_fields = ("_func","_fmax")
    def __init__(self, 
                 max_value: float,
                 scalar: Callable | None = None,
                 vector: Callable | None = None,
                 matrix: Callable | None = None):
        """Creates a frequency and coordinate dependent property object.
        
        If the property is defined as a scalar value, use the "scalar" argument.
        
        If the property is a diagonal rank-2 tensor, use the "vector" argument.
        
        If the property is a full rank-2 tensor, use the "matrix" argument.

        The max_value property must be set to tell EMerge how height this value can get 
        as it will be used to define the discretization of the mesh.
        
        Args:
            max_value (float): The heighest value of the material property
            scalar (Callable | None, optional): The scalar value function returning a float/complex. Defaults to None.
            vector (Callable | None, optional): The diagonal rank-2 tensor function returning a (3,) array. Defaults to None.
            matrix (Callable | None, optional): The rank-2 tensor function returning a (3,3) array. Defaults to None.

        """
        if scalar is not None:
            def _func(f, x, y, z) -> np.ndarray:
                return np.eye(3)[:, :, None] * scalar(f,x,y,z)[None, None, :]
        
        if vector is not None:
            def _func(f,x, y, z) -> np.ndarray:
                N = x.shape[0]
                out = np.zeros((3, 3, N), dtype=vector(1e9,0,0,0).dtype)
                idx = np.arange(3)
                out[idx, idx, :] = vector(f,x,y,z)
                return out
        
        if matrix is not None:
            _func = matrix

        self._func: Callable = _func
        
        self._fmax: Callable = lambda f: max_value
        
    def __call__(self, f: float, data: np.ndarray, coords: np.ndarray, ids: np.ndarray) -> np.ndarray:
        xs = coords[0,ids]
        ys = coords[1,ids]
        zs = coords[2,ids]
        data[:,:,ids] = self._func(f,xs,ys,zs)
        return data
    
    @property
    def value(self) -> float:
        raise ValueError('Frequency and coordinate dependent material properties have no fixed value. Use the scalar(f) method to get the value at a specific frequency and coordinate.')
    
    def scalar(self, f: float):
        return self._func(f, 0,0,0)[0,0]

class Material(Saveable):
    """The Material class generalizes a material in the EMerge FEM environment.

    If a scalar value is provided for the relative permittivity or the relative permeability
    it will be used as multiplication entries for the material property diadic as identity matrix.

    Additionally, a frequency, coordinate or both frequency and coordinate dependent material property
    may be supplied for the properties: er, ur, tand and cond.

    To supply a frequency-dependent property use: emerge.FreqDependent()
    To supply a coordinate-dependent property use: emerge.CoordDependent()
    to supply a frequency and coordinate dependent property use: emerge.FreqCoordDependent()

    """
    _matnames: list[str] = []
    _namectr: int = 0

    _pickle_exclude = {"_neff"}
    skip_fields = ("_neff",)

    def __init__(
        self,
        er: float | complex | np.ndarray | MatProperty = 1.0,
        ur: float | complex | np.ndarray | MatProperty = 1.0,
        tand: float | MatProperty = 0.0,
        cond: float | MatProperty = 0.0,
        _neff: float | None = None,
        density: float | MatProperty = 1.0,
        cond_thermal: float | MatProperty = 1.0,
        specific_heat: float | MatProperty = 1.0,
        color: str = "#BEBEBE",
        opacity: float = 1.0,
        _metal: bool = False,
        name: str | None = None,
    ):

        if not isinstance(er, MatProperty):
            er = MatProperty(er)
        if not isinstance(ur, MatProperty):
            ur = MatProperty(ur)
        if not isinstance(tand, MatProperty):
            tand = MatProperty(tand)
        if not isinstance(cond, MatProperty):
            cond = MatProperty(cond)

        if not isinstance(density, MatProperty):
            density = MatProperty(density)
        if not isinstance(cond_thermal, MatProperty):
            cond_thermal = MatProperty(cond_thermal)
        if not isinstance(specific_heat, MatProperty):
            specific_heat = MatProperty(specific_heat)

        # Electrical
        self.er: MatProperty = er
        self.ur: MatProperty = ur
        self.tand: MatProperty = tand
        self.cond: MatProperty = cond

        # Thermal
        self.density: MatProperty = density
        self.cond_thermal: MatProperty = cond_thermal
        self.specific_heat: MatProperty = specific_heat

        # Other
        self.name: str = name
        self.color: str = color
        self.opacity: float = opacity
        self._hash_key: int = -1

        if _neff is None:
            self._neff: Callable = lambda f: np.sqrt(
                self.ur._fmax(f) * self.er._fmax(f)
            )
        else:
            self._neff: Callable = lambda f: _neff
        self._metal: bool = _metal

        if self.name is None:
            self.name = self._generate_name()
        
    @classmethod
    def _generate_name(cls) -> str:
        i = cls._namectr
        while True:
            name = f'UnnamedMaterial_{i}'
            if name not in cls._matnames:
                cls._matnames.append(name)
                cls._namectr = i+1
                break
            i += 1
        return name

    @property
    def _color_rgb(self) -> tuple[float, float, float]:
        return tuple(
            int(self.color.lstrip("#")[i : i + 2], 16) / 255.0 for i in (0, 2, 4)
        )

    def __getstate__(self):
        state = self.__dict__.copy()
        for k in self._pickle_exclude:
            state.pop(k, None)

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        for k in self._pickle_exclude:
            setattr(self, k, None)

    def __hash__(self) -> int:
        return id(self)
    
    def __str__(self) -> str:
        return f"Material({self.name})"

    def __repr__(self):
        return f"Material({self.name})"

    @property
    def frequency_dependent(self) -> bool:
        """If The material property are at all frequency dependent."""
        return (
            self.er._freq_dependent
            or self.ur._freq_dependent
            or self.tand._freq_dependent
            or self.cond._freq_dependent
        )

    @property
    def coordinate_dependent(self) -> bool:
        """If the material properties are at all coordinate dependent"""
        return (
            self.er._coord_dependent
            or self.ur._coord_dependent
            or self.tand._coord_dependent
            or self.cond._coord_dependent
        )

    def neff(self, f: float):
        """Computes the maximum occuring effective refractive index for this material."""
        return self._neff(f)

    @property
    def color_rgb(self) -> tuple[float, float, float]:
        return self._color_rgb

    @staticmethod
    def drude_model(
        conductivity: float,
        colission_time: float,
        er: float = 1.0,
        ur: float = 1.0,
        color: str = "#aaaaaa",
        opacity: float = 0.3,
        metal: bool = True,
    ) -> Material:
        """Creates a Material using the Drume model for conductivity
        Requires at least the DC bulk condutivity σ₀ [S/m] and the
        collision time τ.

        Args:
            conductivity (float): The DC bulk conductivity σ₀ in S/m
            colission_time (float): The collision time.
            er (float, optional): The dielectric constant. Defaults to 1.0.
            ur (float, optional): The relative permeability. Defaults to 1.0.
            color (str, optional): The material rendering color. Defaults to "#aaaaaa".
            opacity (float, optional): The material rendering opacity. Defaults to 0.3.
            metal (bool, optional): If it should be rendered as a metal.. Defaults to True.

        Returns:
            Material: The resultant material.
        """
        colission_dist = colission_time / C0
        fsigma = FreqDependent(
            scalar=lambda f: conductivity / (1 - 1j * 2 * np.pi * f * colission_dist)
        )
        return Material(er, ur, 0.0, fsigma, color=color, opacity=opacity, _metal=metal)
    
AIR = Material(
    color="EMERGE-AIR",
    opacity="EMERGE-AIR",
    name="Air",
    cond_thermal=0.026,
    density=1.225,
    specific_heat=1005,
)
COPPER = Material(
    cond=5.8e7,
    color="EMERGE-COPPER",
    opacity="EMERGE-CONDUCTOR",
    _metal=True,
    name="Copper",
    cond_thermal=401,
    density=8960,
    specific_heat=385,
)
PEC = Material(
    color="EMERGE-PEC",
    opacity="EMERGE-CONDUCTOR",
    cond=1e30,
    _metal=True,
    name="PEC",
    cond_thermal=1e30,
    density=8960,
    specific_heat=385,
)