#I couldn't wait for you to come and clear the cupboards
#But now you're gone and leaving nothing but a sign
#Another evening, I'll be sitting reading in-between your lines
#Because I miss you all the time

#So, get away
#Another way to feel what you didn't want yourself to know
#And let yourself go
#You know you didn't lose your self-control
#Let's start at the rainbow
#Turn away
#Another way to be where you didn't want yourself to go
#And let yourself go
#Is that a compromise?

# "I Really Wanted to Stay at Your House" -- Rosa Walton, Hallie Coggins,

"""
Step 4: EdgeRunner.

Takes the active-tile set left after EdgeFiller (Step 3) and traces
connected runs of active tiles, recording each run as a Directional
Freeman Chain Code of Eight Directions (DFCCE).

Two functions live here:
  - edge_filler_checker rebuilds the active-tile set from a filled 0/1
    grid, for callers that hold the grid but not the set.
  - edge_runner is the tracer: from a seed tile it recurses into active
    8-neighbours and appends one chain of turn codes per walk to
    global_chain.

Turn codes come from DIR_CODE: the first step of a walk records an
absolute direction (0-7), every later step the turn taken relative to
the previous direction.
"""

import numpy as np

# Directional Freeman Chain Code of Eight Directions (DFCCE)
# as much as i wanna say i came up with this alghorithm with pretty much the same implemention  (wasnt gonna use base 8), 
# he came up with it first, plus his implementation is just so much more elegant mathamtically which means it is more elegent full stop.

# "Herb had a profound impact on my life and I was lucky to live close to him in Princeton last few years and meet him from time to time." -- Indranil Chakravarty
# died:    November 15, 2020 (aged 94), New Jersey, United States 

DIR_CODE = {
    (-1,  0): 0,  # N
    (-1,  1): 1,  # NE
    ( 0,  1): 2,  # E
    ( 1,  1): 3,  # SE
    ( 1,  0): 4,  # S
    ( 1, -1): 5,  # SW
    ( 0, -1): 6,  # W
    (-1, -1): 7,  # NW
}

def edge_filler_checker(grid_filler) -> set:
    """
    Collect the coordinates of every active tile in a filled grid.

    Args:
        grid_filler: N x N array of 0/1 edge activations -- the filled
            grid returned by edge_filler in Step 3.

    Returns:
        set of (i, j) coords of every tile equal to 1, i.e. the same kind
        of active-tile set compute_edge_grid (Step 1) returns.
    """
    n_rows, n_cols = grid_filler.shape
    active_set = set()
    
    for i in range(n_rows):
        for j in range(n_cols):
            if grid_filler[i, j] == 1:
                active_set.add((i, j))

    return active_set


def edge_runner(grid_comparer, grid_filler, chain, x, y, global_chain, prev_dir=None) -> set:
    """
    Recursively trace a run of connected active tiles into a chain code.

    Starting from tile (x, y), steps into each unvisited active
    8-neighbour, extending the chain by one turn code (see DIR_CODE)
    per step. A walk with no unvisited neighbour left is appended to
    global_chain.

    Args:
        grid_comparer: set of (i, j) active-tile coords; also serves as
            the visited set, with tiles removed as they are walked.
        grid_filler: N x N array of 0/1 edge activations, used for the
            bounds check and the active-tile lookup.
        chain: list of turn codes for the walk in progress. Pass None on
            the first call to begin a fresh walk from a seed tile.
        x, y: current tile. Ignored on the first call (chain is None),
            where the seed tile is popped from grid_comparer instead.
        global_chain: accumulator; each completed chain is appended here.
        prev_dir: absolute direction (0-7) of the previous step, or None
            for the first step of a walk.

    Returns:
        None -- results are collected in global_chain.
    """
    
    n_rows, n_cols = grid_filler.shape

    isFound = False
    diri = [-1, 0, 1]
    dirj = [-1, 0, 1]

    #begining:
    if chain is None:
        chain = []
        x,y = grid_comparer.pop()  # get a seed tile to start the chain

    #middle:
    for di in diri:
        fi = x + di
        for dj in dirj:
            fj = y + dj

            #edge cases:
            if di == 0 and dj == 0:
                continue  #skip (0,0)
            if not (0 <= fi < n_rows and 0 <= fj < n_cols):
                continue
            
            #finder (actually important bit):
            if grid_filler[fi, fj] == 1:
                isFound = True
                abs_dir = DIR_CODE[(di, dj)]

                turn = abs_dir if prev_dir is None else (abs_dir - prev_dir) % 8
                new_chain = chain + [turn]  # fresh list per branch

                grid_comparer.discard((fi, fj))
                edge_runner(grid_comparer, grid_filler, new_chain, fi, fj, global_chain, abs_dir)
    
    #end:
    if isFound == False:
        global_chain.append(chain.copy())

    


