"""
core/cell.py
Representasi satu sel dalam grid maze.
"""


class Cell:
    """
    Setiap sel memiliki 4 dinding (top, right, bottom, left).
    Dinding True = ada dinding, False = terbuka (jalan).
    """

    DIRS = {
        "top":    (-1,  0),
        "bottom": ( 1,  0),
        "left":   ( 0, -1),
        "right":  ( 0,  1),
    }

    OPPOSITE = {
        "top": "bottom",
        "bottom": "top",
        "left": "right",
        "right": "left",
    }

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self._visited = False   # dipakai saat generate

    def open_wall(self, direction: str):
        """Buka dinding ke arah tertentu."""
        self.walls[direction] = False

    def can_go(self, direction: str) -> bool:
        """True jika tidak ada dinding ke arah itu."""
        return not self.walls[direction]

    def open_neighbors(self, grid: list) -> list:
        """
        Kembalikan list (row, col) tetangga yang bisa diakses
        (tidak ada dinding di antara).
        """
        result = []
        rows = len(grid)
        cols = len(grid[0])
        for direction, (dr, dc) in self.DIRS.items():
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not self.walls[direction]:
                    result.append((nr, nc))
        return result

    def __repr__(self):
        return f"Cell({self.row}, {self.col})"
