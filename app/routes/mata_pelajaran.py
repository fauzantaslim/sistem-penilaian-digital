from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models import MataPelajaran

mapel_bp = Blueprint('mapel', __name__, url_prefix='/mapel')


@mapel_bp.route('/')
@login_required
def index():
    search     = request.args.get('q', '').strip()
    page       = request.args.get('page', 1, type=int)
    query      = MataPelajaran.query
    if search:
        query = query.filter(
            (MataPelajaran.nama.ilike(f'%{search}%')) |
            (MataPelajaran.kode.ilike(f'%{search}%'))
        )
    mapel_list = query.order_by(MataPelajaran.nama).paginate(page=page, per_page=10, error_out=False)
    return render_template('mata_pelajaran/index.html', title='Kelola Mata Pelajaran', mapel_list=mapel_list, search=search)


@mapel_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        nama      = request.form.get('nama', '').strip()
        kode      = request.form.get('kode', '').strip().upper()
        deskripsi = request.form.get('deskripsi', '').strip()

        if not nama or not kode:
            flash('Nama dan kode mata pelajaran wajib diisi.', 'danger')
            return render_template('mata_pelajaran/tambah.html', title='Tambah Mata Pelajaran')

        if MataPelajaran.query.filter_by(kode=kode).first():
            flash(f'Kode {kode} sudah digunakan.', 'warning')
            return render_template('mata_pelajaran/tambah.html', title='Tambah Mata Pelajaran')

        mapel = MataPelajaran(nama=nama, kode=kode, deskripsi=deskripsi)
        db.session.add(mapel)
        db.session.commit()
        flash(f'Mata pelajaran {nama} berhasil ditambahkan.', 'success')
        return redirect(url_for('mapel.index'))

    return render_template('mata_pelajaran/tambah.html', title='Tambah Mata Pelajaran')


@mapel_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    mapel = MataPelajaran.query.get_or_404(id)

    if request.method == 'POST':
        nama      = request.form.get('nama', '').strip()
        kode      = request.form.get('kode', '').strip().upper()
        deskripsi = request.form.get('deskripsi', '').strip()

        if not nama or not kode:
            flash('Nama dan kode mata pelajaran wajib diisi.', 'danger')
            return render_template('mata_pelajaran/edit.html', title='Edit Mata Pelajaran', mapel=mapel)

        existing = MataPelajaran.query.filter_by(kode=kode).first()
        if existing and existing.id != id:
            flash(f'Kode {kode} sudah digunakan mata pelajaran lain.', 'warning')
            return render_template('mata_pelajaran/edit.html', title='Edit Mata Pelajaran', mapel=mapel)

        mapel.nama      = nama
        mapel.kode      = kode
        mapel.deskripsi = deskripsi
        db.session.commit()
        flash(f'Mata pelajaran {nama} berhasil diperbarui.', 'success')
        return redirect(url_for('mapel.index'))

    return render_template('mata_pelajaran/edit.html', title='Edit Mata Pelajaran', mapel=mapel)


@mapel_bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    mapel = MataPelajaran.query.get_or_404(id)
    nama  = mapel.nama
    db.session.delete(mapel)
    db.session.commit()
    flash(f'Mata pelajaran {nama} berhasil dihapus.', 'success')
    return redirect(url_for('mapel.index'))
