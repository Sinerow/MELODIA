import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import ui
from models import Lagu

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(ROOT_DIR, "lagu.csv")

data_lagu = []


def muat_data():
    global data_lagu
    try:
        data_lagu = []
        if os.path.exists(FILE_CSV):
            with open(FILE_CSV, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if any(row.values()):
                        data_lagu.append(Lagu.from_dict(row))
        tampilkan_data()
    except Exception as e:
        messagebox.showerror("Gagal Memuat Data", str(e), parent=root)


def tampilkan_data(*_):
    for row in tabel.get_children():
        tabel.delete(row)

    kata_kunci = search_var.get().strip().casefold()
    filter_st = filter_var.get()

    baris_tertampil = 0
    for l in data_lagu:
        teks_gabung = f"{l.judul} {l.penyanyi} {l.album} {l.genre}".casefold()
        
        if kata_kunci and kata_kunci not in teks_gabung:
            continue
        if filter_st != "Semua Status" and l.status != filter_st:
            continue

        tag = "tersedia" if l.status == "Tersedia" else "dipinjam"
        tabel.insert(
            "", "end",
            values=(l.judul, l.penyanyi, l.album, l.genre, l.status, l.pendengar_formatted),
            tags=(tag,)
        )
        baris_tertampil += 1

    label_count.config(text=f"Menampilkan {baris_tertampil} dari {len(data_lagu)} koleksi")


def ekspor_csv():
    lokasi = filedialog.asksaveasfilename(
        parent=root,
        title="Ekspor Lagu MELODIA",
        defaultextension=".csv",
        initialfile="koleksi_lagu_melodia.csv",
        filetypes=[("CSV File", "*.csv")]
    )
    if not lokasi:
        return
    try:
        with open(lokasi, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["judul", "penyanyi", "album", "genre", "status", "pendengar"])
            for l in data_lagu:
                writer.writerow(l.to_list())
        messagebox.showinfo("Berhasil", "Data berhasil diekspor!", parent=root)
    except Exception as e:
        messagebox.showerror("Gagal", str(e), parent=root)


root = tk.Tk()
root.title("Melodia | Koleksi Lagu")
root.geometry("1080x720")
root.configure(bg=ui.BG)

ui.terapkan_tema_ttk()

search_var = tk.StringVar()
filter_var = tk.StringVar(value="Semua Status")

# Header
header = tk.Frame(root, bg=ui.BG)
header.pack(fill="x", padx=30, pady=(18, 10))
tk.Label(header, text="♫ MELODIA", font=("Segoe UI", 18, "bold"), bg=ui.BG, fg=ui.PURPLE).pack(side="left")
tk.Label(header, text="EXPLORE COLLECTION", font=("Segoe UI", 9, "bold"), bg=ui.BG, fg=ui.MUTED).pack(side="right")

# Toolbar Filter/Search
toolbar = tk.Frame(root, bg=ui.BG)
toolbar.pack(fill="x", padx=30, pady=10)

search_entry = tk.Entry(toolbar, textvariable=search_var, font=("Segoe UI", 10), bg=ui.FIELD, fg=ui.WHITE, insertbackground=ui.PURPLE, relief="flat")
search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
search_var.trace_add("write", tampilkan_data)

filter_box = ttk.Combobox(toolbar, textvariable=filter_var, values=["Semua Status", "Tersedia", "Dipinjam"], state="readonly", width=14, style="Melodia.TCombobox")
filter_box.pack(side="left", padx=(0, 10))
filter_box.bind("<<ComboboxSelected>>", tampilkan_data)

ui.buat_tombol_modern(toolbar, "EKSPOR", ekspor_csv, ui.PURPLE, icon="⇩").pack(side="right")

# Tabel Utama
table_panel = ui.buat_panel_kartu(root)
table_panel.pack(fill="both", expand=True, padx=30, pady=10)

tabel = ttk.Treeview(
    table_panel,
    columns=("judul", "penyanyi", "album", "genre", "status", "pendengar"),
    show="headings",
    style="Melodia.Treeview"
)

tabel.heading("judul", text="JUDUL LAGU")
tabel.heading("penyanyi", text="PENYANYI")
tabel.heading("album", text="ALBUM")
tabel.heading("genre", text="GENRE")
tabel.heading("status", text="STATUS")
tabel.heading("pendengar", text="PENDENGAR")

tabel.column("judul", width=220, anchor="w")
tabel.column("penyanyi", width=180, anchor="w")
tabel.column("album", width=160, anchor="w")
tabel.column("genre", width=120, anchor="center")
tabel.column("status", width=110, anchor="center")
tabel.column("pendengar", width=120, anchor="e")

tabel.tag_configure("tersedia", foreground=ui.GREEN)
tabel.tag_configure("dipinjam", foreground=ui.PINK)

scroll = ttk.Scrollbar(table_panel, orient="vertical", command=tabel.yview)
tabel.configure(yscrollcommand=scroll.set)

tabel.pack(side="left", fill="both", expand=True, padx=5, pady=5)
scroll.pack(side="right", fill="y", pady=5)

# Footer Status
footer = tk.Frame(root, bg=ui.BG)
footer.pack(fill="x", padx=30, pady=(0, 10))

label_count = tk.Label(footer, text="Memuat data...", font=("Segoe UI", 9), bg=ui.BG, fg=ui.MUTED)
label_count.pack(side="left")

ui.buat_now_playing_bar(root, "Gala Bunga Matahari", "Sal Priadi")

muat_data()
root.mainloop()
