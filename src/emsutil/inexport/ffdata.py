import numpy as np
from .strutil import arry_to_line, matrix_to_lines, arry_to_fwl
from ..emdata import EHFieldFF
from dataclasses import dataclass
from typing import List
from loguru import logger
import os

@dataclass
class Column:
    name: str
    values: np.ndarray

    @staticmethod
    def from_array(name: str, data: np.ndarray) -> List["Column"]:
        """
        Returns:
        - [Column] if data is real
        - [Column(real), Column(imag)] if data is complex
        """
        data = np.asarray(data)

        if np.iscomplexobj(data):
            return [
                Column(f"{name}[re]", data.real),
                Column(f"{name}[im]", data.imag),
            ]
        else:
            return [Column(name, data)]


def to_lines(
    columns: List[Column],
    header_prefix: str = "$ ",
    separator: str = "  ",
    fmt: str = "{:g}",
) -> List[str]:
    """
    Convert columns to equally spaced text lines.
    """

    # Convert all values to strings first
    str_cols = [[fmt.format(v) for v in col.values] for col in columns]
    headers = [col.name for col in columns]
    headers[0] = header_prefix + headers[0]
    for i in range(len(headers)-1):
        headers[i] = headers[i] + ';'
    # Compute column widths (including separator!)
    widths = []
    for h, col in zip(headers, str_cols):
        widths.append(max(len(h), max(len(v) for v in col)))

    def format_row(items, sep: str):
        return sep.join(item.ljust(w) for item, w in zip(items, widths))

    lines = []

    # Header
    lines.append(format_row(headers, separator))

    # Data rows
    nrows = len(columns[0].values)
    for i in range(nrows):
        row = [col[i] for col in str_cols]
        lines.append(format_row(row, separator))

    return lines

class _fieldGetter:
    
    def __init__(self, fields: list[EHFieldFF]):
        self.names: list[str] = []
        self.data: list = fields
    
    @property
    def name(self) -> str:
        return '.'.join([n.capitalize() for n in self.names])
        
    def __getattr__(self, name: str) -> EHFieldFF:
        self.names.append(name)
        self.data = [getattr(item, name) for item in self.data]
        return self
    
class FarFieldExporter:
    """A class to export far-field data to a text file.
    
    """
    def __init__(self, filename: str, fields: list[EHFieldFF], precision: int = 4, todeg: bool = True):
        self.filename: str = filename
        self.fields: list[EHFieldFF] = fields
        self.precision: int = precision
        self.columns: list[_fieldGetter] = []
        self.todeg: bool = todeg
    
    def addcol(self) -> EHFieldFF:
        """Returns a field getter to specify which field component to export.
        
        Example:
        >>> exporter = FarFieldExporter('data.txt', field_data)
        >>> exporter.addcol().Ex
        >>> exporter.addcol().gain.theta
        >>> exporter.write()

        Returns:
            EHFieldFF(_fieldGetter): Field getter to specify field component.
        """
        getter = _fieldGetter(self.fields)
        self.columns.append(getter)
        return getter
    
    def write(self) -> None:
        """Saves the far-field data to a text file.
        """
        base = self.fields[0]
        
        thetas = base.theta
        phis = base.phi
        
        theta_lin = thetas[0,:].flatten()
        phi_lin = phis[:,0].flatten()
        p = self.precision
        mult = 1.0
        unit = 'rad'
        if self.todeg:
            mult = 180.0 / np.pi
            theta_lin = theta_lin * mult
            phi_lin = phi_lin * mult
            thetas = thetas * mult
            phis = phis * mult
            unit = 'deg'
        
        datalines = []
        datalines.append(f'% Theta({unit})')
        datalines.append(' '.join([f'{x:.{p}g}' for x in theta_lin]))
        datalines.append(f'% Phi({unit})')
        datalines.append(' '.join([f'{x:.{p}g}' for x in phi_lin]))
        datalines.append('% Frequencies(Hz)')
        datalines.append(' '.join([f'{field.freq:.{p}g}' for field in self.fields]))
        datalines.append('')
        thcol = Column(f'Theta({unit})', thetas.flatten())
        phcol = Column(f'Phi({unit})', phis.flatten())
        
        for i, field in enumerate(self.fields):
            freq = field.freq
            cols = []
            datalines.append(f'# {freq:.{p}g} Hz')
            for col in self.columns:
                cols.extend(Column.from_array(col.name, col.data[i].flatten()))
            
            datalines.extend(to_lines([thcol, phcol] + cols, fmt=f"{{:.{p}g}}"))
            datalines.append('')
        
        #replace any extension of filename with.emff
        filename = os.path.splitext(self.filename)[0] + '.emff'
        self.filename = filename
        with open(self.filename, 'w') as f:
            f.write('\n'.join(datalines))
        logger.info(f'Wrote far-field data to {self.filename}')
        
