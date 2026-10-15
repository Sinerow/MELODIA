import csv
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

# ==========================================
# MELODIA | MAIN DASHBOARD
# ==========================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(ROOT_DIR, "lagu.csv")

FILE_TAMBAH = os.path.join(ROOT_DIR, "tambah_lagu.py")
FILE_KOLEKSI = os.path.join(ROOT_DIR, "tampil_buku.py")

KOLOM = ["judul", "penulis", "isbn", "status"]

# Palet warna MELODIA
BG = "#0B0B14"
PANEL = "#151525"
FIELD = "#202037"
PURPLE = "#A78BFA"
PINK = "#F472B6"
BLUE = "#60A5FA"
WHITE = "#F4F2FF"
MUTED = "#9292AE"
GREEN = "#6EE7B7"
RED = "#FB7185"


# ==========================================
# MANAJEMEN DATA
# ==========================================

def siapkan_csv():
    """Buat CSV dengan header jika file belum tersedia."""
    if not os.path.exists(FILE_CSV) or os.path.getsize(FILE_CSV) == 0:
        with open(
            FILE_CSV, "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(KOLOM)


def muat_data():
    """Baca data koleksi dengan validasi header."""
    siapkan_csv()

    with open(
        FILE_CSV, "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Header lagu.csv tidak ditemukan.")

        header = {
            str(k).strip().casefold()
            for k in reader.fieldnames
            if k
        }

        if not set(KOLOM).issubset(header):
            raise ValueError(
                "Header lagu.csv harus berisi:\n"
                "judul, penulis, isbn, status"
            )

        hasil = []

        for nomor, row in enumerate(reader, start=2):
            data = {
                str(k).strip().casefold(): str(v or "").strip()
                for k, v in row.items()
                if k is not None
            }

            if not any(data.values()):
                continue

            judul = data.get("judul", "")
            penulis = data.get("penulis", "")
            isbn = data.get("isbn", "")
            status = data.get("status", "Tersedia")

            if not judul or not penulis or not isbn:
                raise ValueError(
                    f"Data tidak lengkap pada baris {nomor}."
                )

            status_normal = status.casefold()

            if status_normal not in ("tersedia", "dipinjam"):
                raise ValueError(
                    f"Status tidak valid pada baris {nomor}: "
                    f"{status}"
                )

            hasil.append({
                "judul": judul,
                "penulis": penulis,
                "isbn": isbn,
                "status": (
                    "Tersedia"
                    if status_normal == "tersedia"
                    else "Dipinjam"
                )
            })

        return hasil


# ==========================================
# STATISTIK DASHBOARD
# ==========================================

def perbarui_statistik():
    try:
        data = muat_data()

        total = len(data)
        tersedia = sum(
            item["status"] == "Tersedia"
            for item in data
        )
        dipinjam = sum(
            item["status"] == "Dipinjam"
            for item in data
        )

        label_total.config(text=str(total))
        label_tersedia.config(text=str(tersedia))
        label_dipinjam.config(text=str(dipinjam))

        label_status.config(
            text="DATA TERSINKRONISASI",
            fg=GREEN
        )

    except (OSError, csv.Error, UnicodeError, ValueError) as error:
        label_total.config(text="—")
        label_tersedia.config(text="—")
        label_dipinjam.config(text="—")

        label_status.config(
            text="GAGAL MEMUAT DATA",
            fg=RED
        )

        messagebox.showerror(
            "Gagal memuat koleksi",
            f"Periksa file lagu.csv.\n\n{error}",
            parent=root
        )


# ==========================================
# NAVIGASI HALAMAN
# ==========================================

def buka_halaman(nama_file, judul):
    """Jalankan halaman lama sebagai proses terpisah.

    Cara ini mempertahankan kompatibilitas dengan halaman
    yang saat ini masih memiliki tk.Tk() dan mainloop sendiri.
    """
    lokasi = os.path.join(ROOT_DIR, nama_file)

    if not os.path.isfile(lokasi):
        messagebox.showerror(
            "File tidak ditemukan",
            f"File {nama_file} tidak ditemukan.\n\n"
            "Pastikan file berada di folder MELODIA.",
            parent=root
        )
        return

    try:
        subprocess.Popen(
            [sys.executable, lokasi],
            cwd=ROOT_DIR
        )

        label_aktivitas.config(
            text=f"Halaman dibuka: {judul}",
            fg=PURPLE
        )

        # Perbarui statistik ketika jendela utama aktif kembali.
        root.after(1000, perbarui_statistik)

    except OSError as error:
        messagebox.showerror(
            "Gagal membuka halaman",
            f"Tidak dapat membuka {judul}.\n\n{error}",
            parent=root
        )


def buka_tambah():
    buka_halaman("tambah_lagu.py", "Tambah Koleksi")


def buka_koleksi():
    buka_halaman("tampil_buku.py", "Koleksi Musik")


# ==========================================
# KOMPONEN UI
# ==========================================

def buat_stat(parent, judul, warna):
    panel = tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground="#292440",
        highlightthickness=1
    )

    angka = tk.Label(
        panel,
        text="0",
        font=("Segoe UI", 27, "bold"),
        bg=PANEL,
        fg=warna
    )
    angka.pack(anchor="w", padx=18, pady=(17, 0))

    tk.Label(
        panel,
        text=judul,
        font=("Segoe UI", 10),
        bg=PANEL,
        fg=MUTED
    ).pack(anchor="w", padx=19, pady=(2, 16))

    return panel, angka


def buat_tombol(parent, teks, perintah, warna, foreground=BG):
    tombol = tk.Button(
        parent,
        text=teks,
        command=perintah,
        bg=warna,
        fg=foreground,
        activebackground=PINK,
        activeforeground=BG,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=18,
        pady=13
    )

    tombol.bind(
        "<Enter>",
        lambda _event: tombol.config(
            bg=PINK if warna == PURPLE else "#33334A"
        )
    )
    tombol.bind(
        "<Leave>",
        lambda _event: tombol.config(bg=warna)
    )

    return tombol


