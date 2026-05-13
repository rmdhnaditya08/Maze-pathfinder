"""
core/player.py
State pemain: posisi, langkah, dan riwayat gerakan.
"""


class Player:
    """
    Menyimpan posisi pemain saat ini dan jumlah langkah.
    """

    def __init__(self, start_row: int = 0, start_col: int = 0):
        self.row = start_row
        self.col = start_col
        self.steps = 0
        self.history: list[tuple[int, int]] = [(start_row, start_col)]

    def move_to(self, row: int, col: int):
        self.row = row
        self.col = col
        self.steps += 1
        self.history.append((row, col))

    def reset(self, row: int = 0, col: int = 0):
        self.row = row
        self.col = col
        self.steps = 0
        self.history = [(row, col)]

    @property
    def pos(self) -> tuple[int, int]:
        return (self.row, self.col)

    def __repr__(self):
        return f"Player(pos={self.pos}, steps={self.steps})"
