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

## Shape detection (prerequisite for new edge_runner)
- Need a way to identify how many distinct "shapes" exist in the activation
  grid and find each shape's midpoint to use as a seed for the new
  edge_runner.
- Open: definition of "shape" (connected component of edges? enclosed
  non-edge region?), and the midpoint definition (centroid, geometric
  center, something else).
