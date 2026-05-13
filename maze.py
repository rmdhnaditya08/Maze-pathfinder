"""
core/maze.py
Grid maze + generator menggunakan DFS Recursive Backtracker.
"""

import random
from cell import Cell


class Maze:
    """
    Grid 2D berisi objek Cell.
    Maze dihasilkan menggunakan DFS Recursive Backtracker:
      - Mulai dari sel (0,0)
      - Pilih tetangga yang belum dikunjungi secara acak
      - Hapus dinding di antara keduanya
      - Backtrack jika tidak ada tetangga yang belum dikunjungi
    Hasilnya: maze yang selalu punya solusi (perfect maze).
    """

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Cell]] = [
            [Cell(r, c) for c in range(cols)] for r in range(rows)
        ]
        self._generate()

    # ── PUBLIC ────────────────────────────────────────────

    def get(self, row: int, col: int) -> Cell | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def neighbors_open(self, row: int, col: int) -> list[tuple[int, int]]:
        """Tetangga yang bisa dilewati (tanpa dinding)."""
        return self.grid[row][col].open_neighbors(self.grid)

    # ── GENERATOR (DFS Recursive Backtracker) ─────────────

    def _generate(self):
        """
        Algoritma: DFS Recursive Backtracker (iteratif menggunakan stack).
        Kompleksitas: O(rows * cols)
        """
        visited = [[False] * self.cols for _ in range(self.rows)]
        stack = [(0, 0)]
        visited[0][0] = True

        while stack:
            r, c = stack[-1]
            # Cari semua tetangga yang belum dikunjungi
            unvisited = []
            for direction, (dr, dc) in Cell.DIRS.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if not visited[nr][nc]:
                        unvisited.append((direction, nr, nc))

            if unvisited:
                direction, nr, nc = random.choice(unvisited)
                # Buka dinding antara current dan neighbor
                self.grid[r][c].open_wall(direction)
                self.grid[nr][nc].open_wall(Cell.OPPOSITE[direction])
                visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()

    def __repr__(self):
        return f"Maze({self.rows}x{self.cols})"
