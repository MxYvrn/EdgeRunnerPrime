# EdgeRunnerPrime — Ideas

Speculative redesigns and directions that aren't on the immediate TODO
but are worth keeping written down.

## Midpoint-seeded DFCCE edge_runner

A different way of running the chain code, decoupled from the current
"seed from an active tile, walk 8-connected actives" approach.

### How the current edge_runner works
- Picks a seed off the active-tile set produced by EdgeFiller.
- Walks 8-connected active tiles.
- Records each step as a turn code relative to `prev_dir` (the
  direction of the previous step).
- The chain is therefore a function of *the walker's own history* --
  every entry depends on the last entry.

### How the midpoint version would work
- Don't seed from an active tile. Seed from the **midpoint of a
  detected shape** -- i.e. an interior point of the region whose
  boundary we want to describe.
- From that midpoint, "find" the surrounding walls by reading the
  averaged regions produced by `grid_avrager` (and probably
  `grid_collapser`). The runner queries the spatial layout of those
  averaged areas rather than stepping one tile at a time.
- The turn chain is derived from that spatial layout directly, not
  from a `prev_dir` reference of past steps. Each entry in the chain
  describes where a wall sits relative to the midpoint, not relative
  to the last step taken.

### Why this might be better
- Removes the path-dependence of the chain: two runs over the same
  shape can't diverge based on which active tile happened to seed
  them.
- Lets the runner use the structure that `grid_avrager` and
  `grid_collapser` already build, instead of re-walking the raw
  activation grid.
- Should handle "objects with internal structure" (e.g. a square with
  lines coming off its faces) more cleanly, because the runner sees
  the whole neighbourhood at once instead of committing to a single
  direction at each step.

### Prerequisites
- **Shape detection.** Need a way to identify how many distinct
  shapes exist in the activation grid and to compute each shape's
  midpoint. Open: definition of "shape" (connected component of
  edges? enclosed non-edge region?), and the midpoint definition
  (centroid, geometric centre, something else). This is already on
  the TODO.
- **A clear contract with `grid_avrager` / `grid_collapser`.** The
  midpoint runner reads from these stages, so their output format
  needs to be stable enough to read against.

### Test pattern to design against
Activation matrix = a square plus four lines, each perpendicular to
one face of the square. A runner placed at the square's midpoint
should be able to find its four walls (the square's sides) and ignore
or separately characterise the four protrusions.

### What this replaces vs. what stays
- Replaces: the active-tile seeded walker that currently lives in
  `edge_runner[OLD].py` (with turn-right + closure + option-2
  branching).
- Stays: DFCCE itself as the chain representation, and Freeman's base-8
  scheme. The midpoint version is about *how* the chain is generated,
  not what the chain is.
