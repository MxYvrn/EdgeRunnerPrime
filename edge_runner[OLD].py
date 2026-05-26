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

Traces closed boundaries from the active-tile set left after EdgeFiller
(Step 3) and records each loop as a Directional Freeman Chain Code of
Eight Directions (DFCCE).

Walking rules:
  - Turn-right (right-handed Moore-neighbor): at each step the rightmost
    available active neighbour relative to the incoming direction is
    chosen for the main continuation. Produces clockwise winding so
    rotation-invariant comparisons stay consistent.
  - Closure: a walk terminates and is recorded when it returns to its
    own start tile. Dead-end walks (no closure reached) are still
    appended so nothing is lost.
  - Option 2 branching: at a junction the rightmost turn continues the
    current chain; every other active neighbour spawns an independent
    walk with a fresh chain whose start is the junction itself.
    Branches and main path therefore produce separate shapes.

Two functions live here:
  - edge_filler_checker rebuilds the active-tile set from a filled 0/1
    grid, for callers that hold the grid but not the set.
  - edge_runner is the tracer.

Option 1 (shared-prefix branching, the pre-rewrite behaviour) is kept
commented out at the bottom of this file for reference.
"""

import numpy as np

# Directional Freeman Chain Code of Eight Directions (DFCCE)
# as much as i wanna say i came up with this alghorithm with pretty much the same implemention  (wasnt gonna use base 8),
# he came up with it first, plus his implementation is just so much more elegant mathamtically which means it is more elegent full stop.

# "Herb had a profound impact on my life and I was lucky to live close to him in Princeton last few years and meet him from time to time." -- Indranil Chakravarty
# died: November 15, 2020 (aged 94), New Jersey, United States

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

# Turn-right priority over the 8 relative turns.
# rel = (abs_dir - prev_dir) % 8
# 0=straight, 1=slight R, 2=hard R, 3=sharp R, 4=back,
# 5=sharp L, 6=hard L, 7=slight L.
# Lower value = preferred. Heuristic; may need tuning for tight junctions.
TURN_RIGHT_PRIORITY = {2: 0, 1: 1, 3: 2, 0: 3, 7: 4, 5: 5, 6: 6, 4: 7}


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


def edge_runner(grid_comparer, grid_filler, chain, x, y, global_chain, prev_dir=None, start_xy=None) -> None:
    """
    Walk one step of a closed-loop trace.

    Args:
        grid_comparer: set of (i, j) active-tile coords; doubles as the
            visited set, with tiles removed as they are walked.
        grid_filler: N x N array of 0/1 edge activations. Used for bounds
            checks and for collecting neighbours regardless of whether
            they've been consumed yet (needed so closure can see the
            start tile after it's been popped).
        chain: list of turn codes for the walk in progress. Pass None on
            the first call to begin a fresh walk; the seed will be popped
            from grid_comparer.
        x, y: current tile. Ignored on the first call (chain is None).
        global_chain: accumulator; each completed walk -- closed loop or
            dead-end -- is appended here.
        prev_dir: absolute direction (0-7) of the previous step, or None
            on the first step of a walk.
        start_xy: (i, j) of this walk's start tile, used for the closure
            check. Set internally on the first call.

    Returns:
        None -- results are collected in global_chain.
    """
    n_rows, n_cols = grid_filler.shape

    if chain is None:
        chain = []
        x, y = grid_comparer.pop()
        start_xy = (x, y)

    neighbors = []
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            fi, fj = x + di, y + dj
            if not (0 <= fi < n_rows and 0 <= fj < n_cols):
                continue
            if grid_filler[fi, fj] == 1:
                neighbors.append((di, dj, fi, fj))

    for di, dj, fi, fj in neighbors:
        if (fi, fj) == start_xy and len(chain) >= 3:
            abs_dir = DIR_CODE[(di, dj)]
            turn = abs_dir if prev_dir is None else (abs_dir - prev_dir) % 8
            global_chain.append(chain + [turn])
            return

    fresh = [(di, dj, fi, fj) for (di, dj, fi, fj) in neighbors if (fi, fj) in grid_comparer]
    if not fresh:
        global_chain.append(chain.copy())
        return

    def sort_key(item):
        di, dj, _, _ = item
        abs_dir = DIR_CODE[(di, dj)]
        if prev_dir is None:
            return abs_dir
        rel = (abs_dir - prev_dir) % 8
        return TURN_RIGHT_PRIORITY[rel]

    fresh.sort(key=sort_key)

    di_m, dj_m, fi_m, fj_m = fresh[0]
    abs_dir_m = DIR_CODE[(di_m, dj_m)]
    turn_m = abs_dir_m if prev_dir is None else (abs_dir_m - prev_dir) % 8
    grid_comparer.discard((fi_m, fj_m))

    # Option 2: side branches at a junction begin their own walk with the
    # junction tile as their start, so each branch produces its own shape.
    for di_b, dj_b, fi_b, fj_b in fresh[1:]:
        abs_dir_b = DIR_CODE[(di_b, dj_b)]
        grid_comparer.discard((fi_b, fj_b))
        edge_runner(grid_comparer, grid_filler, [abs_dir_b], fi_b, fj_b, global_chain, abs_dir_b, (x, y))

    edge_runner(grid_comparer, grid_filler, chain + [turn_m], fi_m, fj_m, global_chain, abs_dir_m, start_xy)


# ---------------------------------------------------------------------------
# OPTION 1 (shared-prefix branching) -- pre-rewrite behaviour, kept for
# reference. Each branch at a junction carries the parent's chain prefix,
# so a Y-junction yields multiple chains that share their first segment.
# Has no turn-right rule and no closure check; terminates only when a
# walk runs out of unvisited active neighbours.
# ---------------------------------------------------------------------------
#
# def edge_runner(grid_comparer, grid_filler, chain, x, y, global_chain, prev_dir=None) -> set:
#     n_rows, n_cols = grid_filler.shape
#
#     isFound = False
#     diri = [-1, 0, 1]
#     dirj = [-1, 0, 1]
#
#     #begining:
#     if chain is None:
#         chain = []
#         x,y = grid_comparer.pop()  # get a seed tile to start the chain
#
#     #middle:
#     for di in diri:
#         fi = x + di
#         for dj in dirj:
#             fj = y + dj
#
#             #edge cases:
#             if di == 0 and dj == 0:
#                 continue  #skip (0,0)
#             if not (0 <= fi < n_rows and 0 <= fj < n_cols):
#                 continue
#
#             #finder (actually important bit):
#             if grid_filler[fi, fj] == 1:
#                 isFound = True
#                 abs_dir = DIR_CODE[(di, dj)]
#
#                 turn = abs_dir if prev_dir is None else (abs_dir - prev_dir) % 8
#                 new_chain = chain + [turn]  # fresh list per branch
#
#                 grid_comparer.discard((fi, fj))
#                 edge_runner(grid_comparer, grid_filler, new_chain, fi, fj, global_chain, abs_dir)
#
#     #end:
#     if isFound == False:
#         global_chain.append(chain.copy())
