class Node:
    def __init__(self, location, visited=False):
        self.location = location   # (row, col) in the N x N grid
        self.visited = visited

    def __repr__(self):
        return f"Node(location={self.location}, visited={self.visited})"
