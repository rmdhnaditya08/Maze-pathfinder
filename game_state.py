"""
core/game_state.py
State machine game: PLAYING → WIN.
Juga menyimpan logika gerakan pemain dan validasi.
"""

import time
from enum import Enum, auto
from maze   import Maze
from player import Player
from cell   import Cell
from dijkstra import dijkstra


class State(Enum):
    PLAYING = auto()
    WIN     = auto()


class GameState:
    """
    Mengelola seluruh logika game:
      - Maze generation
      - Gerakan pemain (dengan validasi dinding)
      - Aktivasi hint Dijkstra
      - Deteksi kemenangan
      - Level progression
    """

    START_POS = (0, 0)

    # Ukuran maze per level
    LEVEL_SIZES = [11, 15, 19, 23, 29, 35]

    def __init__(self):
        self.level       = 1
        self.state       = State.PLAYING
        self._new_maze()

    # ── MAZE SETUP ─────────────────────────────────────────────────────

    def _new_maze(self):
        size = self._level_size()
        self.maze_size = size
        self.maze      = Maze(size, size)
        self.player    = Player(*self.START_POS)
        self.end_pos   = (size - 1, size - 1)
        self.state     = State.PLAYING

        # Hint (Dijkstra)
        self.hint_active   = False
        self.hint_path:   list  = []
        self.hint_visited: set  = set()
        self.optimal_steps: int = 0

        # Timer
        self._start_time = time.time()
        self.elapsed     = 0.0

        # Trail gerakan pemain
        self.trail: set[tuple[int, int]] = {self.START_POS}

    def _level_size(self) -> int:
        idx = min(self.level - 1, len(self.LEVEL_SIZES) - 1)
        return self.LEVEL_SIZES[idx]

    # ── ACTIONS ────────────────────────────────────────────────────────

    def new_maze(self):
        """Buat maze baru di level yang sama."""
        self._new_maze()

    def restart(self):
        """Restart dari posisi awal, maze sama."""
        self.player.reset(*self.START_POS)
        self.trail        = {self.START_POS}
        self.hint_active  = False
        self.hint_path    = []
        self.hint_visited = set()
        self.state        = State.PLAYING
        self._start_time  = time.time()
        self.elapsed      = 0.0

    def next_level(self):
        """Naik level dan buat maze baru."""
        self.level += 1
        self._new_maze()

    def move(self, direction: str) -> bool:
        """
        Coba gerakkan pemain ke arah tertentu.
        Kembalikan True jika berhasil bergerak.
        direction: 'top' | 'bottom' | 'left' | 'right'
        """
        if self.state != State.PLAYING:
            return False

        r, c  = self.player.pos
        cell  = self.maze.get(r, c)

        if not cell.can_go(direction):
            return False   # ada dinding

        dr, dc = Cell.DIRS[direction]
        nr, nc = r + dr, c + dc

        if self.maze.get(nr, nc) is None:
            return False   # di luar grid

        self.player.move_to(nr, nc)
        self.trail.add((nr, nc))

        # Cek menang
        if self.player.pos == self.end_pos:
            self.elapsed = time.time() - self._start_time
            self.state   = State.WIN

        return True

    def toggle_hint(self):
        """
        Aktifkan / matikan hint Dijkstra.
        Saat diaktifkan, hitung jalur terpendek dari posisi pemain ke END.
        """
        if self.hint_active:
            self.hint_active  = False
            self.hint_path    = []
            self.hint_visited = set()
        else:
            path, visited = dijkstra(
                self.maze,
                self.player.pos,
                self.end_pos,
            )
            self.hint_path    = path
            self.hint_visited = visited
            self.hint_active  = True
            self.optimal_steps = len(path) - 1 if path else 0

    # ── TICK ───────────────────────────────────────────────────────────

    def tick(self):
        """Panggil setiap frame untuk update timer."""
        if self.state == State.PLAYING:
            self.elapsed = time.time() - self._start_time

        # Invalidasi hint jika pemain bergerak (path berubah)
        # (hint di-reset saat move() dipanggil dengan mematikannya otomatis
        #  agar pemain harus tekan H lagi — membuat hint terasa "aktif pakai")

    # ── PROPERTIES ─────────────────────────────────────────────────────

    @property
    def steps(self) -> int:
        return self.player.steps

    @property
    def player_pos(self) -> tuple[int, int]:
        return self.player.pos
