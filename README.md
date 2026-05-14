# Maze Pathfinder

|    NRP     |      Name      |
| :--------: | :------------: |
| 5025241053 | Ary Pasya Fernanda |
| 5025241129 | Mochamad Ramadhan Aditya Rachaman |
| 5025241147 | Lucky Himawan Prasetya |

> Maze generator dan pathfinder interaktif berbasis Pygame dengan visualisasi algoritma Dijkstra secara real-time.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green?style=flat-square&logo=python)
![Algorithm](https://img.shields.io/badge/Algorithm-Dijkstra-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## Tentang Proyek

**Maze Pathfinder** adalah aplikasi game edukatif yang menggabungkan gameplay eksplorasi labirin dengan visualisasi algoritma pathfinding. Pemain menavigasi maze yang dihasilkan secara prosedural, sementara fitur hint menampilkan cara kerja algoritma **Dijkstra** secara langsung — sel mana yang dieksplorasi, dan jalur terpendek yang ditemukan.

Proyek ini cocok untuk:
- Pemula yang ingin memahami **algoritma graph** secara visual
- Developer yang belajar **Pygame** dan struktur game sederhana
- Demonstrasi **DFS maze generation** dan **Dijkstra pathfinding**

---

## Fitur

| Fitur | Deskripsi |
|---|---|
|  **Maze Prosedural** | Maze unik setiap sesi menggunakan DFS Recursive Backtracker |
|  **Hint Dijkstra** | Visualisasi real-time jalur optimal & sel yang dieksplorasi |
|  **Statistik Live** | Langkah, waktu, dan efisiensi rute pemain |
|  **6 Level** | Maze membesar setiap level (11×11 hingga 35×35) |
|  **Trail Pemain** | Jejak pergerakan pemain ditampilkan di grid |
|  **Win Screen** | Ringkasan performa dengan perbandingan jalur optimal |
|  **Dual Input** | Mendukung Arrow Keys dan WASD |
|  **Web-Ready** | Kompatibel dengan Pygbag untuk deployment berbasis browser |

---

## Screenshot

<img width="527" height="683" alt="screenshot-2026-05-14_17 49 24" src="https://github.com/user-attachments/assets/c1b0a96f-3ed8-442e-9c5a-2cb956d70a72" />

**Keterangan warna:**

| Warna | Elemen |
|---|---|
| 🟢 Hijau Neon | Posisi START |
| 🟠 Oranye | Posisi END (tujuan) |
| 🔵 Cyan Terang | Posisi pemain saat ini |
| 🟦 Biru Gelap | Jejak (trail) pergerakan |
| 💙 Biru Cerah | Jalur hint optimal Dijkstra |
| 🟣 Ungu Gelap | Sel yang dieksplorasi Dijkstra |

---

## Arsitektur Proyek

```
maze-pathfinder/
│
├── main.py             # Entry point — game loop utama (async/Pygbag-ready)
│
├── core/
│   ├── cell.py         # Representasi satu sel grid (dinding & koneksi)
│   ├── maze.py         # Grid maze + DFS generator
│   ├── player.py       # State pemain (posisi, langkah, riwayat)
│   └── game_state.py   # State machine: PLAYING → WIN, logika gerak & hint
│
├── algorithms/
│   └── dijkstra.py     # Algoritma Dijkstra (pathfinding + rekonstruksi jalur)
│
├── visualization/
│   ├── renderer.py     # Semua operasi drawing via Pygame
│   ├── ui.py           # Komponen UI: Button, Toast notification
│   └── colors.py       # Konstanta warna RGB
│
└── requirements.txt    # Dependensi Python
```

**Pola desain yang digunakan:**
- **State Machine** — `GameState` mengelola transisi `PLAYING → WIN`
- **Separation of Concerns** — logika, rendering, dan algoritma dipisah
- **Lazy Evaluation** — hint Dijkstra hanya dihitung saat pengguna memintanya

---

## Penjelasan Kode

### `cell.py` — Representasi Sel

Setiap sel di grid maze memiliki 4 dinding (atas, kanan, bawah, kiri). Dinding bernilai `True` berarti tertutup, `False` berarti terbuka (jalan dapat dilalui).

```python
class Cell:
    DIRS = {
        "top":    (-1,  0),
        "bottom": ( 1,  0),
        "left":   ( 0, -1),
        "right":  ( 0,  1),
    }
```

Method `open_neighbors()` mengembalikan daftar tetangga yang dapat diakses — digunakan oleh Dijkstra saat traversal graf.

---

### `maze.py` — Generator DFS Recursive Backtracker

Maze dibuat menggunakan **DFS iteratif dengan stack**. Algoritma ini menjamin setiap maze adalah *perfect maze* (selalu ada tepat satu jalur antara dua titik mana pun).

```python
def _generate(self):
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        r, c = stack[-1]
        unvisited = [tetangga yang belum dikunjungi]
        if unvisited:
            pilih acak → buka dinding → push ke stack
        else:
            stack.pop()  # backtrack
```

**Kompleksitas:** O(rows × cols) — setiap sel dikunjungi tepat satu kali.

---

### `dijkstra.py` — Pathfinding dengan Priority Queue

Implementasi Dijkstra menggunakan `heapq` (min-heap). Karena setiap langkah berbobot sama (1), Dijkstra identik dengan BFS di sini, namun tetap menggunakan heap sesuai definisi algoritma aslinya.

```python
def dijkstra(maze, start, end):
    heap = [(0, start_row, start_col)]   # (jarak, r, c)
    while heap:
        d, r, c = heapq.heappop(heap)
        for nr, nc in maze.neighbors_open(r, c):
            if new_dist < dist.get(nb, ∞):
                dist[nb] = new_dist
                heapq.heappush(heap, (new_dist, nr, nc))
```

Fungsi ini mengembalikan dua nilai:
- `path` — list koordinat dari START ke END (jalur terpendek)
- `visited` — semua sel yang dieksplorasi (untuk visualisasi ungu)

**Kompleksitas:** O((V + E) log V) — V = jumlah sel, E = jumlah edge terbuka.

---

### `game_state.py` — Logika & State Machine

`GameState` adalah inti game. Ia menyatukan maze, pemain, hint, dan timer.

```python
class State(Enum):
    PLAYING = auto()
    WIN     = auto()

class GameState:
    LEVEL_SIZES = [11, 15, 19, 23, 29, 35]  # ukuran maze per level
```

Metode penting:
- `move(direction)` — validasi dinding, gerakkan pemain, cek kemenangan
- `toggle_hint()` — jalankan/matikan Dijkstra dari posisi saat ini
- `tick()` — update timer setiap frame

---

### `renderer.py` — Rendering Berlapis

Drawing dilakukan dalam urutan layer agar elemen tidak saling menimpa:

```
Layer 1: Background sel (passage / trail / hint)
Layer 2: Hint visited (ungu — sel dieksplorasi Dijkstra)
Layer 3: Trail pemain (biru gelap)
Layer 4: Hint path highlight (cyan transparan via SRCALPHA)
Layer 5: Garis dinding
Layer 6: Marker START & END
Layer 7: Lingkaran pemain + efek glow
Layer 8: Panel UI kanan
Layer 9: Win screen overlay (jika menang)
Layer 10: Toast notification
```

---

### `ui.py` — Komponen UI

- **`Button`** — tombol klikabel dengan efek hover, mendukung state disabled
- **`Toast`** — notifikasi sementara (2.5 detik) dengan fade-out animasi di 0.5 detik terakhir

---

### `colors.py` — Sistem Warna

Semua warna didefinisikan sebagai konstanta RGB terpusat agar mudah diganti tanpa mengubah kode rendering.

```python
BG_DARK       = (  8,  18,  28)   # latar belakang gelap
PLAYER_COLOR  = (  0, 220, 255)   # cyan terang untuk pemain
HINT_VISITED  = ( 80,  20, 150)   # ungu untuk sel Dijkstra
```

---

## Cara Menjalankan

### Prasyarat

- **Python 3.10** atau lebih baru
- **pip** (package manager Python)

### Instalasi

**1. Clone repositori**

```bash
git clone https://github.com/username/maze-pathfinder.git
cd maze-pathfinder
```

**2. (Opsional) Buat virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependensi**

```bash
pip install -r requirements.txt
```

**4. Jalankan aplikasi**

```bash
python main.py
```

### Menjalankan di Browser (via Pygbag)

Proyek ini sudah kompatibel dengan **Pygbag** untuk deployment web:

```bash
pip install pygbag
pygbag main.py
```

Buka `http://localhost:8000` di browser setelah build selesai.

---

## ⌨️ Kontrol

| Tombol | Fungsi |
|---|---|
| `↑` `↓` `←` `→` | Gerakkan pemain |
| `W` `A` `S` `D` | Gerakkan pemain (alternatif) |
| `H` | Aktifkan / matikan hint Dijkstra |
| `R` | Restart dari posisi awal (maze sama) |
| `N` | Buat maze baru (level sama) / lanjut ke level berikutnya (saat menang) |
| `ESC` | Keluar dari aplikasi |

---

## Algoritma

### DFS Recursive Backtracker (Maze Generation)

Menghasilkan *perfect maze* — labirin di mana setiap dua sel memiliki tepat satu jalur unik. Sifat ini memastikan maze selalu memiliki solusi dan tidak ada sel yang terisolasi.

```
Mulai di (0,0)
  → Pilih tetangga belum dikunjungi secara acak
  → Hapus dinding di antara keduanya
  → Pindah ke tetangga tersebut
  → Jika tidak ada tetangga → backtrack
  → Ulangi sampai semua sel dikunjungi
```

### Dijkstra (Pathfinding)

Menemukan jalur terpendek dari posisi pemain ke tujuan. Karena semua edge berbobot 1, jumlah langkah minimal sama dengan jarak BFS, namun implementasi heap dipertahankan untuk keakuratan representasi algoritma.

Hint menampilkan dua informasi sekaligus:
- **Sel ungu** — sel yang "dilihat" algoritma (explored)
- **Sel biru cerah** — jalur terpendek yang ditemukan (optimal path)

---

## Level & Progression

| Level | Ukuran Maze | Jumlah Sel |
|---|---|---|
| 1 | 11 × 11 | 121 |
| 2 | 15 × 15 | 225 |
| 3 | 19 × 19 | 361 |
| 4 | 23 × 23 | 529 |
| 5 | 29 × 29 | 841 |
| 6+ | 35 × 35 | 1.225 |

Setiap level baru menghasilkan maze yang lebih besar dan kompleks. Setelah level 6, ukuran tetap di 35×35 dengan layout yang selalu berbeda.

---

## Roadmap

- [ ] Tambahkan algoritma A* sebagai alternatif hint
- [ ] Mode timer dengan leaderboard lokal
- [ ] Animasi pemain (sprite movement)
- [ ] Tema warna yang dapat dipilih (dark / light / retro)
- [ ] Ekspor maze ke format gambar PNG
- [ ] Multiplayer lokal (layar terpisah)

---

## Kontribusi

Kontribusi sangat disambut! Silakan buka *issue* untuk melaporkan bug atau mengusulkan fitur baru, lalu kirim *pull request* dengan deskripsi perubahan yang jelas.

---
