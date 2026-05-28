import numpy as np

# 8 unit directions, generated from {-1,0,1}^2 (skip the no-move case)
_DIRECTIONS = [
    (di, dj)
    for di in (-1, 0, 1)
    for dj in (-1, 0, 1)
    if not (di == 0 and dj == 0)
] # above array / tuple thing should be removed 

def edge_filler(grid, grid_comparer, d=2):
    """
    Args:
        grid: N x N array of 0/1 edge activations (the "normal grid")
        grid_comparer: set of (i, j) coords of active tiles, as returned
            by compute_edge_grid in n2_neurons.py
        d: gap span to bridge (look-distance). d=2 fills one midpoint;
           d=k fills the k-1 tiles between an active tile and a far one.

    Returns:
        New N x N array (same dtype as grid) with gaps filled.
    """

    dir = []
    for directions in range(-1*d, d + 1):
        dir.append(directions)

    snapshot = np.asarray(grid)
    n_rows, n_cols = snapshot.shape
    grid_filled = snapshot.copy()

    for i, j in grid_comparer:  # readability of this line is kinda bad imo, but it is more efficient 
        
        for di in dir:
            fi = i + di
            
            for dj in dir:
                fj = j + dj        # far tile, distance d
            
                if not (0 <= fi < n_rows and 0 <= fj < n_cols):
                    continue
            
                if snapshot[fi, fj] == 1:
                    # fill the d-1 in-between tiles (guaranteed in bounds:
                    # each sits strictly between two in-bounds endpoints)
                    for step in range(1, d):
                        mi = i + di * step 
                        mj = j + dj * step
                        if snapshot[mi, mj] == 0:
                            grid_filled[mi, mj] = 1

    return grid_filled

def edge_filter(global_chain,cutter):
    for i in global_chain:
        if len(i) < cutter:
            global_chain.remove(i)
    return global_chain
