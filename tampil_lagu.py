import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ==========================================
# MELODIA | TAMPIL LAGU
# Halaman Koleksi Musik
# ==========================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(ROOT_DIR, "lagu.csv")

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

KOLOM = ("judul", "penulis", "isbn", "status")

data_lagu = []


# ==========================================
# MANAJEMEN DATA CSV
# ==========================================

def siapkan_csv():
    """Membuat CSV dengan header jika belum tersedia."""
    if not os.path.exists(FILE_CSV) or os.path.getsize(FILE_CSV) == 0:
        with open(
            FILE_CSV,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(KOLOM)


def muat_data():
    """Membaca data lagu.csv dan memperbarui tabel."""
    global data_lagu

    try:
        siapkan_csv()

        with open(
            FILE_CSV,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("Header CSV tidak ditemukan.")

            header = {
                str(kolom).strip().casefold()
                for kolom in reader.fieldnames
                if kolom
            }

            if not set(KOLOM).issubset(header):
                raise ValueError(
                    "Format header CSV tidak sesuai.\n\n"
                    "Header yang dibutuhkan:\n"
                    "judul, penulis, isbn, status"
                )

            data_baru = []

            for nomor, row in enumerate(reader, start=2):
                baris = {
                    str(kunci).strip().casefold():
                    str(nilai or "").strip()
                    for kunci, nilai in row.items()
                    if kunci is not None
                }

                if not any(baris.values()):
                    continue

                judul = baris.get("judul", "")
                penulis = baris.get("penulis", "")
                isbn = baris.get("isbn", "")
                status = baris.get("status", "Tersedia")

                if not judul or not penulis or not isbn:
                    raise ValueError(
                        f"Data tidak lengkap pada baris {nomor}."
                    )

                if status.casefold() not in ("tersedia", "dipinjam"):
                    raise ValueError(
                        f"Status tidak valid pada baris {nomor}: "
                        f"{status}"
                    )

                status = (
                    "Tersedia"
                    if status.casefold() == "tersedia"
                    else "Dipinjam"
                )

                data_baru.append({
                    "judul": judul,
                    "penulis": penulis,
                    "isbn": isbn,
                    "status": status
                })

        data_lagu = data_baru
        tampilkan_data()

        label_status.config(
            text="DATA BERHASIL DIMUAT",
            fg=GREEN
        )

    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        messagebox.showerror(
            "Gagal Memuat Data",
            f"Data koleksi tidak dapat dibaca.\n\n{error}",
            parent=root
        )

        label_status.config(
            text="GAGAL MEMUAT DATA",
            fg=RED
        )


# ==========================================
# PENCARIAN DAN FILTER
# ==========================================

def ambil_hasil_filter():
    """Menghasilkan koleksi sesuai pencarian dan status."""
    kata_kunci = search_var.get().strip().casefold()
    status_pilihan = filter_var.get()

    hasil = []

    for lagu in data_lagu:
        teks = " ".join(lagu.values()).casefold()

        if kata_kunci and kata_kunci not in teks:
            continue

        if status_pilihan != "Semua Status":
            if lagu["status"] != status_pilihan:
                continue

        hasil.append(lagu)

    return hasil


def tampilkan_data(*_):
    """Menampilkan koleksi yang sesuai dengan filter."""
    for item in tabel.get_children():
        tabel.delete(item)

    hasil = ambil_hasil_filter()

    for indeks, lagu in enumerate(hasil):
        if lagu["status"] == "Tersedia":
            tag = "tersedia"
        else:
            tag = "dipinjam"

        tabel.insert(
            "",
            "end",
            iid=f"lagu_{indeks}",
            values=(
                lagu["judul"],
                lagu["penulis"],
                lagu["isbn"],
                lagu["status"]
            ),
            tags=(tag,)
        )

    label_hasil.config(
        text=f"Menampilkan {len(hasil)} dari {len(data_lagu)} koleksi"
    )

    total = len(data_lagu)
    tersedia = sum(
        lagu["status"] == "Tersedia"
        for lagu in data_lagu
    )
    dipinjam = sum(
        lagu["status"] == "Dipinjam"
        for lagu in data_lagu
    )

    stat_total.config(text=str(total))
    stat_tersedia.config(text=str(tersedia))
    stat_dipinjam.config(text=str(dipinjam))


def cari_data(*_):
    tampilkan_data()


def reset_filter():
    search_var.set("")
    filter_var.set("Semua Status")
    tampilkan_data()


# ==========================================
# DETAIL LAGU
# ==========================================

def tampilkan_detail(_event=None):
    pilihan = tabel.selection()

    if not pilihan:
        return

    nilai = tabel.item(pilihan[0], "values")

    if not nilai:
        return

    judul, penulis, isbn, status = nilai

    messagebox.showinfo(
        "Detail Koleksi",
        "♫  DETAIL KOLEKSI\n\n"
        f"Judul   : {judul}\n"
        f"Penulis : {penulis}\n"
        f"ISBN    : {isbn}\n"
        f"Status  : {status}",
        parent=root
    )


# ==========================================
# EKSPOR CSV
# ==========================================

def ekspor_csv():
    hasil = ambil_hasil_filter()

    if not hasil:
        messagebox.showwarning(
            "Tidak Ada Data",
            "Tidak ada koleksi untuk diekspor.",
            parent=root
        )
        return

    lokasi = filedialog.asksaveasfilename(
        parent=root,
        title="Ekspor Koleksi MELODIA",
        defaultextension=".csv",
        initialfile="koleksi_melodia.csv",
        filetypes=[("File CSV", "*.csv")]
    )

    if not lokasi:
        return

    if os.path.abspath(lokasi) == os.path.abspath(FILE_CSV):
        messagebox.showwarning(
            "Lokasi Tidak Diizinkan",
            "Jangan menimpa file lagu.csv utama.",
            parent=root
        )
        return

    try:
        with open(
            lokasi,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=KOLOM
            )
            writer.writeheader()
            writer.writerows(hasil)

        messagebox.showinfo(
            "Ekspor Berhasil",
            f"{len(hasil)} koleksi berhasil diekspor.",
            parent=root
        )

    except OSError as error:
        messagebox.showerror(
            "Ekspor Gagal",
            str(error),
            parent=root
        )


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
        font=("Segoe UI", 22, "bold"),
        bg=PANEL,
        fg=warna
    )
    angka.pack(anchor="w", padx=16, pady=(12, 0))

    tk.Label(
        panel,
        text=judul,
        font=("Segoe UI", 9),
        bg=PANEL,
        fg=MUTED
    ).pack(anchor="w", padx=16, pady=(0, 12))

    return panel, angka


def tombol(parent, teks, aksi, warna=PURPLE, foreground=BG):
    return tk.Button(
        parent,
        text=teks,
        command=aksi,
        bg=warna,
        fg=foreground,
        activebackground=PINK,
        activeforeground=BG,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 9, "bold"),
        padx=14,
        pady=10
    )


