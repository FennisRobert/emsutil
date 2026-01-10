import numpy as np
from .strutil import arry_to_line, matrix_to_lines, arry_to_fwl
from ..emdata import EHFieldFF

def export_ffdata(filename: str, 
                  thetas: np.ndarray,
                  phis: np.ndarray,
                  frequencies: np.ndarray,
                  fields: list[EHFieldFF],
                  precision: int = 4) -> None:
    
    lines = []
    lines.append('% Theta (deg)')
    lines.append(arry_to_line(thetas, precision=precision))
    lines.append('% Phi (deg)')
    lines.append(arry_to_line(phis, precision=precision))
    lines.append('')
    nF = frequencies.shape[0]
    
    actual_frequencies = []
    blocks = []
    
    T, P = np.meshgrid(thetas, phis, indexing='ij')
    
    thetal = T.flatten()
    phil = P.flatten()
    
    for iF in range(nF):
        freq = frequencies[iF]
        actual_frequencies.append(freq)
        
        farfield = fields[iF]._E
        Fx = farfield[0,:,:].squeeze().flatten()
        Fy = farfield[1,:,:].squeeze().flatten()
        Fz = farfield[2,:,:].squeeze().flatten()
        
        block_lines = []
        
        block_lines.append(f'# {freq} (Hz)')
        block_lines.append('$ Theta(deg); Phi(deg); E_x[re](V/m); E_x[im](V/m); E_y[re](V/m); E_y[im](V/m); E_z[re](V/m); E_z[im](V/m)')
        positions = (0, 14, 24, 38, 52, 66, 80, 94)
        for th, ph, ex, ey, ez in zip(thetal, phil, Fx, Fy, Fz):
            re_ex = np.real(ex)
            im_ex = np.imag(ex)
            re_ey = np.real(ey)
            im_ey = np.imag(ey)
            re_ez = np.real(ez)
            im_ez = np.imag(ez)
            line_values = np.array([th, ph, re_ex, im_ex, re_ey, im_ey, re_ez, im_ez])
            line = arry_to_fwl(line_values, positions, precision=precision)
            block_lines.append(line)

        lines.extend(block_lines)
        lines.extend('')
    
    text = '\n'.join(lines)
    with open(filename, 'w') as f:
        f.write(text)