"""
visualization/renderer.py
Semua fungsi menggambar: maze, player, hint, UI panel.
"""

import pygame
from colors import *


class Renderer:
    """
    Bertanggung jawab untuk semua operasi drawing ke screen pygame.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        maze_rows: int,
        maze_cols: int,
        cell_size: int,
        offset_x: int = 0,
        offset_y: int = 0,
    ):
        self.screen     = screen
        self.rows       = maze_rows
        self.cols       = maze_cols
        self.cell       = cell_size
        self.ox         = offset_x   # offset X area maze
        self.oy         = offset_y   # offset Y area maze
        self._font_cache: dict[int, pygame.font.Font] = {}

    # ── FONTS ──────────────────────────────────────────────────────────

    def font(self, size: int) -> pygame.font.Font:
        if size not in self._font_cache:
            try:
                self._font_cache[size] = pygame.font.SysFont("consolas", size)
            except Exception:
                self._font_cache[size] = pygame.font.Font(None, size)
        return self._font_cache[size]

    # ── MAZE ───────────────────────────────────────────────────────────

    def draw_background(self):
        self.screen.fill(BG_DARK)

    def draw_maze(self, maze, trail: set = None, hint_path: list = None,
                  hint_visited: set = None):
        """
        Gambar seluruh grid maze:
          Layer 1: background sel
          Layer 2: hint (visited Dijkstra) — ungu
          Layer 3: trail pemain — biru gelap
          Layer 4: hint path — cyan transparan
          Layer 5: dinding
        """
        trail        = trail        or set()
        hint_path    = hint_path    or []
        hint_visited = hint_visited or set()
        hint_set     = set(hint_path)

        wall_w = max(2, self.cell // 8)

        for r in range(self.rows):
            for c in range(self.cols):
                x = self.ox + c * self.cell
                y = self.oy + r * self.cell
                pos = (r, c)

                # ── Isi sel ──
                if pos in hint_set:
                    color = (0, 50, 100)
                elif pos in trail:
                    color = TRAIL_COLOR
                elif pos in hint_visited:
                    color = (40, 10, 70)
                else:
                    color = PASSAGE_COLOR

                pygame.draw.rect(self.screen, color,
                                 (x, y, self.cell, self.cell))

                # ── Highlight hint path ──
                if pos in hint_set:
                    s = pygame.Surface((self.cell, self.cell), pygame.SRCALPHA)
                    s.fill((0, 180, 255, 55))
                    self.screen.blit(s, (x, y))

                # ── Dinding ──
                cell = maze.get(r, c)
                if cell.walls["top"]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x, y), (x + self.cell, y), wall_w)
                if cell.walls["right"]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x + self.cell, y),
                                     (x + self.cell, y + self.cell), wall_w)
                if cell.walls["bottom"]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x, y + self.cell),
                                     (x + self.cell, y + self.cell), wall_w)
                if cell.walls["left"]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x, y), (x, y + self.cell), wall_w)

        # Border luar maze
        pygame.draw.rect(self.screen, WALL_COLOR,
                         (self.ox, self.oy,
                          self.cols * self.cell,
                          self.rows * self.cell), wall_w)

    # ── MARKERS ────────────────────────────────────────────────────────

    def draw_markers(self, start: tuple, end: tuple):
        """Gambar START (hijau) dan END (oranye)."""
        self._draw_marker(start[0], start[1], START_COLOR, "S")
        self._draw_marker(end[0],   end[1],   END_COLOR,   "E")

    def _draw_marker(self, r: int, c: int, color: tuple, label: str):
        x = self.ox + c * self.cell
        y = self.oy + r * self.cell
        pad = max(3, self.cell // 5)
        rect = (x + pad, y + pad, self.cell - pad * 2, self.cell - pad * 2)
        pygame.draw.rect(self.screen, color, rect, border_radius=3)
        if self.cell >= 16:
            txt = self.font(max(10, self.cell // 2)).render(label, True, BLACK)
            tx = x + (self.cell - txt.get_width())  // 2
            ty = y + (self.cell - txt.get_height()) // 2
            self.screen.blit(txt, (tx, ty))

    # ── PLAYER ─────────────────────────────────────────────────────────

    def draw_player(self, row: int, col: int):
        x = self.ox + col * self.cell + self.cell // 2
        y = self.oy + row * self.cell + self.cell // 2
        r = max(4, self.cell // 2 - 3)

        # Glow
        glow_surf = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*PLAYER_GLOW, 80), (r * 2, r * 2), r * 2)
        self.screen.blit(glow_surf, (x - r * 2, y - r * 2))

        # Lingkaran player
        pygame.draw.circle(self.screen, PLAYER_COLOR, (x, y), r)
        pygame.draw.circle(self.screen, WHITE, (x, y), r, 2)

    # ── UI PANEL (kanan) ───────────────────────────────────────────────

    def draw_ui_panel(self, panel_rect: pygame.Rect, maze_size: int,
                      steps: int, hint_active: bool, hint_steps: int,
                      level: int, elapsed: float):
        """Gambar panel info di sisi kanan."""
        px, py, pw, ph = panel_rect

        # Background panel
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        pygame.draw.rect(self.screen, UI_BORDER, panel_rect, 1)

        y = py + 14
        pad = 14

        # ── Judul ──
        self._text("Maze Pathfinder", px + pad, y,
                   self.font(14), UI_ACCENT, bold=True)
        y += 20
       
        self._hline(px + pad, y, pw - pad * 2)
        y += 12

        # ── Info game ──
        self._label_val("LEVEL",    str(level),           px, y, pw, pad)
        y += 22
        self._label_val("MAZE",     f"{maze_size}×{maze_size}", px, y, pw, pad)
        y += 22
        self._label_val("LANGKAH",  str(steps),           px, y, pw, pad)
        y += 22
        self._label_val("WAKTU",    f"{elapsed:.0f}s",    px, y, pw, pad)
        y += 28

        self._hline(px + pad, y, pw - pad * 2)
        y += 12

        # ── Hint info ──
        self._text("[ DIJKSTRA HINT ]", px + pad, y, self.font(10), UI_ACCENT)
        y += 18

        if hint_active:
            self._text("✓ Hint aktif", px + pad, y, self.font(10), UI_SUCCESS)
            y += 16
            self._text(f"Jalur optimal: {hint_steps} langkah",
                       px + pad, y, self.font(10), UI_WARNING)
        else:
            self._text("Tekan  H  untuk hint", px + pad, y,
                       self.font(10), UI_DIM)
        y += 28

        self._hline(px + pad, y, pw - pad * 2)
        y += 12

        # ── Kontrol ──
        self._text("[ KONTROL ]", px + pad, y, self.font(10), UI_ACCENT)
        y += 18
        controls = [
            ("↑ ↓ ← →", "Gerak"),
            ("WASD",     "Gerak"),
            ("H",        "Hint"),
            ("R",        "Restart"),
            ("N",        "Maze baru"),
            ("ESC",      "Keluar"),
        ]
        for key, desc in controls:
            self._text(f"{key:<6} {desc}", px + pad, y, self.font(10), UI_DIM)
            y += 16

        y += 6
        self._hline(px + pad, y, pw - pad * 2)
        y += 12

        # ── Legend ──
        self._text("[ LEGENDA ]", px + pad, y, self.font(10), UI_ACCENT)
        y += 18
        legends = [
            (START_COLOR,   "START"),
            (END_COLOR,     "END"),
            (PLAYER_COLOR,  "PEMAIN"),
            (TRAIL_COLOR,   "JEJAK"),
            ((0, 50, 100),  "HINT PATH"),
            ((40, 10, 70),  "EXPLORED"),
        ]
        for color, label in legends:
            pygame.draw.rect(self.screen, color,
                             (px + pad, y, 10, 10), border_radius=2)
            self._text(label, px + pad + 16, y, self.font(10), UI_DIM)
            y += 16

    # ── WIN SCREEN ─────────────────────────────────────────────────────

    def draw_win_screen(self, screen_w: int, screen_h: int,
                        steps: int, optimal: int, elapsed: float):
        """Overlay transparan saat pemain menang."""
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 10, 25, 210))
        self.screen.blit(overlay, (0, 0))

        cx = screen_w // 2

        # Judul
        self._text_center("🏆  SELESAI!", cx, screen_h // 2 - 100,
                           self.font(36), WIN_TITLE)
        self._text_center("Maze berhasil diselesaikan",
                          cx, screen_h // 2 - 58,
                          self.font(14), WIN_SUBTITLE)

        # Statistik
        eff = f"{(optimal / steps * 100):.0f}%" if steps > 0 else "-"
        stats = [
            ("Langkah kamu",  str(steps)),
            ("Jalur optimal", str(optimal)),
            ("Efisiensi",     eff),
            ("Waktu",         f"{elapsed:.1f} detik"),
        ]
        sy = screen_h // 2 - 20
        for label, val in stats:
            self._text_center(f"{label:<18} {val:>6}",
                              cx, sy, self.font(13), UI_TEXT)
            sy += 22

        self._text_center("Tekan  N  untuk maze baru  |  R  untuk restart",
                          cx, sy + 16, self.font(11), UI_DIM)

    # ── HELPERS ────────────────────────────────────────────────────────

    def _text(self, txt: str, x: int, y: int,
              font: pygame.font.Font, color: tuple, bold: bool = False):
        surf = font.render(txt, True, color)
        self.screen.blit(surf, (x, y))

    def _text_center(self, txt: str, cx: int, y: int,
                     font: pygame.font.Font, color: tuple):
        surf = font.render(txt, True, color)
        self.screen.blit(surf, (cx - surf.get_width() // 2, y))

    def _hline(self, x: int, y: int, w: int):
        pygame.draw.line(self.screen, UI_BORDER,
                         (x, y), (x + w, y), 1)

    def _label_val(self, label: str, val: str,
                   px: int, y: int, pw: int, pad: int):
        self._text(label, px + pad, y, self.font(10), UI_DIM)
        val_surf = self.font(11).render(val, True, UI_ACCENT)
        self.screen.blit(val_surf,
                         (px + pw - pad - val_surf.get_width(), y))

    def cell_rect(self, row: int, col: int) -> pygame.Rect:
        """Kembalikan pygame.Rect untuk sel (row, col)."""
        return pygame.Rect(
            self.ox + col * self.cell,
            self.oy + row * self.cell,
            self.cell, self.cell
        )
