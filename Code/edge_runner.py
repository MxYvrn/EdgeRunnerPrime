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

#________________________________________________________________________________________#

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

def edge_filler_checker(grid_filler) -> set:
    """Rebuild the active-tile set from a filled 0/1 grid (edge_runner needs both)."""
    n_rows, n_cols = grid_filler.shape
    grid_comparer = set()

    for i in range(n_rows):
        for j in range(n_cols):
            
            if grid_filler[i, j] == 1:
                grid_comparer.add((i, j))

    return grid_comparer


def edge_runner(grid_comparer, grid_filler, chain, global_chain, x, y, prev_dir=None, start_xy=None, shortner=10) -> None:
    """
    Trace boundary paths through active tiles, recording each as a DFCCE chain.

    First step records absolute Freeman dir (0-7); subsequent steps record
    relative turn `(abs_dir - prev_dir) % 8`. Tiles are popped from
    `grid_comparer` as walked. Multi-neighbour tiles branch (shared prefix).
    A walk ends on closure (back to seed, len >= `shortner`) or dead end;
    either way it's appended to `global_chain`.

    `chain=None` starts a fresh walk (seed popped from `grid_comparer`).
    `grid_filler` is read-only -- used for bounds + walkability + closure.
    """
    n_rows, n_cols = grid_filler.shape
    found = False

    #beginning:
    if chain is None:
        chain = []
        x, y = grid_comparer.pop()
        start_xy = (x, y)

    #middle:
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):

            fi = x + di
            fj = y + dj
            
            #closure check:
            if (fi, fj) == start_xy and len(chain) >= shortner:
                abs_dir = DIR_CODE[(di, dj)]
                turn = abs_dir if prev_dir is None else (abs_dir - prev_dir) % 8
                global_chain.append(chain + [turn])
                return

            elif di == 0 and dj == 0:
                continue

            elif not (0 <= fi < n_rows and 0 <= fj < n_cols):
                continue

            elif grid_filler[fi, fj] == 1:
                found = True
                abs_dir = DIR_CODE[(di, dj)]
                turn = abs_dir if prev_dir is None else (abs_dir - prev_dir) % 8
                grid_comparer.discard((fi, fj))
                edge_runner(grid_comparer, grid_filler, (chain + [turn]), global_chain, fi, fj, abs_dir, start_xy, shortner)
            
    #end:
    if found == False:
        global_chain.append(chain)
        return