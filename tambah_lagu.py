import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# ==========================================
# MELODIA | TAMBAH LAGU
# ==========================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(ROOT_DIR, "lagu.csv")

BG = "#0B0B14"
PANEL = "#151525"
FIELD = "#202037"
PURPLE = "#A78BFA"
PINK = "#F472B6"
WHITE = "#F4F2FF"
MUTED = "#9292AE"
GREEN = "#6EE7B7"


def siapkan_csv():
    """Buat file CSV dengan header jika belum tersedia."""
    if not os.path.exists(FILE_CSV) or os.path.getsize(FILE_CSV) == 0:
        with open(FILE_CSV, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["judul", "penulis", "isbn", "status"])


def muat_data():
    """Baca data yang sudah tersimpan."""
    siapkan_csv()

    with open(FILE_CSV, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return [
            {
                "judul": (row.get("judul") or "").strip(),
                "penulis": (row.get("penulis") or "").strip(),
                "isbn": (row.get("isbn") or "").strip(),
                "status": (row.get("status") or "Tersedia").strip()
            }
            for row in reader
        ]


def simpan_lagu():
    judul = entry_judul.get().strip()
    penulis = entry_penulis.get().strip()
    isbn = entry_isbn.get().strip()
    status = status_var.get()

    # Validasi formulir
    if not judul or not penulis or not isbn:
        messagebox.showwarning(
            "Data belum lengkap",
            "Judul, penulis, dan ISBN wajib diisi.",
            parent=root
        )
        return

    if status not in ("Tersedia", "Dipinjam"):
        messagebox.showwarning(
            "Status tidak valid",
            "Pilih status lagu yang tersedia.",
            parent=root
        )
        return

    try:
        data_lama = muat_data()
    except (OSError, csv.Error, UnicodeError) as error:
        messagebox.showerror(
            "Gagal membaca data",
            f"File CSV tidak dapat dibaca.\n{error}",
            parent=root
        )
        return

    # Cegah ISBN ganda
    for lagu in data_lama:
        if lagu["isbn"].casefold() == isbn.casefold():
            messagebox.showwarning(
                "ISBN sudah terdaftar",
                "ISBN ini sudah ada dalam koleksi.",
                parent=root
            )
            entry_isbn.focus_set()
            return

    # Simpan dengan header dan urutan kolom yang konsisten
    try:
        with open(FILE_CSV, "a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([judul, penulis, isbn, status])
    except OSError as error:
        messagebox.showerror(
            "Gagal menyimpan",
            f"Data tidak dapat disimpan.\n{error}",
            parent=root
        )
        return

    messagebox.showinfo(
        "Berhasil disimpan!",
        f"♫ Lagu berhasil ditambahkan!\n\n"
        f"Judul: {judul}\n"
        f"Penulis: {penulis}\n"
        f"Status: {status}",
        parent=root
    )

    bersihkan_form()
    perbarui_ringkasan()


def bersihkan_form():
    entry_judul.delete(0, tk.END)
    entry_penulis.delete(0, tk.END)
    entry_isbn.delete(0, tk.END)
    status_var.set("Tersedia")
    entry_judul.focus_set()


def perbarui_ringkasan():
    try:
        data = muat_data()
        total = len(data)
        tersedia = sum(
            lagu["status"].casefold() == "tersedia"
            for lagu in data
        )
        dipinjam = sum(
            lagu["status"].casefold() == "dipinjam"
            for lagu in data
        )

        label_total.config(text=str(total))
        label_tersedia.config(text=str(tersedia))
        label_dipinjam.config(text=str(dipinjam))

    except (OSError, csv.Error, UnicodeError):
        label_total.config(text="—")
        label_tersedia.config(text="—")
        label_dipinjam.config(text="—")


def buat_label(parent, teks):
    return tk.Label(
        parent,
        text=teks,
        font=("Segoe UI", 10, "bold"),
        bg=PANEL,
        fg=WHITE
    )


def buat_input(parent, placeholder):
    field = tk.Entry(
        parent,
        font=("Segoe UI", 11),
        bg=FIELD,
        fg=WHITE,
        insertbackground=PURPLE,
        relief="flat",
        bd=0
    )
    field.pack(fill="x", ipady=11, pady=(7, 18))
    field.insert(0, placeholder)
    field.config(fg=MUTED)

    def fokus_masuk(_event):
        if field.get() == placeholder:
            field.delete(0, tk.END)
            field.config(fg=WHITE)

    def fokus_keluar(_event):
        if not field.get().strip():
            field.delete(0, tk.END)
            field.insert(0, placeholder)
            field.config(fg=MUTED)

    field.bind("<FocusIn>", fokus_masuk)
    field.bind("<FocusOut>", fokus_keluar)

    return field


def ambil_nilai(field, placeholder):
    nilai = field.get().strip()
    if nilai == placeholder:
        return ""
    return nilai


def proses_simpan():
    # Abaikan teks petunjuk jika kolom belum diisi.
    nilai_judul = ambil_nilai(entry_judul, "Contoh: Laskar Pelangi")
    nilai_penulis = ambil_nilai(entry_penulis, "Nama penulis atau pencipta")
    nilai_isbn = ambil_nilai(entry_isbn, "Masukkan nomor ISBN")

    entry_judul.delete(0, tk.END)
    entry_judul.insert(0, nilai_judul)

    entry_penulis.delete(0, tk.END)
    entry_penulis.insert(0, nilai_penulis)

    entry_isbn.delete(0, tk.END)
    entry_isbn.insert(0, nilai_isbn)

    entry_judul.config(fg=WHITE)
    entry_penulis.config(fg=WHITE)
    entry_isbn.config(fg=WHITE)

    simpan_lagu()


# ==========================================
# JENDELA APLIKASI
# ==========================================

root = tk.Tk()
root.title("Melodia | Tambah Lagu")
root.geometry("850x760")
root.minsize(700, 650)
root.configure(bg=BG)

# Style untuk dropdown
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Melodia.TCombobox",
    fieldbackground=FIELD,
    background=FIELD,
    foreground=WHITE,
    arrowcolor=PURPLE,
    bordercolor=FIELD,
    lightcolor=FIELD,
    darkcolor=FIELD,
    padding=9
)
style.map(
    "Melodia.TCombobox",
    fieldbackground=[("readonly", FIELD)],
    foreground=[("readonly", WHITE)]
)

# Header
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=35, pady=(24, 20))

