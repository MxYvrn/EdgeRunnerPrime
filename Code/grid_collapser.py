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
                collapsed += [1]
            else:
                run.append(cell)

        if run:
            collapsed.append(np.mean(run, axis=0))

        out_rows.append(collapsed)

    return out_rows
