import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

import ui

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(ROOT_DIR, "lagu.csv")


def simpan_lagu():
    judul = ui.ambil_nilai_input(entry_judul, "Contoh: Hati-Hati di Jalan")
    penyanyi = ui.ambil_nilai_input(entry_penyanyi, "Contoh: Tulus")
    album = ui.ambil_nilai_input(entry_album, "Contoh: Manusia")
    genre = genre_var.get()
    status = status_var.get()
    pendengar_str = ui.ambil_nilai_input(entry_pendengar, "Contoh: 5000000")

    if not judul or not penyanyi:
        messagebox.showwarning("Form Belum Lengkap", "Judul dan Penyanyi wajib diisi!", parent=root)
        return

    try:
        pendengar = int(pendengar_str) if pendengar_str else 0
    except ValueError:
        messagebox.showwarning("Input Salah", "Jumlah pendengar harus berupa angka!", parent=root)
        return

    try:
        with open(FILE_CSV, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([judul, penyanyi, album, genre, status, pendengar])

        messagebox.showinfo("Sukses", f"♫ Lagu '{judul}' berhasil ditambahkan!", parent=root)
        bersihkan_form()
    except Exception as e:
        messagebox.showerror("Gagal Menyimpan", str(e), parent=root)


def bersihkan_form():
    for entry, ph in [
        (entry_judul, "Contoh: Hati-Hati di Jalan"),
        (entry_penyanyi, "Contoh: Tulus"),
        (entry_album, "Contoh: Manusia"),
        (entry_pendengar, "Contoh: 5000000")
    ]:
        entry.delete(0, tk.END)
        entry.insert(0, ph)
        entry.config(fg=ui.MUTED)

    status_var.set("Tersedia")
    genre_var.set("Pop")


root = tk.Tk()
root.title("Melodia | Tambah Lagu")
root.geometry("780x700")
root.configure(bg=ui.BG)

ui.terapkan_tema_ttk()

# Header
header = tk.Frame(root, bg=ui.BG)
header.pack(fill="x", padx=30, pady=(20, 10))
tk.Label(header, text="♫ MELODIA", font=("Segoe UI", 18, "bold"), bg=ui.BG, fg=ui.PURPLE).pack(side="left")
tk.Label(header, text="INPUT TRACK", font=("Segoe UI", 9, "bold"), bg=ui.BG, fg=ui.MUTED).pack(side="right")

panel = ui.buat_panel_kartu(root)
panel.pack(fill="both", expand=True, padx=30, pady=10)

tk.Label(panel, text="Tambah Koleksi Musik", font=("Segoe UI", 18, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w", padx=25, pady=(20, 5))

form = tk.Frame(panel, bg=ui.PANEL)
form.pack(fill="x", padx=25, pady=10)

tk.Label(form, text="JUDUL LAGU", font=("Segoe UI", 9, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w")
entry_judul = ui.buat_input_field(form, "Contoh: Hati-Hati di Jalan")

tk.Label(form, text="PENYANYI / ARTIS", font=("Segoe UI", 9, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w")
entry_penyanyi = ui.buat_input_field(form, "Contoh: Tulus")

tk.Label(form, text="ALBUM", font=("Segoe UI", 9, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w")
entry_album = ui.buat_input_field(form, "Contoh: Manusia")

grid_frame = tk.Frame(form, bg=ui.PANEL)
grid_frame.pack(fill="x", pady=5)

# Dropdown Genre
g_left = tk.Frame(grid_frame, bg=ui.PANEL)
g_left.pack(side="left", fill="x", expand=True, padx=(0, 5))
tk.Label(g_left, text="GENRE", font=("Segoe UI", 9, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w")
genre_var = tk.StringVar(value="Pop")
box_genre = ttk.Combobox(g_left, textvariable=genre_var, values=["Pop", "Indie Folk", "Alternative", "Rock", "Acoustic", "Pop Jawa"], state="readonly", style="Melodia.TCombobox")
box_genre.pack(fill="x", pady=5)

# Dropdown Status
g_right = tk.Frame(grid_frame, bg=ui.PANEL)
g_right.pack(side="left", fill="x", expand=True, padx=(5, 0))
tk.Label(g_right, text="STATUS", font=("Segoe UI", 9, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w")
status_var = tk.StringVar(value="Tersedia")
box_status = ttk.Combobox(g_right, textvariable=status_var, values=["Tersedia", "Dipinjam"], state="readonly", style="Melodia.TCombobox")
box_status.pack(fill="x", pady=5)

tk.Label(form, text="ESTIMASI PENDENGAR (ESTIMATED LISTENERS)", font=("Segoe UI", 9, "bold"), bg=ui.PANEL, fg=ui.WHITE).pack(anchor="w", pady=(10, 0))
entry_pendengar = ui.buat_input_field(form, "Contoh: 5000000")

# Action Buttons
btn_frame = tk.Frame(panel, bg=ui.PANEL)
btn_frame.pack(fill="x", padx=25, pady=(10, 20))

ui.buat_tombol_modern(btn_frame, "SIMPAN LAGU", simpan_lagu, ui.PURPLE, icon="＋").pack(side="left", fill="x", expand=True, padx=(0, 5))
ui.buat_tombol_modern(btn_frame, "RESET", bersihkan_form, ui.FIELD, ui.WHITE, icon="↺").pack(side="left", padx=(5, 0))

root.mainloop()