def buat_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg=MUTED)

    def fokus_masuk(_event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=WHITE)

    def fokus_keluar(_event):
        if not entry.get().strip():
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.config(fg=MUTED)

    entry.bind("<FocusIn>", fokus_masuk)
    entry.bind("<FocusOut>", fokus_keluar)


# ==========================================
# JENDELA APLIKASI
# ==========================================

root = tk.Tk()
root.title("Melodia | Koleksi Lagu")
root.geometry("1100x740")
root.minsize(800, 600)
root.configure(bg=BG)

search_var = tk.StringVar()
filter_var = tk.StringVar(value="Semua Status")

# ==========================================
# STYLE TABEL
# ==========================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Melodia.Treeview",
    background=PANEL,
    foreground=WHITE,
    fieldbackground=PANEL,
    borderwidth=0,
    rowheight=36,
    font=("Segoe UI", 10)
)

style.configure(
    "Melodia.Treeview.Heading",
    background="#25213A",
    foreground=PURPLE,
    relief="flat",
    borderwidth=0,
    font=("Segoe UI", 9, "bold"),
    padding=(10, 12)
)

style.map(
    "Melodia.Treeview",
    background=[("selected", "#49366F")],
    foreground=[("selected", WHITE)]
)

style.configure(
    "Melodia.TCombobox",
    fieldbackground=FIELD,
    background=FIELD,
    foreground=WHITE,
    arrowcolor=PURPLE,
    bordercolor=FIELD,
    padding=8
)

style.map(
    "Melodia.TCombobox",
    fieldbackground=[("readonly", FIELD)],
    foreground=[("readonly", WHITE)]
)

# ==========================================
# HEADER
# ==========================================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=30, pady=(22, 15))

tk.Label(
    header,
    text="♫  MELODIA",
    font=("Segoe UI", 20, "bold"),
    bg=BG,
    fg=PURPLE
).pack(side="left")

tk.Label(
    header,
    text="YOUR COLLECTION  /  LIBRARY",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=MUTED
).pack(side="right", pady=8)

tk.Frame(
    root,
    bg="#292440",
    height=1
).pack(fill="x", padx=30, pady=(0, 20))

# ==========================================
# JUDUL HALAMAN
# ==========================================

