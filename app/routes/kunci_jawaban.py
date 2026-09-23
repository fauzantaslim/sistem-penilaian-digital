from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models import KunciJawaban, MataPelajaran

kunci_bp = Blueprint('kunci', __name__, url_prefix='/kunci')

OPSI_JAWABAN = ['A', 'B', 'C', 'D', 'E']


@kunci_bp.route('/')
@login_required
def index():
    mapel_id  = request.args.get('mapel_id', type=int)
    mapel_list = MataPelajaran.query.order_by(MataPelajaran.nama).all()
    kunci_list = []

    if mapel_id:
        kunci_list = (
            KunciJawaban.query
            .filter_by(mapel_id=mapel_id)
            .order_by(KunciJawaban.nomor_soal)
            .all()
        )

    return render_template(
        'kunci_jawaban/index.html',
        title='Kelola Kunci Jawaban',
        mapel_list=mapel_list,
        kunci_list=kunci_list,
        selected_mapel=mapel_id,
        opsi=OPSI_JAWABAN
    )


@kunci_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    mapel_list = MataPelajaran.query.order_by(MataPelajaran.nama).all()

    if request.method == 'POST':
        mapel_id      = request.form.get('mapel_id', type=int)
        nomor_soal    = request.form.get('nomor_soal', type=int)
        jawaban_benar = request.form.get('jawaban_benar', '').strip().upper()

        if not mapel_id or not nomor_soal or not jawaban_benar:
            flash('Semua field wajib diisi.', 'danger')
            return render_template('kunci_jawaban/tambah.html', title='Tambah Kunci Jawaban',
                                   mapel_list=mapel_list, opsi=OPSI_JAWABAN)

        if jawaban_benar not in OPSI_JAWABAN:
            flash('Jawaban benar harus salah satu dari A, B, C, D, E.', 'danger')
            return render_template('kunci_jawaban/tambah.html', title='Tambah Kunci Jawaban',
                                   mapel_list=mapel_list, opsi=OPSI_JAWABAN)

        existing = KunciJawaban.query.filter_by(mapel_id=mapel_id, nomor_soal=nomor_soal).first()
        if existing:
            flash(f'Kunci jawaban untuk soal nomor {nomor_soal} sudah ada.', 'warning')
            return render_template('kunci_jawaban/tambah.html', title='Tambah Kunci Jawaban',
                                   mapel_list=mapel_list, opsi=OPSI_JAWABAN)

        kunci = KunciJawaban(mapel_id=mapel_id, nomor_soal=nomor_soal, jawaban_benar=jawaban_benar)
        db.session.add(kunci)
        db.session.commit()
        flash(f'Kunci jawaban soal {nomor_soal} berhasil ditambahkan.', 'success')
        return redirect(url_for('kunci.index', mapel_id=mapel_id))

    return render_template('kunci_jawaban/tambah.html', title='Tambah Kunci Jawaban',
                           mapel_list=mapel_list, opsi=OPSI_JAWABAN)


@kunci_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    kunci      = KunciJawaban.query.get_or_404(id)
    mapel_list = MataPelajaran.query.order_by(MataPelajaran.nama).all()

    if request.method == 'POST':
        jawaban_benar = request.form.get('jawaban_benar', '').strip().upper()

        if jawaban_benar not in OPSI_JAWABAN:
            flash('Jawaban benar harus salah satu dari A, B, C, D, E.', 'danger')
            return render_template('kunci_jawaban/edit.html', title='Edit Kunci Jawaban',
                                   kunci=kunci, mapel_list=mapel_list, opsi=OPSI_JAWABAN)

        kunci.jawaban_benar = jawaban_benar
        db.session.commit()
        flash(f'Kunci jawaban soal {kunci.nomor_soal} berhasil diperbarui.', 'success')
        return redirect(url_for('kunci.index', mapel_id=kunci.mapel_id))

    return render_template('kunci_jawaban/edit.html', title='Edit Kunci Jawaban',
                           kunci=kunci, mapel_list=mapel_list, opsi=OPSI_JAWABAN)


@kunci_bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    kunci = KunciJawaban.query.get_or_404(id)
    mapel_id = kunci.mapel_id
    db.session.delete(kunci)
    db.session.commit()
    flash(f'Kunci jawaban soal {kunci.nomor_soal} berhasil dihapus.', 'success')
    return redirect(url_for('kunci.index', mapel_id=mapel_id))
