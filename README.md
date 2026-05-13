# 🧩 Maze Pathfinder

> **Design & Analysis of Algorithms** — Group Project  
> Game maze interaktif dengan implementasi algoritma **Dijkstra** sebagai fitur hint jalur terpendek.

---

## 📁 Struktur Direktori

```
nawasena_maze/
├── main.py                      ← Entry point (jalankan ini)
├── requirements.txt
│
├── core/
│   ├── __init__.py
│   ├── cell.py                  ← Representasi sel maze
│   ├── maze.py                  ← Grid maze + generator (DFS Backtracker)
│   ├── player.py                ← State pemain
│   └── game_state.py            ← State machine + logika game
│
├── algorithms/
│   ├── __init__.py
│   └── dijkstra.py              ← Algoritma Dijkstra (pathfinding hint)
│
└── visualization/
    ├── __init__.py
    ├── colors.py                ← Konstanta warna
    ├── renderer.py              ← Semua operasi drawing pygame
    └── ui.py                   ← Komponen UI (Button, Toast)
```

---

## 🚀 Cara Menjalankan

```bash
# 1. Install dependensi
pip install -r requirements.txt

# 2. Jalankan game
python main.py
```

---

## 🎮 Cara Bermain

| Tombol         | Aksi                                        |
|----------------|---------------------------------------------|
| `↑ ↓ ← →`     | Gerakkan pemain                             |
| `W A S D`      | Gerakkan pemain (alternatif)                |
| `H`            | Aktifkan / matikan **hint Dijkstra**        |
| `R`            | Restart dari posisi awal (maze sama)        |
| `N`            | Buat maze baru (level sama / next level)    |
| `ESC`          | Keluar                                      |

**Tujuan:** Gerakkan karakter (lingkaran cyan) dari **START** (kiri atas, hijau) ke **END** (kanan bawah, oranye).

---

## 🧠 Algoritma yang Diimplementasi

### 1. DFS Recursive Backtracker — *Maze Generator*

Dipakai untuk **membuat maze** yang selalu memiliki solusi unik:

```
1. Mulai dari sel (0,0), tandai sebagai dikunjungi
2. Pilih acak tetangga yang belum dikunjungi
3. Hapus dinding antara sel saat ini dan tetangga terpilih
4. Lanjutkan rekursif ke tetangga tersebut
5. Backtrack jika tidak ada tetangga yang belum dikunjungi
```

- Kompleksitas: **O(rows × cols)**
- Hasilnya: *perfect maze* — setiap sel terhubung, satu solusi unik

### 2. Dijkstra — *Hint / Solver*

Dipakai sebagai **fitur hint** (tekan `H`) untuk menampilkan jalur terpendek dari posisi pemain saat ini ke END:

```
1. Inisialisasi dist[start] = 0, semua lain = ∞
2. Masukkan (0, start) ke priority queue (min-heap)
3. Selama heap tidak kosong:
   a. Ambil node dengan dist terkecil
   b. Jika node = END → rekonstruksi jalur via parent dict
   c. Untuk setiap tetangga yang bisa diakses:
      - Hitung dist_baru = dist[curr] + 1
      - Jika dist_baru < dist[tetangga] → update dan push ke heap
```

- Kompleksitas: **O((V + E) log V)**  
  V = jumlah sel, E = jumlah edge (jalan terbuka)
- Garansi: selalu menemukan **jalur terpendek**

---

## 📊 Fitur Game

- **6 Level** dengan maze yang semakin besar (11×11 → 35×35)
- **Hint interaktif** — Dijkstra dihitung ulang setiap pemain bergerak saat hint aktif
- **Statistik real-time** — jumlah langkah, waktu, efisiensi vs jalur optimal
- **Trail visual** — jejak pergerakan pemain ditampilkan
- **Win screen** — menampilkan perbandingan langkah pemain vs optimal Dijkstra

---

## 👥 Kelompok Nawasena 2026

> *(isi nama anggota kelompok)*

---

## 📚 Referensi

- Cormen, T. H., et al. *Introduction to Algorithms* (CLRS), 4th Ed.
- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs." *Numerische Mathematik*.
- Maze generation: Jamis Buck, *Maze Generation: Recursive Backtracking* (2010)