tk.Label(
    root,
    text="Koleksi Lagu",
    font=("Segoe UI", 25, "bold"),
    bg=BG,
    fg=WHITE
).pack(anchor="w", padx=35)

tk.Label(
    root,
    text="Temukan kembali setiap cerita dalam koleksimu.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=36, pady=(3, 18))

# ==========================================
# STATISTIK
# ==========================================

stats = tk.Frame(root, bg=BG)
stats.pack(fill="x", padx=30)

panel_total, stat_total = buat_stat(
    stats, "Total Koleksi", PURPLE
)
panel_tersedia, stat_tersedia = buat_stat(
    stats, "Tersedia", GREEN
)
panel_dipinjam, stat_dipinjam = buat_stat(
    stats, "Dipinjam", PINK
)

for panel in (panel_total, panel_tersedia, panel_dipinjam):
    panel.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

# ==========================================
# TOOLBAR PENCARIAN
# ==========================================

toolbar = tk.Frame(root, bg=BG)
toolbar.pack(fill="x", padx=35, pady=(22, 12))

search_box = tk.Entry(
    toolbar,
    textvariable=search_var,
    font=("Segoe UI", 10),
    bg=FIELD,
    fg=WHITE,
    insertbackground=PURPLE,
    relief="flat"
)

search_box.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 10)
)

buat_placeholder(
    search_box,
    "Cari judul, penulis, atau ISBN..."
)

search_var.trace_add("write", cari_data)

filter_box = ttk.Combobox(
    toolbar,
    textvariable=filter_var,
    values=["Semua Status", "Tersedia", "Dipinjam"],
    state="readonly",
    width=16,
    style="Melodia.TCombobox",
    font=("Segoe UI", 9)
)
filter_box.pack(side="left", padx=(0, 8))
filter_box.bind("<<ComboboxSelected>>", tampilkan_data)

tombol(
    toolbar,
    "↻ REFRESH",
    muat_data,
    BLUE
).pack(side="left", padx=(0, 8))

tombol(
    toolbar,
    "RESET",
    reset_filter,
    "#302B45",
    WHITE
).pack(side="left")

# ==========================================
# TABEL KOLEKSI
# ==========================================

table_panel = tk.Frame(root, bg=PANEL)
table_panel.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=(0, 10)
)

tabel = ttk.Treeview(
    table_panel,
    columns=KOLOM,
    show="headings",
    style="Melodia.Treeview",
    selectmode="browse"
)

tabel.heading("judul", text="JUDUL")
tabel.heading("penulis", text="PENULIS")
tabel.heading("isbn", text="ISBN")
tabel.heading("status", text="STATUS")

tabel.column(
    "judul", width=260, minwidth=150, anchor="w"
)
tabel.column(
    "penulis", width=220, minwidth=120, anchor="w"
)
tabel.column(
    "isbn", width=190, minwidth=130, anchor="w"
)
tabel.column(
    "status", width=115, minwidth=100, anchor="center"
)

scroll_y = ttk.Scrollbar(
    table_panel,
    orient="vertical",
    command=tabel.yview
)

scroll_x = ttk.Scrollbar(
    table_panel,
    orient="horizontal",
    command=tabel.xview
)

tabel.configure(
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

table_panel.rowconfigure(0, weight=1)
table_panel.columnconfigure(0, weight=1)

tabel.grid(
    row=0, column=0,
    sticky="nsew",
    padx=(8, 0), pady=8
)

scroll_y.grid(row=0, column=1, sticky="ns", pady=8)
scroll_x.grid(
    row=1, column=0,
    sticky="ew", padx=(8, 0)
)

tabel.tag_configure("tersedia", foreground=GREEN)
tabel.tag_configure("dipinjam", foreground=PINK)

tabel.bind("<Double-1>", tampilkan_detail)

# ==========================================
# FOOTER
# ==========================================

footer = tk.Frame(root, bg=BG)
footer.pack(fill="x", padx=35, pady=(0, 8))

label_hasil = tk.Label(
    footer,
    text="Memuat koleksi...",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
)
label_hasil.pack(side="left")

label_status = tk.Label(
    footer,
    text="MENYIAPKAN DATA",
    font=("Segoe UI", 8, "bold"),
    bg=BG,
    fg=GREEN
)
label_status.pack(side="left", padx=15)

tombol(
    footer,
    "⇩ EKSPOR CSV",
    ekspor_csv,
    PURPLE
).pack(side="right")

tk.Label(
    footer,
    text="Klik dua kali baris untuk detail",
    font=("Segoe UI", 8),
    bg=BG,
    fg=MUTED
).pack(side="right", padx=15)

# ==========================================
# JALANKAN APLIKASI
# ==========================================

muat_data()
root.mainloop()