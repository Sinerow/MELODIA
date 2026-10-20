import math
import tkinter as tk
from tkinter import ttk

BG = "#0B0B14"            # Deep Dark Space
PANEL = "#151525"         # Surface Panel
PANEL_BORDER = "#292440"  # Subtle Purple Border
FIELD = "#202037"         # Entry Field
PURPLE = "#A78BFA"        # Neon Violet
PINK = "#F472B6"          # Neon Pink
BLUE = "#60A5FA"          # Neon Blue
CYAN = "#38BDF8"          # Electric Cyan
WHITE = "#F4F2FF"         # Crisp White
MUTED = "#9292AE"         # Muted Purple Gray
GREEN = "#6EE7B7"         # Emerald Green
RED = "#FB7185"           # Coral Red


class MusicVisualizer(tk.Canvas):
    """Visualizer gelombang audio animasi dinamis."""

    def __init__(self, parent, width=280, height=45, num_bars=22, **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=PANEL,
            highlightthickness=0,
            bd=0,
            **kwargs
        )
        self.num_bars = num_bars
        self.bar_width = width / num_bars
        self.max_height = height
        self.phase = 0
        self.is_running = True
        self.animate()

    def animate(self):
        if not self.winfo_exists():
            return

        self.delete("all")
        self.phase += 0.18

        for i in range(self.num_bars):
            wave1 = math.sin(self.phase + i * 0.45)
            wave2 = math.cos(self.phase * 0.8 + i * 0.25)
            height_factor = abs(wave1 * 0.6 + wave2 * 0.4)
            bar_h = max(5, height_factor * (self.max_height - 5))

            x0 = i * self.bar_width + 2
            y0 = (self.max_height - bar_h) / 2
            x1 = (i + 1) * self.bar_width - 2
            y1 = y0 + bar_h

            ratio = i / self.num_bars
            color = CYAN if ratio < 0.35 else (PURPLE if ratio < 0.7 else PINK)

            self.create_rectangle(x0, y0, x1, y1, fill=color, outline="", tags="bar")

        if self.is_running:
            self.after(45, self.animate)


def terapkan_tema_ttk():
    """Terapkan style kustom global TTK."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Melodia.TCombobox",
        fieldbackground=FIELD,
        background=FIELD,
        foreground=WHITE,
        arrowcolor=PURPLE,
        bordercolor=PANEL_BORDER,
        lightcolor=FIELD,
        darkcolor=FIELD,
        padding=8
    )
    style.map(
        "Melodia.TCombobox",
        fieldbackground=[("readonly", FIELD)],
        foreground=[("readonly", WHITE)]
    )

    style.configure(
        "Melodia.Treeview",
        background=PANEL,
        foreground=WHITE,
        fieldbackground=PANEL,
        rowheight=38,
        font=("Segoe UI", 10),
        borderwidth=0
    )
    style.configure(
        "Melodia.Treeview.Heading",
        background=FIELD,
        foreground=PURPLE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        borderwidth=0
    )
    style.map(
        "Melodia.Treeview",
        background=[("selected", "#332A59")],
        foreground=[("selected", WHITE)]
    )


def buat_panel_kartu(parent, **kwargs):
    return tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground=PANEL_BORDER,
        highlightthickness=1,
        **kwargs
    )


def buat_tombol_modern(parent, teks, perintah, warna_bg=PURPLE, warna_fg=BG, icon=""):
    label_teks = f"{icon}  {teks}".strip() if icon else teks
    tombol = tk.Button(
        parent,
        text=label_teks,
        command=perintah,
        bg=warna_bg,
        fg=warna_fg,
        activebackground=PINK,
        activeforeground=BG,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=18,
        pady=10
    )

    def hover_in(_e):
        if warna_bg == PURPLE:
            tombol.config(bg=PINK)
        elif warna_bg == FIELD:
            tombol.config(bg="#33334A")
        elif warna_bg == BLUE:
            tombol.config(bg="#93C5FD")

    def hover_out(_e):
        tombol.config(bg=warna_bg)

    tombol.bind("<Enter>", hover_in)
    tombol.bind("<Leave>", hover_out)
    return tombol


def buat_stat_card(parent, judul, warna_angka, icon="♫"):
    panel = buat_panel_kartu(parent)

    header_frame = tk.Frame(panel, bg=PANEL)
    header_frame.pack(fill="x", padx=18, pady=(15, 0))

    tk.Label(
        header_frame,
        text=icon,
        font=("Segoe UI", 14),
        bg=PANEL,
        fg=warna_angka
    ).pack(side="left")

    label_angka = tk.Label(
        panel,
        text="0",
        font=("Segoe UI", 24, "bold"),
        bg=PANEL,
        fg=warna_angka
    )
    label_angka.pack(anchor="w", padx=18, pady=(4, 0))

    tk.Label(
        panel,
        text=judul,
        font=("Segoe UI", 9, "bold"),
        bg=PANEL,
        fg=MUTED
    ).pack(anchor="w", padx=18, pady=(2, 14))

    return panel, label_angka


def buat_input_field(parent, placeholder, show_char=None):
    container = tk.Frame(parent, bg=FIELD)
    container.pack(fill="x", pady=(5, 15))

    field = tk.Entry(
        container,
        font=("Segoe UI", 11),
        bg=FIELD,
        fg=WHITE,
        insertbackground=PURPLE,
        relief="flat",
        bd=0,
        show=show_char or ""
    )
    field.pack(fill="x", padx=14, ipady=10)
    field.insert(0, placeholder)
    field.config(fg=MUTED)

    def fokus_masuk(_e):
        if field.get() == placeholder:
            field.delete(0, tk.END)
            field.config(fg=WHITE)

    def fokus_keluar(_e):
        if not field.get().strip():
            field.delete(0, tk.END)
            field.insert(0, placeholder)
            field.config(fg=MUTED)

    field.bind("<FocusIn>", fokus_masuk)
    field.bind("<FocusOut>", fokus_keluar)
    return field


def ambil_nilai_input(field, placeholder):
    val = field.get().strip()
    return "" if val == placeholder else val


def buat_now_playing_bar(parent, judul_lagu="Laskar Pelangi", penyanyi="Nidji"):
    bar = tk.Frame(parent, bg=PANEL, highlightbackground=PANEL_BORDER, highlightthickness=1)
    bar.pack(fill="x", side="bottom", padx=20, pady=15)

    info = tk.Frame(bar, bg=PANEL)
    info.pack(side="left", padx=20, pady=10)

    tk.Label(
        info,
        text=f"▶  {judul_lagu}",
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=WHITE
    ).pack(anchor="w")

    tk.Label(
        info,
        text=f"Penyanyi: {penyanyi}",
        font=("Segoe UI", 9),
        bg=PANEL,
        fg=MUTED
    ).pack(anchor="w")

    vis = MusicVisualizer(bar, width=180, height=35, num_bars=16)
    vis.pack(side="right", padx=20)

    return bar