def import_farfield(filename: str, degrees: bool = True) -> dict[str, np.ndarray]:
    """Reads emerge farfiel datafiles created by FarFieldExporter.
    They can be recognized by the .emff extension.

    Args:
        filename (str): The path to the far-field data file.
        degrees (bool): If True, theta and phi angles are converted to degrees.

    Returns:
        dict[str, np.ndarray]: The imported far-field data structured as:
            {
                "theta": np.ndarray,  # Theta grid (nTheta, nPhi)
                "phi": np.ndarray,    # Phi grid (nTheta, nPhi)
                "freq": np.ndarray,   # Frequencies (nF,)
                "Ex": np.ndarray,     # Electric field component Ex (nF, nTheta, nPhi)
                "Ey": np.ndarray,     # Electric field component Ey (nF, nTheta, nPhi)
                ...
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    # ---------------- helpers ----------------
    def parse_vector(header):
        i = lines.index(header) + 1
        return np.array(lines[i].split(), float)

    def strip_unit(name):
        if "(" in name and ")" in name:
            base, unit = name.split("(")
            return base.strip(), unit.rstrip(")")
        return name.strip(), None

    def to_rad(values, unit):
        if unit == "deg":
            return np.deg2rad(values)
        return values

    # ---------------- global grids ----------------
    theta_name, theta_unit = strip_unit("% Theta(deg)")
    phi_name,   phi_unit   = strip_unit("% Phi(deg)")

    # Find actual headers (deg or rad)
    theta_header = next(l for l in lines if l.startswith("% Theta"))
    phi_header   = next(l for l in lines if l.startswith("% Phi"))

    theta_vals = parse_vector(theta_header)
    phi_vals   = parse_vector(phi_header)
    freqs      = parse_vector("% Frequencies(Hz)\n")

    theta_unit = theta_header.split("(")[1].split(")")[0]
    phi_unit   = phi_header.split("(")[1].split(")")[0]

    theta_vals = to_rad(theta_vals, theta_unit)
    phi_vals   = to_rad(phi_vals, phi_unit)

    nTheta = len(theta_vals)
    nPhi   = len(phi_vals)
    nF     = len(freqs)

    theta_grid, phi_grid = np.meshgrid(theta_vals, phi_vals, indexing="ij")

    result = {
        "theta": theta_grid,
        "phi": phi_grid,
        "freq": freqs,
    }

    # ---------------- frequency blocks ----------------
    field_buffers = {}
    column_map = {}
    header_info = {}
    fidx = -1
    header_cols = None
    data_rows = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Frequency block
        if line.startswith("#"):
            fidx += 1
            data_rows = []
            continue

        # Header line
        if line.startswith("$"):
            header_cols = []
            column_map.clear()
            header_info.clear()

            raw_cols = line[1:].split(";")
            for i, raw in enumerate(raw_cols):
                name, unit = strip_unit(raw)
                header_cols.append(name)
                header_info[name] = unit

                if "[" in name and "]" in name:
                    base, comp = name.split("[")
                    comp = comp.rstrip("]")
                    column_map.setdefault(base, {})[comp] = i
                else:
                    column_map[name] = i
            continue

        if line.startswith("%"):
            continue

        parts = line.split()
        if header_cols is None or len(parts) < len(header_cols):
            continue

        data_rows.append([float(p) for p in parts])

        if len(data_rows) == nTheta * nPhi:
            data = np.array(data_rows)

            for field, comps in column_map.items():
                unit = header_info.get(field)

                if isinstance(comps, dict):  # complex
                    re = data[:, comps["re"]]
                    im = data[:, comps["im"]]
                    arr = re + 1j * im
                else:  # real
                    arr = data[:, comps]

                if unit in ("deg", "rad"):
                    arr = to_rad(arr, unit)

                arr = arr.reshape(nTheta, nPhi)
                field_buffers.setdefault(field, []).append(arr)

    
    # Stack frequencies
    for field, blocks in field_buffers.items():
        result[field] = np.stack(blocks, axis=0)
    
    if degrees:
        result["theta"] = np.rad2deg(result["theta"])
        result["phi"] = np.rad2deg(result["phi"])
        result["Theta"] = np.rad2deg(result["Theta"])
        result["Phi"] = np.rad2deg(result["Phi"])
    return result
