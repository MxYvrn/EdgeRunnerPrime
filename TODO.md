# EdgeRunnerPrime — TODO

Open design questions, deliberately deferred for now.

## Neuron architecture
- Currently single-layered: `N^2 tiles -> 1 shared neuron` (one logistic-regression unit applied to every tile).
- Decide the real arrangement:
  - How many layers?
  - How many neurons per layer?
  - One shared neuron vs. a distinct neuron per tile / region?
  - Hidden layers + activation choice if we go multi-layer.

## Rectangular images
- `compute_edge_grid` currently rejects non-square images.
- Define the procedure for rectangular input (padding? cropping? non-square N x M tiling?).

## Node usage
- `Node` exists (location + visited) but is not yet wired into the N^2 output.
- Decide how the edge grid gets turned into a graph/grid of `Node`s for traversal.

## EdgeRunner chain semantics
- `edge_runner` traces only the component containing its seed tile. A grid
  with several disconnected runs needs the caller to loop, re-seeding while
  `grid_comparer` is non-empty. Decide where that loop lives (caller, or a
  wrapper in `edge_runner.py`).
- A branch point (a tile with 2+ unvisited active neighbours) emits one chain
  per root-to-leaf path, so branched components produce multiple chains that
  share a prefix. Decide whether that is the wanted output or whether branches
  should be merged / split into a single canonical contour.
- An isolated seed (no active neighbours) emits an empty chain `[]`. Decide
  whether degenerate single-tile runs should be emitted at all.
