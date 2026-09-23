from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Siswa, MataPelajaran, LembarJawaban, HasilPenilaian

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_siswa  = Siswa.query.count()
    total_mapel  = MataPelajaran.query.count()
    total_proses = LembarJawaban.query.filter_by(status='done').count()
    total_pending = LembarJawaban.query.filter_by(status='pending').count()

    # Rata-rata skor dari semua hasil penilaian
    hasil_list = HasilPenilaian.query.filter(HasilPenilaian.skor.isnot(None)).all()
    rata_skor  = round(sum(h.skor for h in hasil_list) / len(hasil_list), 1) if hasil_list else 0

    # 10 penilaian terbaru
    penilaian_terbaru = (
        HasilPenilaian.query
        .join(HasilPenilaian.lembar_jawaban)
        .order_by(HasilPenilaian.created_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        'dashboard/index.html',
        title='Dashboard',
        total_siswa=total_siswa,
        total_mapel=total_mapel,
        total_proses=total_proses,
        total_pending=total_pending,
        rata_skor=rata_skor,
        penilaian_terbaru=penilaian_terbaru
    )
