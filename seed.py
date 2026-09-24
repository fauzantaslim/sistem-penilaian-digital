from app import create_app, db
from app.models import User

app = create_app()

def seed_users():
    with app.app_context():
        # Cek apakah user admin sudah ada
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Membuat user admin...")
            new_admin = User(
                username='admin',
                email='admin@sekolah.com',
                nama_lengkap='Administrator'
            )
            new_admin.set_password('admin')
            db.session.add(new_admin)
            db.session.commit()
            print("Berhasil! User admin telah dibuat.")
            print("Username: admin")
            print("Password: admin")
        else:
            print("User admin sudah ada di database.")

if __name__ == '__main__':
    seed_users()
