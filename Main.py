import csv
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

import ui

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(ROOT_DIR, "lagu.csv")

KOLOM = ["judul", "penyanyi", "album", "genre", "status", "pendengar"]


def siapkan_csv():
    if not os.path.exists(FILE_CSV) or os.path.getsize(FILE_CSV) == 0:
        with open(FILE_CSV, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(KOLOM)


def muat_data():
    siapkan_csv()
    with open(FILE_CSV, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if any(row.values())]


def perbarui_statistik():
    try:
        data = muat_data()
        total = len(data)
        tersedia = sum(1 for item in data if item.get("status", "").casefold() == "tersedia")
        dipinjam = sum(1 for item in data if item.get("status", "").casefold() == "dipinjam")
        total_listeners = sum(int(item.get("pendengar", 0) or 0) for item in data)

        label_total.config(text=str(total))
        label_tersedia.config(text=str(tersedia))
        label_dipinjam.config(text=str(dipinjam))
        
        if total_listeners >= 1_000_000:
            formatted_listeners = f"{total_listeners / 1_000_000:.1f}M"
        else:
            formatted_listeners = f"{total_listeners:,}"
        label_pendengar.config(text=formatted_listeners)

        label_status.config(text="● DATA TERSINKRONISASI", fg=ui.GREEN)
    except Exception as err:
        label_status.config(text="● GAGAL MEMUAT DATA", fg=ui.RED)


def buka_halaman(nama_file, judul):
    lokasi = os.path.join(ROOT_DIR, nama_file)
    if not os.path.isfile(lokasi):
        messagebox.showerror("Error", f"File {nama_file} tidak ditemukan.", parent=root)
        return
    try:
        subprocess.Popen([sys.executable, lokasi], cwd=ROOT_DIR)
        root.after(1200, perbarui_statistik)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka {judul}: {e}", parent=root)


root = tk.Tk()
root.title("Melodia | Music Dashboard")
root.geometry("1020x720")
root.configure(bg=ui.BG)

# Header Branding
header = tk.Frame(root, bg=ui.BG)
header.pack(fill="x", padx=35, pady=(20, 10))

tk.Label(header, text="♫ MELODIA", font=("Segoe UI", 22, "bold"), bg=ui.BG, fg=ui.PURPLE).pack(side="left")
tk.Label(header, text="MUSIC DASHBOARD", font=("Segoe UI", 9, "bold"), bg=ui.BG, fg=ui.PINK).pack(side="right")

tk.Frame(root, bg=ui.PANEL_BORDER, height=1).pack(fill="x", padx=35, pady=(5, 15))

# Welcome Banner
tk.Label(root, text="Ruang Musik & Audio Digital", font=("Segoe UI", 24, "bold"), bg=ui.BG, fg=ui.WHITE).pack(anchor="w", padx=35)
tk.Label(root, text="Kelola trek favorit, status pemutaran, dan total pendengar dalam satu perpustakaan.", font=("Segoe UI", 10), bg=ui.BG, fg=ui.MUTED).pack(anchor="w", padx=35, pady=(2, 15))

# Cards Statistik
stats_frame = tk.Frame(root, bg=ui.BG)
stats_frame.pack(fill="x", padx=30, pady=5)

card_total, label_total = ui.buat_stat_card(stats_frame, "Total Lagu", ui.PURPLE, "🎵")
card_tersedia, label_tersedia = ui.buat_stat_card(stats_frame, "Tersedia", ui.GREEN, "▶")
card_dipinjam, label_dipinjam = ui.buat_stat_card(stats_frame, "Diputar/Dipinjam", ui.PINK, "🎧")
card_pendengar, label_pendengar = ui.buat_stat_card(stats_frame, "Total Pendengar", ui.CYAN, "🔥")

for card in (card_total, card_tersedia, card_dipinjam, card_pendengar):
    card.pack(side="left", fill="both", expand=True, padx=5)

# Navigasi Utama
menu_frame = tk.Frame(root, bg=ui.BG)
menu_frame.pack(fill="x", padx=35, pady=25)

# Kartu Tambah Lagu
p_tambah = ui.buat_panel_kartu(menu_frame)
p_tambah.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(p_tambah, text="＋", font=("Segoe UI", 24, "bold"), bg=ui.PANEL, fg=ui.PURPLE).pack(anchor="w", padx=18, pady=(15, 0))
tk.Label(p_tambah, text="Tambah Lagu Baru", font=("Segoe UI", 13, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w", padx=18)
tk.Label(p_tambah, text="Input judul, penyanyi, album, dan estimasi pendengar.", font=("Segoe UI", 9), bg=ui.PANEL, fg=ui.MUTED, wraplength=220, justify="left").pack(anchor="w", padx=18, pady=(2, 15))
ui.buat_tombol_modern(p_tambah, "TAMBAH LAGU", lambda: buka_halaman("tambah_lagu.py", "Tambah Lagu"), ui.PURPLE).pack(fill="x", padx=18, pady=(0, 18))

# Kartu Jelajah Koleksi
p_koleksi = ui.buat_panel_kartu(menu_frame)
p_koleksi.pack(side="left", fill="both", expand=True, padx=(10, 0))

tk.Label(p_koleksi, text="☷", font=("Segoe UI", 24, "bold"), bg=ui.PANEL, fg=ui.BLUE).pack(anchor="w", padx=18, pady=(15, 0))
tk.Label(p_koleksi, text="Eksplor Koleksi", font=("Segoe UI", 13, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w", padx=18)
tk.Label(p_koleksi, text="Filter genre, pencarian judul/penyanyi, dan ekspor CSV.", font=("Segoe UI", 9), bg=ui.PANEL, fg=ui.MUTED, wraplength=220, justify="left").pack(anchor="w", padx=18, pady=(2, 15))
ui.buat_tombol_modern(p_koleksi, "BUKA KOLEKSI", lambda: buka_halaman("tampil_buku.py", "Koleksi Musik"), ui.BLUE).pack(fill="x", padx=18, pady=(0, 18))

# Bottom Status
status_bar = tk.Frame(root, bg=ui.BG)
status_bar.pack(fill="x", padx=35)

label_status = tk.Label(status_bar, text="MEMUAT...", font=("Segoe UI", 8, "bold"), bg=ui.BG, fg=ui.GREEN)
label_status.pack(side="left")

ui.buat_tombol_modern(status_bar, "REFRESH", perbarui_statistik, ui.FIELD, ui.WHITE, icon="↻").pack(side="right")

ui.buat_now_playing_bar(root, "Untungnya, Hidup Harus Tetap Berjalan", "Bernadya")

perbarui_statistik()
root.mainloop()
