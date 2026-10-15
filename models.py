class Lagu:
    """Model data untuk satu entri koleksi Melodia."""

    KOLOM = ("judul", "penulis", "isbn", "status")
    STATUS_VALID = ("Tersedia", "Dipinjam")

    def __init__(
        self,
        judul,
        penulis,
        isbn,
        status="Tersedia"
    ):
        self.judul = str(judul).strip()
        self.penulis = str(penulis).strip()
        self.isbn = str(isbn).strip()
        self.status = str(status).strip()

        self.validasi()

    def validasi(self):
        """Memastikan data penting telah diisi."""
        if not self.judul:
            raise ValueError("Judul wajib diisi.")

        if not self.penulis:
            raise ValueError("Penulis wajib diisi.")

        if not self.isbn:
            raise ValueError("ISBN wajib diisi.")

        if self.status.casefold() not in {
            status.casefold() for status in self.STATUS_VALID
        }:
            raise ValueError(
                "Status harus Tersedia atau Dipinjam."
            )

        # Samakan penulisan status agar konsisten.
        if self.status.casefold() == "tersedia":
            self.status = "Tersedia"
        else:
            self.status = "Dipinjam"

    def to_list(self):
        """Mengubah objek menjadi daftar untuk CSV."""
        return [
            self.judul,
            self.penulis,
            self.isbn,
            self.status
        ]

    def to_dict(self):
        """Mengubah objek menjadi dictionary."""
        return {
            "judul": self.judul,
            "penulis": self.penulis,
            "isbn": self.isbn,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Membuat objek Lagu dari satu baris dictionary CSV."""
        return cls(
            judul=data.get("judul", ""),
            penulis=data.get("penulis", ""),
            isbn=data.get("isbn", ""),
            status=data.get("status", "Tersedia")
        )

    def __str__(self):
        return (
            f"{self.judul} — {self.penulis} "
            f"(ISBN: {self.isbn}) [{self.status}]"
        )

    def __repr__(self):
        return (
            f"Lagu(judul={self.judul!r}, "
            f"penulis={self.penulis!r}, "
            f"isbn={self.isbn!r}, "
            f"status={self.status!r})"
        )


class Buku:
    """
    Model kompatibilitas untuk kode lama.
    Tetap tersedia jika program lain masih memakai Buku.
    """

    def __init__(
        self,
        judul,
        penulis,
        isbn,
        status="Tersedia"
    ):
        self.judul = str(judul).strip()
        self.penulis = str(penulis).strip()
        self.isbn = str(isbn).strip()
        self.status = str(status).strip()

    def to_list(self):
        return [
            self.judul,
            self.penulis,
            self.isbn,
            self.status
        ]

    def __str__(self):
        return (
            f"{self.judul} oleh {self.penulis} "
            f"(ISBN: {self.isbn}) - {self.status}"
        )


class Anggota:
    """Model data anggota perpustakaan."""

    def __init__(self, id_anggota, nama, kelas, no_hp):
        self.id = str(id_anggota).strip()
        self.nama = str(nama).strip()
        self.kelas = str(kelas).strip()
        self.no_hp = str(no_hp).strip()

    def to_list(self):
        return [
            self.id,
            self.nama,
            self.kelas,
            self.no_hp
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "kelas": self.kelas,
            "no_hp": self.no_hp
        }

    def __str__(self):
        return f"{self.nama} ({self.id}) - Kelas {self.kelas}"