tk.Label(
    header,
    text="♫  MELODIA",
    font=("Segoe UI", 19, "bold"),
    bg=BG,
    fg=PURPLE
).pack(anchor="w")

tk.Label(
    header,
    text="ADD TO YOUR COLLECTION  /  RUANG MUSIK DIGITAL",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(4, 0))

tk.Frame(root, bg="#292440", height=1).pack(
    fill="x", padx=35, pady=(0, 22)
)

# Panel formulir
form_panel = tk.Frame(root, bg=PANEL)
form_panel.pack(fill="x", padx=35)

tk.Label(
    form_panel,
    text="Tambahkan cerita baru.",
    font=("Segoe UI", 21, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(anchor="w", padx=25, pady=(22, 5))

tk.Label(
    form_panel,
    text="Lengkapi informasi di bawah untuk menyimpan koleksi.",
    font=("Segoe UI", 10),
    bg=PANEL,
    fg=MUTED
).pack(anchor="w", padx=25, pady=(0, 20))

form = tk.Frame(form_panel, bg=PANEL)
form.pack(fill="x", padx=25)

buat_label(form, "JUDUL").pack(anchor="w")
entry_judul = buat_input(form, "Contoh: Laskar Pelangi")

buat_label(form, "PENULIS").pack(anchor="w")
entry_penulis = buat_input(form, "Nama penulis atau pencipta")

buat_label(form, "ISBN").pack(anchor="w")
entry_isbn = buat_input(form, "Masukkan nomor ISBN")

buat_label(form, "STATUS KOLEKSI").pack(anchor="w")

status_var = tk.StringVar(value="Tersedia")
status_box = ttk.Combobox(
    form,
    textvariable=status_var,
    values=["Tersedia", "Dipinjam"],
    state="readonly",
    style="Melodia.TCombobox",
    font=("Segoe UI", 10)
)
status_box.pack(fill="x", ipady=3, pady=(7, 22))

# Tombol aksi
actions = tk.Frame(form_panel, bg=PANEL)
actions.pack(fill="x", padx=25, pady=(0, 25))

tk.Button(
    actions,
    text="＋  SIMPAN KOLEKSI",
    command=proses_simpan,
    bg=PURPLE,
    fg=BG,
    activebackground=PINK,
    activeforeground=BG,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 10, "bold"),
    padx=18,
    pady=12
).pack(side="left", fill="x", expand=True, padx=(0, 6))

tk.Button(
    actions,
    text="↺  RESET",
    command=bersihkan_form,
    bg=FIELD,
    fg=WHITE,
    activebackground="#33334A",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 10, "bold"),
    padx=18,
    pady=12
).pack(side="left", padx=(6, 0))

# Ringkasan koleksi
tk.Label(
    root,
    text="KONDISI KOLEKSI SAAT INI",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=38, pady=(22, 10))

stats = tk.Frame(root, bg=BG)
stats.pack(fill="x", padx=35)

def buat_stat(parent, judul, warna):
    panel = tk.Frame(parent, bg=PANEL)
    panel.pack(side="left", fill="both", expand=True, padx=5)

    angka = tk.Label(
        panel,
        text="0",
        font=("Segoe UI", 20, "bold"),
        bg=PANEL,
        fg=warna
    )
    angka.pack(anchor="w", padx=15, pady=(12, 0))

    tk.Label(
        panel,
        text=judul,
        font=("Segoe UI", 9),
        bg=PANEL,
        fg=MUTED
    ).pack(anchor="w", padx=15, pady=(0, 12))

    return angka


label_total = buat_stat(stats, "Total koleksi", PURPLE)
label_tersedia = buat_stat(stats, "Tersedia", GREEN)
label_dipinjam = buat_stat(stats, "Dipinjam", PINK)

tk.Label(
    root,
    text="MELODIA  •  SIMPAN MUSIK, SIMPAN CERITA",
    font=("Segoe UI", 8, "bold"),
    bg=BG,
    fg=MUTED
).pack(pady=18)

perbarui_ringkasan()
entry_judul.focus_set()

root.mainloop()