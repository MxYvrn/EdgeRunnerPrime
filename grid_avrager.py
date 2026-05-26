"""
Step (parallel branch): GridAvrager.

Vertical counterpart to grid_collapser, but shape-preserving. For each
column, every non-edge cell is replaced by the mean of the vertical run
(column segment bounded by edge cells, or by the column boundary) it
belongs to. All cells in the same run end up holding the same averaged
color. Edge cells (== 1) pass through unchanged.

  col in : [A, B, 1, C, D, E]
  col out: [m(A,B), m(A,B), 1, m(C,D,E), m(C,D,E), m(C,D,E)]

Output is the same N x N object grid; cells are either int 1 or an
RGB-mean ndarray, matching the input convention from n2_grid /
edge_filler.
"""

import numpy as np


def _is_edge(cell):
    # grid cells are either int 1 (edge sentinel) or an RGB-mean ndarray
    return isinstance(cell, (int, np.integer)) and cell == 1


def grid_avrager(grid):
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
