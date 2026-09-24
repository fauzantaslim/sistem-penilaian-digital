from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Selamat datang, {user.nama_lengkap or user.username}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Email atau password salah. Silakan coba lagi.', 'danger')

    return render_template('auth/login.html', title='Login')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username         = request.form.get('username', '').strip()
        nama_lengkap     = request.form.get('nama_lengkap', '').strip()
        email            = request.form.get('email', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validasi
        if not username or not email or not password or not nama_lengkap:
            flash('Semua field wajib diisi.', 'danger')
            return render_template('auth/register.html', title='Daftar')

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'danger')
            return render_template('auth/register.html', title='Daftar')

        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar. Gunakan email lain.', 'warning')
            return render_template('auth/register.html', title='Daftar')

        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan. Pilih username lain.', 'warning')
            return render_template('auth/register.html', title='Daftar')

        user = User(username=username, email=email, nama_lengkap=nama_lengkap or None)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Akun berhasil dibuat! Silakan login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Daftar Akun')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('auth.login'))
