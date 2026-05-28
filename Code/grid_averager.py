import numpy as np

def _is_edge(cell):
    # grid cells are either int 1 (edge sentinel) or an RGB-mean ndarray
    return isinstance(cell, (int, np.integer)) and cell == 1

def grid_averager(grid):
    n_rows, n_cols = grid.shape
    out = grid.copy()

    for j in range(n_cols):
        run_idx = []
        run_vals = []

        def flush():
            if not run_vals:
                return
            mean_val = np.mean(run_vals, axis=0)
            for i in run_idx:
                out[i, j] = mean_val

        for i in range(n_rows):
            cell = grid[i, j]
            if _is_edge(cell):
                flush()
                run_idx = []
                run_vals = []
            else:
                run_idx.append(i)
                run_vals.append(cell)

        flush()
        
    return out