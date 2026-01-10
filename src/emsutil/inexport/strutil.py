import numpy as np

def arry_to_line(array: np.ndarray, separator: str = ' ', precision: int = 4) -> str:
    return separator.join([f"{x:.{precision}f}" for x in array.squeeze()])

def arry_to_fwl(array: np.ndarray, start_positions: list[int], precision: int = 4) -> str:
    # Place the numbers at the starting position indices provided by the start-positions list
    line_length = max(start_positions) + 10  # Extra space for number
    line = [' ']*line_length
    for i, pos in enumerate(start_positions):
        num_str = f"{array[i]:.{precision}f}"
        for j, ch in enumerate(num_str):
            if pos + j < line_length:
                line[pos + j] = ch
    return ''.join(line)

def matrix_to_lines(matrix: np.ndarray, separator: str = ',', precision: int = 4) -> str:
    lines = []
    for row in matrix:
        line = arry_to_line(row, separator, precision)
        lines.append(line)
    return '\n'.join(lines)