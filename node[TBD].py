"""
Step 2: Node.

A Node represents one tile position in the N^2 grid as the edge tracer
walks it. For now it only tracks where it is and whether it's been seen.
"""


class Node:
    def __init__(self, location, visited=False):
        self.location = location   # (row, col) in the N x N grid
        self.visited = visited

    def __repr__(self):
        return f"Node(location={self.location}, visited={self.visited})"