# ==========================================
# JENDELA DASHBOARD
# ==========================================

root = tk.Tk()
root.title("Melodia | Music Library")
root.geometry("1000x720")
root.minsize(780, 620)
root.configure(bg=BG)

# Atur ikon dan font melalui tema native Tk.
try:
    root.tk.call("tk", "scaling", 1.1)
except tk.TclError:
    pass

# Header
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=38, pady=(28, 22))

brand = tk.Frame(header, bg=BG)
brand.pack(side="left")

tk.Label(
    brand,
    text="♫  MELODIA",
    font=("Segoe UI", 23, "bold"),
    bg=BG,
    fg=PURPLE
).pack(anchor="w")

tk.Label(
    brand,
    text="YOUR PERSONAL MUSIC & STORY LIBRARY",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(4, 0))

tk.Label(
    header,
    text="MAIN DASHBOARD",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=PINK
).pack(side="right", pady=12)

tk.Frame(
    root,
    bg="#292440",
    height=1
).pack(fill="x", padx=38, pady=(0, 27))

# Sambutan
tk.Label(
    root,
    text="Simpan cerita, nikmati musik.",
    font=("Segoe UI", 27, "bold"),
    bg=BG,
    fg=WHITE
).pack(anchor="w", padx=42)

tk.Label(
    root,
    text=(
        "Kelola koleksi dengan mudah dalam satu ruang "
        "digital yang terorganisasi."
    ),
    font=("Segoe UI", 11),
    bg=BG,
    fg=MUTED,
    wraplength=700,
    justify="left"
).pack(anchor="w", padx=44, pady=(7, 24))

# Statistik
tk.Label(
    root,
    text="RINGKASAN KOLEKSI",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=42, pady=(0, 12))

stats = tk.Frame(root, bg=BG)
stats.pack(fill="x", padx=37)

panel_total, label_total = buat_stat(
    stats, "Total Koleksi", PURPLE
)
panel_tersedia, label_tersedia = buat_stat(
    stats, "Tersedia", GREEN
)
panel_dipinjam, label_dipinjam = buat_stat(
    stats, "Sedang Dipinjam", PINK
)

for panel in (panel_total, panel_tersedia, panel_dipinjam):
    panel.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

# Navigasi
tk.Label(
    root,
    text="PENGELOLAAN PERPUSTAKAAN",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=42, pady=(29, 12))

menu = tk.Frame(root, bg=BG)
menu.pack(fill="x", padx=42)

# Kartu tambah
kartu_tambah = tk.Frame(
    menu,
    bg=PANEL,
    highlightbackground="#292440",
    highlightthickness=1
)
kartu_tambah.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)

tk.Label(
    kartu_tambah,
    text="＋",
    font=("Segoe UI", 27, "bold"),
    bg=PANEL,
    fg=PURPLE
).pack(anchor="w", padx=20, pady=(15, 0))

tk.Label(
    kartu_tambah,
    text="Tambah Koleksi",
    font=("Segoe UI", 14, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(anchor="w", padx=20, pady=(2, 5))

tk.Label(
    kartu_tambah,
    text="Tambahkan judul dan informasi koleksi baru.",
    font=("Segoe UI", 9),
    bg=PANEL,
    fg=MUTED,
    wraplength=300,
    justify="left"
).pack(anchor="w", padx=20, pady=(0, 15))

buat_tombol(
    kartu_tambah,
    "＋  TAMBAH DATA",
    buka_tambah,
    PURPLE
).pack(fill="x", padx=20, pady=(0, 20))

# Kartu koleksi
kartu_koleksi = tk.Frame(
    menu,
    bg=PANEL,
    highlightbackground="#292440",
    highlightthickness=1
)
kartu_koleksi.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(8, 0)
)

tk.Label(
    kartu_koleksi,
    text="☷",
    font=("Segoe UI", 27, "bold"),
    bg=PANEL,
    fg=BLUE
).pack(anchor="w", padx=20, pady=(15, 0))

tk.Label(
    kartu_koleksi,
    text="Jelajahi Koleksi",
    font=("Segoe UI", 14, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(anchor="w", padx=20, pady=(2, 5))

tk.Label(
    kartu_koleksi,
    text="Cari, filter, lihat detail, dan ekspor koleksi.",
    font=("Segoe UI", 9),
    bg=PANEL,
    fg=MUTED,
    wraplength=300,
    justify="left"
).pack(anchor="w", padx=20, pady=(0, 15))

buat_tombol(
    kartu_koleksi,
    "☷  LIHAT KOLEKSI",
    buka_koleksi,
    BLUE
).pack(fill="x", padx=20, pady=(0, 20))

# Status dan refresh
status_bar = tk.Frame(root, bg=BG)
status_bar.pack(fill="x", padx=42, pady=(24, 0))

label_status = tk.Label(
    status_bar,
    text="MEMUAT DATA...",
    font=("Segoe UI", 8, "bold"),
    bg=BG,
    fg=GREEN
)
label_status.pack(side="left")

buat_tombol(
    status_bar,
    "↻  REFRESH DATA",
    perbarui_statistik,
    FIELD,
    WHITE
).pack(side="right")

label_aktivitas = tk.Label(
    root,
    text="MELODIA  •  SIMPAN MUSIK, SIMPAN CERITA",
    font=("Segoe UI", 8, "bold"),
    bg=BG,
    fg=MUTED
)
label_aktivitas.pack(pady=(18, 12))

# Jalankan dashboard
perbarui_statistik()
root.mainloop()