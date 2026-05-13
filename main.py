"""
main.py - Modified for Web/Azure Deployment
Entry point game Maze Pathfinder.
"""

import sys
import os
import asyncio  # Penambahan untuk dukungan Web/Pygbag

# Pastikan root project ada di sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from game_state         import GameState, State
from renderer  import Renderer
from ui        import Toast
from colors    import *

# ── KONSTANTA LAYOUT ───────────────────────────────────────────────────────────

PANEL_W    = 200        
MIN_CELL   = 14         
MAX_CELL   = 28         

SCREEN_H   = 700
FPS        = 60

# ── KEY MAP ────────────────────────────────────────────────────────────────────

KEY_DIR = {
    pygame.K_UP:    "top",
    pygame.K_w:     "top",
    pygame.K_DOWN:  "bottom",
    pygame.K_s:     "bottom",
    pygame.K_LEFT:  "left",
    pygame.K_a:     "left",
    pygame.K_RIGHT: "right",
    pygame.K_d:     "right",
}

# ── FUNGSI HITUNG LAYOUT ───────────────────────────────────────────────────────

def compute_layout(maze_size: int) -> tuple[int, int, int, int]:
    available_w = SCREEN_H - PANEL_W - 20   
    cell = max(MIN_CELL, min(MAX_CELL, available_w // maze_size))
    maze_px   = maze_size * cell
    screen_w  = maze_px + PANEL_W + 30      
    offset_x  = 10
    offset_y  = (SCREEN_H - maze_px) // 2
    offset_y  = max(10, offset_y)
    return cell, screen_w, offset_x, offset_y

# ── MAIN (ASYNC VERSION) ───────────────────────────────────────────────────────

async def main(): # Diubah menjadi async
    pygame.init()
    pygame.display.set_caption("Maze Pathfinder")

    game  = GameState()
    toast = Toast()

    cell, screen_w, ox, oy = compute_layout(game.maze_size)
    screen = pygame.display.set_mode((screen_w, SCREEN_H))

    renderer = Renderer(
        screen, game.maze_size, game.maze_size,
        cell, offset_x=ox, offset_y=oy
    )

    clock = pygame.time.Clock()

    def rebuild():
        nonlocal cell, screen_w, ox, oy, screen, renderer
        cell, screen_w, ox, oy = compute_layout(game.maze_size)
        screen = pygame.display.set_mode((screen_w, SCREEN_H))
        pygame.display.set_caption("Maze Pathfinder")
        renderer = Renderer(
            screen, game.maze_size, game.maze_size,
            cell, offset_x=ox, offset_y=oy
        )

    toast.show("Gunakan panah / WASD untuk bergerak  |  H = Hint Dijkstra",
               UI_DIM)

    running = True
    while running:
        # PENTING bagi Pygbag: Memberikan waktu bagi browser untuk memproses tugas lain
        await asyncio.sleep(0) 
        
        clock.tick(FPS)
        game.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_DIR and game.state == State.PLAYING:
                    moved = game.move(KEY_DIR[event.key])
                    if moved and game.hint_active:
                        game.toggle_hint()   
                        game.toggle_hint()   

                elif event.key == pygame.K_h:
                    if game.state == State.PLAYING:
                        game.toggle_hint()
                        if game.hint_active:
                            toast.show(
                                f"Dijkstra: jalur optimal {game.optimal_steps} langkah",
                                UI_ACCENT
                            )
                        else:
                            toast.show("Hint dimatikan", UI_DIM)

                elif event.key == pygame.K_r:
                    game.restart()
                    toast.show("Restart!", UI_WARNING)

                elif event.key == pygame.K_n:
                    if game.state == State.WIN:
                        game.next_level()
                        rebuild()
                        toast.show(
                            f"Level {game.level} — Maze {game.maze_size}×{game.maze_size}",
                            UI_SUCCESS
                        )
                    else:
                        game.new_maze()
                        toast.show("Maze baru dibuat!", UI_ACCENT)

                elif event.key == pygame.K_ESCAPE:
                    running = False

        # ── Drawing ──
        renderer.draw_background()

        renderer.draw_maze(
            maze         = game.maze,
            trail        = game.trail,
            hint_path    = game.hint_path    if game.hint_active else [],
            hint_visited = game.hint_visited if game.hint_active else set(),
        )

        renderer.draw_markers((0, 0), game.end_pos)
        renderer.draw_player(*game.player_pos)

        maze_px    = game.maze_size * cell
        panel_x    = ox + maze_px + 10
        panel_rect = pygame.Rect(panel_x, 10, PANEL_W - 10, SCREEN_H - 20)

        renderer.draw_ui_panel(
            panel_rect   = panel_rect,
            maze_size    = game.maze_size,
            steps        = game.steps,
            hint_active  = game.hint_active,
            hint_steps   = game.optimal_steps,
            level        = game.level,
            elapsed      = game.elapsed,
        )

        if game.state == State.WIN:
            renderer.draw_win_screen(
                screen_w = screen_w,
                screen_h = SCREEN_H,
                steps    = game.steps,
                optimal  = game.optimal_steps if game.optimal_steps else game.steps,
                elapsed  = game.elapsed,
            )

        toast.draw(screen)
        pygame.display.flip()

    pygame.quit()
    # sys.exit() sebaiknya tidak digunakan di browser karena bisa mematikan environment WASM

if __name__ == "__main__":
    # Menjalankan loop async
    asyncio.run(main())