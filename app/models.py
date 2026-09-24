from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager


# ─────────────────────────────────────────────
# User Loader for Flask-Login
# ─────────────────────────────────────────────
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────────────────────────
# Model: User (Guru)
# ─────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(80), unique=True, nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    nama_lengkap = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ─────────────────────────────────────────────
# Model: Siswa
# ─────────────────────────────────────────────
class Siswa(db.Model):
    __tablename__ = 'siswa'

    id         = db.Column(db.Integer, primary_key=True)
    nama       = db.Column(db.String(150), nullable=False)
    nis        = db.Column(db.String(20), unique=True, nullable=False)
    kelas      = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lembar_jawaban = db.relationship('LembarJawaban', backref='siswa', lazy=True)

    def __repr__(self):
        return f'<Siswa {self.nama} ({self.nis})>'


# ─────────────────────────────────────────────
# Model: Mata Pelajaran
# ─────────────────────────────────────────────
class MataPelajaran(db.Model):
    __tablename__ = 'mata_pelajaran'

    id         = db.Column(db.Integer, primary_key=True)
    nama       = db.Column(db.String(100), nullable=False)
    kode       = db.Column(db.String(20), unique=True, nullable=False)
    deskripsi  = db.Column(db.Text, nullable=True)

    kunci_jawaban  = db.relationship('KunciJawaban', backref='mata_pelajaran', lazy=True, cascade='all, delete-orphan')
    lembar_jawaban = db.relationship('LembarJawaban', backref='mata_pelajaran', lazy=True)

    def __repr__(self):
        return f'<MataPelajaran {self.kode} - {self.nama}>'


# ─────────────────────────────────────────────
# Model: Kunci Jawaban
# ─────────────────────────────────────────────
class KunciJawaban(db.Model):
    __tablename__ = 'kunci_jawaban'

    id            = db.Column(db.Integer, primary_key=True)
    mapel_id      = db.Column(db.Integer, db.ForeignKey('mata_pelajaran.id'), nullable=False)
    nomor_soal    = db.Column(db.Integer, nullable=False)
    jawaban_benar = db.Column(db.String(1), nullable=False)  # A, B, C, D, E
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('mapel_id', 'nomor_soal', name='uq_mapel_nomor'),
    )

    def __repr__(self):
        return f'<KunciJawaban Soal {self.nomor_soal}: {self.jawaban_benar}>'


# ─────────────────────────────────────────────
# Model: Lembar Jawaban
# ─────────────────────────────────────────────
class LembarJawaban(db.Model):
    __tablename__ = 'lembar_jawaban'

    id          = db.Column(db.Integer, primary_key=True)
    siswa_id    = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    mapel_id    = db.Column(db.Integer, db.ForeignKey('mata_pelajaran.id'), nullable=False)
    filename    = db.Column(db.String(255), nullable=False)
    file_path   = db.Column(db.String(500), nullable=False)
    status      = db.Column(db.String(20), default='pending')  # pending, processing, done, error
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    hasil_penilaian = db.relationship('HasilPenilaian', backref='lembar_jawaban', lazy=True, uselist=False)

    def __repr__(self):
        return f'<LembarJawaban {self.filename} [{self.status}]>'


# ─────────────────────────────────────────────
# Model: Hasil Penilaian
# ─────────────────────────────────────────────
class HasilPenilaian(db.Model):
    __tablename__ = 'hasil_penilaian'

    id               = db.Column(db.Integer, primary_key=True)
    lembar_id        = db.Column(db.Integer, db.ForeignKey('lembar_jawaban.id'), nullable=False)
    skor             = db.Column(db.Float, nullable=True)
    detail_jawaban   = db.Column(db.Text, nullable=True)  # JSON string: {"1": "A", "2": "B", ...}
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<HasilPenilaian Skor={self.skor}>'
