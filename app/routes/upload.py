import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import LembarJawaban, Siswa, MataPelajaran

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    siswa_list = Siswa.query.order_by(Siswa.nama).all()
    mapel_list = MataPelajaran.query.order_by(MataPelajaran.nama).all()
    page       = request.args.get('page', 1, type=int)
    history    = LembarJawaban.query.order_by(LembarJawaban.uploaded_at.desc()).paginate(page=page, per_page=10, error_out=False)

    if request.method == 'POST':
        siswa_id = request.form.get('siswa_id', type=int)
        mapel_id = request.form.get('mapel_id', type=int)
        files    = request.files.getlist('files')

        if not siswa_id or not mapel_id:
            flash('Siswa dan mata pelajaran wajib dipilih.', 'danger')
            return render_template('upload/index.html', title='Upload Lembar Jawaban',
                                   siswa_list=siswa_list, mapel_list=mapel_list, history=history)

        if not files or all(f.filename == '' for f in files):
            flash('Pilih minimal satu file gambar untuk diupload.', 'danger')
            return render_template('upload/index.html', title='Upload Lembar Jawaban',
                                   siswa_list=siswa_list, mapel_list=mapel_list, history=history)

        uploaded_count = 0
        errors         = []

        for file in files:
            if file.filename == '':
                continue
            if not allowed_file(file.filename):
                errors.append(f'{file.filename}: format tidak didukung (gunakan JPG/PNG).')
                continue

            # Nama file unik agar tidak bentrok
            ext      = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            lembar = LembarJawaban(
                siswa_id  = siswa_id,
                mapel_id  = mapel_id,
                filename  = secure_filename(file.filename),
                file_path = filepath,
                status    = 'pending'
            )
            db.session.add(lembar)
            uploaded_count += 1

        db.session.commit()

        if uploaded_count:
            flash(f'{uploaded_count} file berhasil diupload dan menunggu diproses.', 'success')
        for err in errors:
            flash(err, 'warning')

        return redirect(url_for('upload.index'))

    return render_template('upload/index.html', title='Upload Lembar Jawaban',
                           siswa_list=siswa_list, mapel_list=mapel_list, history=history)


@upload_bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    lembar = LembarJawaban.query.get_or_404(id)
    # Hapus file dari disk
    if os.path.exists(lembar.file_path):
        os.remove(lembar.file_path)
    db.session.delete(lembar)
    db.session.commit()
    flash('Lembar jawaban berhasil dihapus.', 'success')
    return redirect(url_for('upload.index'))
