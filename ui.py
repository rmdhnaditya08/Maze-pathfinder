"""
visualization/ui.py
Komponen UI ringan: Button, Toast notification, progress bar.
"""

import pygame
import time
from colors import *


class Button:
    """Tombol klikabel sederhana."""

    def __init__(self, rect: pygame.Rect, label: str,
                 color=BTN_NORMAL, hover_color=BTN_HOVER,
                 text_color=BTN_TEXT, font_size=12):
        self.rect        = rect
        self.label       = label
        self.color       = color
        self.hover_color = hover_color
        self.text_color  = text_color
        self.font_size   = font_size
        self.enabled     = True
        self._hovered    = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Kembalikan True jika tombol di-klik."""
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def draw(self, screen: pygame.Surface):
        font = pygame.font.SysFont("consolas", self.font_size)
        if not self.enabled:
            bg = BTN_DISABLED
            tc = BTN_TEXT_DIM
        elif self._hovered:
            bg = self.hover_color
            tc = WHITE
        else:
            bg = self.color
            tc = self.text_color

        pygame.draw.rect(screen, bg, self.rect, border_radius=4)
        pygame.draw.rect(screen, UI_BORDER, self.rect, 1, border_radius=4)

        txt = font.render(self.label, True, tc)
        tx  = self.rect.x + (self.rect.w - txt.get_width())  // 2
        ty  = self.rect.y + (self.rect.h - txt.get_height()) // 2
        screen.blit(txt, (tx, ty))


class Toast:
    """Pesan notifikasi sementara di pojok layar."""

    DURATION = 2.5   # detik

    def __init__(self):
        self._msg      = ""
        self._start    = 0.0
        self._active   = False
        self._color    = UI_ACCENT

    def show(self, msg: str, color=None):
        self._msg    = msg
        self._start  = time.time()
        self._active = True
        self._color  = color or UI_ACCENT

    def draw(self, screen: pygame.Surface):
        if not self._active:
            return
        elapsed = time.time() - self._start
        if elapsed > self.DURATION:
            self._active = False
            return

        # Fade out di 0.5 detik terakhir
        alpha = 255
        if elapsed > self.DURATION - 0.5:
            alpha = int(255 * (self.DURATION - elapsed) / 0.5)

        sw = screen.get_width()
        sh = screen.get_height()

        font = pygame.font.SysFont("consolas", 13)
        txt  = font.render(self._msg, True, self._color)
        tw, th = txt.get_width(), txt.get_height()
        pad = 12
        w, h = tw + pad * 2, th + pad

        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((10, 25, 45, alpha))
        pygame.draw.rect(surf, (*self._color, alpha), (0, 0, w, h), 1,
                         border_radius=4)
        surf.blit(txt, (pad, pad // 2))
        screen.blit(surf, (sw - w - 16, sh - h - 16))
