import os
from flask import Flask, render_template
from config import Config
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Init Extensions ──────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # ── Ensure upload folder exists ───────────────
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # ── Register Blueprints ───────────────────────
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.siswa import siswa_bp
    from app.routes.mata_pelajaran import mapel_bp
    from app.routes.kunci_jawaban import kunci_bp
    from app.routes.upload import upload_bp
    from app.routes.laporan import laporan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(siswa_bp)
    app.register_blueprint(mapel_bp)
    app.register_blueprint(kunci_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(laporan_bp)

    # ── Error Handlers ────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app
