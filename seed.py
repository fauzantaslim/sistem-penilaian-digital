from app import create_app, db
from app.models import User, Siswa, MataPelajaran, KunciJawaban

app = create_app()

# ─── Kelas SMP ────────────────────────────────────────────
KELAS_LIST = [
    'VII A', 'VII B', 'VII C', 'VII D',
    'VIII A', 'VIII B', 'VIII C', 'VIII D',
    'IX A', 'IX B', 'IX C', 'IX D',
]

# ─── Data Mata Pelajaran & Kunci Jawaban ──────────────────
MAPEL_DATA = [
    {
        'nama': 'Matematika',
        'kode': 'MTK',
        'deskripsi': 'Mata Pelajaran Matematika Wajib',
        'kunci': [
            {'tipe': 'PG', 'jawaban': 'A', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'B', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'C', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'D', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'E', 'bobot': 1.0},
            {'tipe': 'ESSAY', 'jawaban': 'x = 5 dan y = 10', 'bobot': 5.0},
            {'tipe': 'ESSAY', 'jawaban': 'Luas = 25 cm^2', 'bobot': 5.0}
        ]
    },
    {
        'nama': 'Bahasa Indonesia',
        'kode': 'BIND',
        'deskripsi': 'Mata Pelajaran Bahasa Indonesia',
        'kunci': [
            {'tipe': 'PG', 'jawaban': 'C', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'A', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'B', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'D', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'E', 'bobot': 1.0},
            {'tipe': 'ESSAY', 'jawaban': 'Majas Personifikasi', 'bobot': 3.0},
            {'tipe': 'ESSAY', 'jawaban': 'Kalimat Deduktif', 'bobot': 3.0}
        ]
    },
    {
        'nama': 'Ilmu Pengetahuan Alam',
        'kode': 'IPA',
        'deskripsi': 'Mata Pelajaran Terpadu IPA',
        'kunci': [
            {'tipe': 'PG', 'jawaban': 'B', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'D', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'A', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'C', 'bobot': 1.0},
            {'tipe': 'PG', 'jawaban': 'E', 'bobot': 1.0},
            {'tipe': 'ESSAY', 'jawaban': 'Fotosintesis menghasilkan Oksigen', 'bobot': 4.0},
            {'tipe': 'ESSAY', 'jawaban': 'Gaya tarik bumi (Gravitasi)', 'bobot': 4.0}
        ]
    }
]

# ─── Data Siswa ──────────────────────────────────────────
SISWA_DATA = [
    # Kelas VII A
    ('Ahmad Zaki Maulana',     '2401001', 'VII A'),
    ('Bella Saputri',          '2401002', 'VII A'),
    ('Dimas Arif Nugroho',     '2401003', 'VII A'),
    ('Elsa Permata Sari',      '2401004', 'VII A'),
    # Kelas VII B
    ('Farhan Hidayat',         '2401005', 'VII B'),
    ('Gina Rahayu',            '2401006', 'VII B'),
    # Kelas VIII A
    ('Hendra Kusuma',          '2301001', 'VIII A'),
    ('Indah Lestari',          '2301002', 'VIII A'),
    ('Joko Susanto',           '2301003', 'VIII A'),
    ('Kirana Dewi',            '2301004', 'VIII A'),
    # Kelas VIII B
    ('Lutfi Andriyanto',       '2301005', 'VIII B'),
    ('Maya Sari Ningrum',      '2301006', 'VIII B'),
    # Kelas IX A
    ('Naufal Rizki',           '2201001', 'IX A'),
    ('Oktaviani Putri',        '2201002', 'IX A'),
    ('Putra Ramadhan',         '2201003', 'IX A'),
    # Kelas IX B
    ('Rahma Wulandari',        '2201004', 'IX B'),
    ('Sandi Prayoga',          '2201005', 'IX B'),
    ('Tika Anggraeni',         '2201006', 'IX B'),
]


def seed_database():
    with app.app_context():
        print("=" * 55)
        print("  SEEDER SISTEM PENILAIAN DIGITAL - SMP")
        print("=" * 55)

        # ── 0. Reset Database ───────────────────────────────
        print("\n[RESET DATABASE]")
        db.drop_all()
        db.create_all()
        print("  [+] Semua tabel telah di-reset.")

        # ── 1. User Admin ──────────────────────────────────
        print("\n[USER]")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("  [+] Membuat user admin...")
            new_admin = User(
                username='admin',
                email='admin@sekolah.com',
                nama_lengkap='Administrator'
            )
            new_admin.set_password('admin')
            db.session.add(new_admin)
            db.session.flush()
            print("      Username : admin")
            print("      Password : admin")
        else:
            print("  [-] User admin sudah ada, dilewati.")

        # ── 2. Mata Pelajaran & Kunci Jawaban ─────────────
        print("\n[MATA PELAJARAN & KUNCI JAWABAN]")
        for mapel_info in MAPEL_DATA:
            mapel = MataPelajaran.query.filter_by(kode=mapel_info['kode']).first()
            if not mapel:
                print(f"  [+] {mapel_info['nama']} ({mapel_info['kode']})...")
                mapel = MataPelajaran(
                    nama=mapel_info['nama'],
                    kode=mapel_info['kode'],
                    deskripsi=mapel_info['deskripsi']
                )
                db.session.add(mapel)
                db.session.flush()

                kunci_list = [
                    KunciJawaban(
                        mapel_id=mapel.id, 
                        nomor_soal=i + 1, 
                        tipe=k['tipe'],
                        jawaban_benar=k['jawaban'],
                        bobot=k['bobot']
                    )
                    for i, k in enumerate(mapel_info['kunci'])
                ]
                db.session.add_all(kunci_list)
                print(f"      -> {len(kunci_list)} kunci jawaban ditambahkan.")
            else:
                print(f"  [-] {mapel_info['nama']} sudah ada, dilewati.")

        # ── 3. Siswa ──────────────────────────────────────
        print("\n[SISWA]")
        added = 0
        for nama, nis, kelas in SISWA_DATA:
            if not Siswa.query.filter_by(nis=nis).first():
                db.session.add(Siswa(nama=nama, nis=nis, kelas=kelas))
                added += 1

        if added:
            print(f"  [+] {added} siswa baru ditambahkan.")
        else:
            print("  [-] Semua data siswa sudah ada, dilewati.")

        # ── Commit ────────────────────────────────────────
        db.session.commit()
        print("\n" + "=" * 55)
        print("  [OK] Seeding selesai dengan sukses!")
        print("=" * 55)


if __name__ == '__main__':
    seed_database()
