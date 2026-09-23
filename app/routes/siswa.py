from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models import Siswa

siswa_bp = Blueprint('siswa', __name__, url_prefix='/siswa')


@siswa_bp.route('/')
@login_required
def index():
    search = request.args.get('q', '').strip()
    page   = request.args.get('page', 1, type=int)

    query = Siswa.query
    if search:
        query = query.filter(
            (Siswa.nama.ilike(f'%{search}%')) |
            (Siswa.nis.ilike(f'%{search}%'))  |
            (Siswa.kelas.ilike(f'%{search}%'))
        )

    siswa_list = query.order_by(Siswa.nama).paginate(page=page, per_page=10, error_out=False)
    return render_template('siswa/index.html', title='Kelola Siswa', siswa_list=siswa_list, search=search)


@siswa_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        nama  = request.form.get('nama', '').strip()
        nis   = request.form.get('nis', '').strip()
        kelas = request.form.get('kelas', '').strip()

        if not nama or not nis or not kelas:
            flash('Semua field wajib diisi.', 'danger')
            return render_template('siswa/tambah.html', title='Tambah Siswa')

        if Siswa.query.filter_by(nis=nis).first():
            flash(f'NIS {nis} sudah terdaftar.', 'warning')
            return render_template('siswa/tambah.html', title='Tambah Siswa')

        siswa = Siswa(nama=nama, nis=nis, kelas=kelas)
        db.session.add(siswa)
        db.session.commit()
        flash(f'Siswa {nama} berhasil ditambahkan.', 'success')
        return redirect(url_for('siswa.index'))

    return render_template('siswa/tambah.html', title='Tambah Siswa')


@siswa_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    siswa = Siswa.query.get_or_404(id)

    if request.method == 'POST':
        nama  = request.form.get('nama', '').strip()
        nis   = request.form.get('nis', '').strip()
        kelas = request.form.get('kelas', '').strip()

        if not nama or not nis or not kelas:
            flash('Semua field wajib diisi.', 'danger')
            return render_template('siswa/edit.html', title='Edit Siswa', siswa=siswa)

        existing = Siswa.query.filter_by(nis=nis).first()
        if existing and existing.id != id:
            flash(f'NIS {nis} sudah digunakan siswa lain.', 'warning')
            return render_template('siswa/edit.html', title='Edit Siswa', siswa=siswa)

        siswa.nama  = nama
        siswa.nis   = nis
        siswa.kelas = kelas
        db.session.commit()
        flash(f'Data siswa {nama} berhasil diperbarui.', 'success')
        return redirect(url_for('siswa.index'))

    return render_template('siswa/edit.html', title='Edit Siswa', siswa=siswa)


@siswa_bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    siswa = Siswa.query.get_or_404(id)
    nama  = siswa.nama
    db.session.delete(siswa)
    db.session.commit()
    flash(f'Siswa {nama} berhasil dihapus.', 'success')
    return redirect(url_for('siswa.index'))
