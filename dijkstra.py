"""
algorithms/dijkstra.py

Algoritma Dijkstra untuk mencari jalur terpendek dalam maze.

Cara kerja:
  - Gunakan Priority Queue (min-heap) untuk selalu mengekspansi
    node dengan jarak terkecil terlebih dahulu.
  - Karena semua edge berbobot 1 (satu langkah), Dijkstra identik
    dengan BFS di sini — namun tetap menggunakan heap agar implementasi
    sesuai definisi Dijkstra yang sesungguhnya.
  - Lacak parent setiap node untuk rekonstruksi jalur.

Kompleksitas:
  - Waktu  : O((V + E) log V)  → V = jumlah sel, E = jumlah edge
  - Ruang  : O(V)
"""

import heapq
from maze import Maze


def dijkstra(
    maze: Maze,
    start: tuple[int, int],
    end: tuple[int, int],
) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
    """
    Jalankan Dijkstra dari `start` ke `end` pada `maze`.

    Returns
    -------
    path    : list of (row, col) dari start → end (inklusif).
              List kosong jika tidak ada jalur.
    visited : set semua sel yang pernah di-explore (untuk visualisasi).
    """
    dist: dict[tuple, int] = {start: 0}
    parent: dict[tuple, tuple | None] = {start: None}
    visited: set[tuple[int, int]] = set()

    # heap entry: (distance, row, col)
    heap: list[tuple[int, int, int]] = [(0, start[0], start[1])]

    while heap:
        d, r, c = heapq.heappop(heap)
        curr = (r, c)

        if curr in visited:
            continue
        visited.add(curr)

        # Tujuan tercapai → rekonstruksi jalur
        if curr == end:
            return _reconstruct(parent, end), visited

        for nr, nc in maze.neighbors_open(r, c):
            nb = (nr, nc)
            new_dist = d + 1  # semua edge berbobot 1
            if nb not in dist or new_dist < dist[nb]:
                dist[nb] = new_dist
                parent[nb] = curr
                heapq.heappush(heap, (new_dist, nr, nc))

    return [], visited  # tidak ada jalur


def _reconstruct(
    parent: dict[tuple, tuple | None],
    end: tuple[int, int],
) -> list[tuple[int, int]]:
    """Telusuri balik parent dict untuk mendapat jalur dari start ke end."""
    path = []
    node: tuple | None = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path
