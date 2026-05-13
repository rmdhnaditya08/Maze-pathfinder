"""
visualization/colors.py
Semua konstanta warna dalam format RGB untuk pygame.
"""

# ── Background & struktur ──────────────────────────────────
BG_DARK        = (  8,  18,  28)   # latar belakang layar
PANEL_BG       = ( 12,  24,  40)   # panel UI kanan
WALL_COLOR     = ( 20,  60, 100)   # garis dinding maze
PASSAGE_COLOR  = ( 10,  25,  42)   # isi sel (jalan)
GRID_LINE      = ( 15,  35,  58)   # garis grid tipis

# ── Pemain ────────────────────────────────────────────────
PLAYER_COLOR   = (  0, 220, 255)   # cyan terang
PLAYER_GLOW    = (  0, 120, 180)   # efek glow player
TRAIL_COLOR    = ( 20,  60,  90)   # jejak gerakan player

# ── Marker Start / End ────────────────────────────────────
START_COLOR    = (  0, 255, 130)   # hijau neon
END_COLOR      = (255, 100,  40)   # oranye

# ── Dijkstra hint ─────────────────────────────────────────
HINT_PATH      = (  0, 180, 255)   # jalur hint (transparan)
HINT_VISITED   = ( 80,  20, 150)   # sel yang di-explore Dijkstra
HINT_ARROW     = (  0, 220, 255)   # warna panah hint

# ── UI ────────────────────────────────────────────────────
UI_BORDER      = ( 30,  80, 130)   # border panel
UI_TEXT        = (180, 220, 255)   # teks biasa
UI_DIM         = ( 70, 110, 150)   # teks redup
UI_ACCENT      = (  0, 212, 255)   # aksen cyan
UI_ACCENT2     = (255, 107,  53)   # aksen oranye
UI_SUCCESS     = (  0, 255, 130)   # teks sukses / hijau
UI_WARNING     = (255, 200,  40)   # kuning warning
UI_DANGER      = (255,  60,  80)   # merah

# ── Button states ─────────────────────────────────────────
BTN_NORMAL     = ( 15,  38,  65)
BTN_HOVER      = ( 20,  55,  95)
BTN_ACTIVE     = (  0,  80, 130)
BTN_DISABLED   = (  8,  22,  38)
BTN_TEXT       = (160, 210, 255)
BTN_TEXT_DIM   = ( 60,  90, 120)

# ── Win screen ────────────────────────────────────────────
WIN_OVERLAY    = (  0,  15,  30, 200)   # RGBA (dipakai surface alpha)
WIN_TITLE      = (  0, 255, 180)
WIN_SUBTITLE   = (160, 220, 255)

# ── Konstanta putih & hitam ───────────────────────────────
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
