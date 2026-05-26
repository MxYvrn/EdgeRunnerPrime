"""
Step 4: GridCollapser.

Runs after edge_filler. For each row of the grid, every run of non-edge
tiles between edges (or between an edge and a row boundary) collapses
into a single tile whose value is the mean of the run's colors. Edge
tiles (== 1) stay in place as separators.

  row in : [A, B, 1, C, D, E]
  row out: [mean(A,B), 1, mean(C,D,E)]

Rows are variable length after collapse, so the result is a list of
lists rather than a rectangular ndarray.
"""

import numpy as np


def _is_edge(cell):
    # grid cells are either int 1 (edge sentinel) or an RGB-mean ndarray
    return isinstance(cell, (int, np.integer)) and cell == 1


def grid_collapser(grid):
    out_rows = []

    for row in grid:
        collapsed = []
        run = []

        for cell in row:
            if _is_edge(cell):
                if run:
                    collapsed.append(np.mean(run, axis=0))
                    run = []
                collapsed.append(1)
            else:
                run.append(cell)

        if run:
            collapsed.append(np.mean(run, axis=0))

        out_rows.append(collapsed)

    return out_rows
