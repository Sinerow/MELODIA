class Lagu:
    """Model data resmi untuk entri lagu di Melodia."""

    KOLOM = ("judul", "penyanyi", "album", "genre", "status", "pendengar")
    STATUS_VALID = ("Tersedia", "Dipinjam")

    def __init__(self, judul, penyanyi, album="", genre="Pop", status="Tersedia", pendengar=0):
        self.judul = str(judul).strip()
        self.penyanyi = str(penyanyi).strip()
        self.album = str(album).strip() or "Single"
        self.genre = str(genre).strip() or "General"
        self.status = str(status).strip()
        
        try:
            self.pendengar = int(pendengar)
        except (ValueError, TypeError):
            self.pendengar = 0

        self.validasi()

    def validasi(self):
        if not self.judul:
            raise ValueError("Judul lagu wajib diisi.")
        if not self.penyanyi:
            raise ValueError("Nama penyanyi/pencipta wajib diisi.")

        status_lower = self.status.casefold()
        if status_lower not in {s.casefold() for s in self.STATUS_VALID}:
            raise ValueError("Status harus 'Tersedia' atau 'Dipinjam'.")
        
        self.status = "Tersedia" if status_lower == "tersedia" else "Dipinjam"

    @property
    def pendengar_formatted(self):
        """Format angka pendengar (contoh: 1,500,000 / 1.5M)."""
        if self.pendengar >= 1_000_000:
            return f"{self.pendengar / 1_000_000:.1f}M"
        if self.pendengar >= 1_000:
            return f"{self.pendengar / 1_000:.1f}K"
        return str(self.pendengar)

    def to_list(self):
        return [
            self.judul,
            self.penyanyi,
            self.album,
            self.genre,
            self.status,
            str(self.pendengar)
        ]

     me
    def to_dict(self):
        return {
            "judul": self.judul,
            "penyanyi": self.penyanyi,
            "album": self.album,
            "genre": self.genre,
            "status": self.status,
            "pendengar": str(self.pendengar)
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            judul=data.get("judul", ""),
            penyanyi=data.get("penyanyi", ""),
            album=data.get("album", ""),
            genre=data.get("genre", ""),
            status=data.get("status", "Tersedia"),
            pendengar=data.get("pendengar", 0)
    )
