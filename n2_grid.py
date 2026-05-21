# “The Grid. A digital frontier. I tried to picture clusters of information as they moved through the computer. 
# What did they look like? Ships, motorcycles? Were the circuits like freeways? I kept dreaming of a world, I thought I'd never see. 
# And then, one day I got in...”

# The Grid -- Daft Punk, from the TRON: Legacy soundtrack

"""
Step 1: N^2 Edge Neurons.

Takes a square RGB image, subdivides it into an N x N grid of tiles
(N^2 tiles total -- hence the name "N^2"), and runs a single trained
neuron over each tile to decide edge / no-edge.

Neuron arrangement is single-layered for now: N^2 tiles -> 1 neuron.
The question of how many layers / neurons to use is deferred (see TODO.md).
"""

import json
import numpy as np

class N2N:
    """A single logistic-regression neuron: p = sigmoid(W . x + b)."""

    def __init__(self):
        self.tile_size = None
        self.W = None
        self.b = None

    def load_weights(self, path):
        
        with open(path) as f:
            data = json.load(f)
        
        self.tile_size = int(data["tile_size"])
        self.W = np.array(data["W"], dtype=np.float32)
        self.b = float(data["b"])

    def is_edge(self, tile):
        """Return 1 if the tile contains an edge, else 0."""
        
        if self.W is None:
            raise ValueError("Weights not loaded. Call load_weights() first.")
        
        x = tile.reshape(-1).astype(np.float32) / 255.0
        
        z = float(np.dot(self.W, x) + self.b)
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        
        return 1 if p > 0.5 else 0


def compute_edge_grid(image, weights_path):
    """
    Subdivide a square image into N^2 tiles and classify each as edge / no-edge.

    Args:
        image: square RGB image, shape (S, S, 3)
        weights_path: path to the neuron weights JSON

    Returns:
        np.ndarray of shape (N, N), values 0/1, where N = S // tile_size
    """

    H, W = image.shape[:2]
    if H != W:
        # Rectangular handling is TBD -- see TODO.md
        raise ValueError(
            f"N2 expects a square image, got {H}x{W}. "
            f"Rectangular support is TBD (see TODO.md)."
        )

    neuron = N2N()
    neuron.load_weights(weights_path)
    ts = neuron.tile_size

    n = H // ts  # grid is n x n  ->  n^2 tiles
    grid = np.zeros((n, n), dtype=np.int8)
    gridComparer = set()

    #actually imp thing:
    for i in range(n):
        for j in range(n):
            
            tile = image[ i*ts : (i + 1)*ts , j*ts : (j + 1)*ts , :]
            edge = neuron.is_edge(tile)
            grid[i, j] = edge

            if edge == 1:
                gridComparer.add((i, j))

    return grid, gridComparer