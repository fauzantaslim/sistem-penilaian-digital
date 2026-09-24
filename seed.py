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
            {'jawaban': 'x = 5 dan y = 10 diperoleh dengan substitusi persamaan linear dua variabel', 'bobot': 4.0},
            {'jawaban': 'Luas lingkaran adalah pi kali jari-jari kuadrat yaitu phi r pangkat dua', 'bobot': 4.0},
            {'jawaban': 'Teorema Pythagoras menyatakan sisi miring kuadrat sama dengan jumlah kuadrat dua sisi lainnya', 'bobot': 4.0},
            {'jawaban': 'Volume kubus adalah sisi pangkat tiga atau s kali s kali s', 'bobot': 4.0},
            {'jawaban': 'FPB dicari menggunakan faktorisasi prima kemudian ambil faktor terkecil', 'bobot': 4.0},
        ]
    },
    {
        'nama': 'Bahasa Indonesia',
        'kode': 'BIND',
        'deskripsi': 'Mata Pelajaran Bahasa Indonesia',
        'kunci': [
            {'jawaban': 'Majas personifikasi adalah gaya bahasa yang memberikan sifat manusia kepada benda mati', 'bobot': 4.0},
            {'jawaban': 'Kalimat deduktif adalah kalimat yang gagasan utamanya terletak di awal paragraf', 'bobot': 4.0},
            {'jawaban': 'Teks eksposisi bertujuan untuk memaparkan informasi secara objektif dan faktual kepada pembaca', 'bobot': 4.0},
            {'jawaban': 'Sinonim adalah kata yang memiliki makna sama atau hampir sama dengan kata lain', 'bobot': 4.0},
            {'jawaban': 'Paragraf argumentasi berisi pendapat yang disertai alasan dan bukti yang kuat', 'bobot': 4.0},
        ]
    },
    {
        'nama': 'Ilmu Pengetahuan Alam',
        'kode': 'IPA',
        'deskripsi': 'Mata Pelajaran Terpadu IPA',
        'kunci': [
            {'jawaban': 'Fotosintesis adalah proses pembuatan makanan oleh tumbuhan menggunakan cahaya matahari menghasilkan oksigen', 'bobot': 4.0},
            {'jawaban': 'Gaya tarik bumi disebut gravitasi yang menyebabkan benda jatuh ke bawah', 'bobot': 4.0},
            {'jawaban': 'Sel adalah unit terkecil penyusun makhluk hidup yang terdiri atas membran sel inti sel dan sitoplasma', 'bobot': 4.0},
            {'jawaban': 'Magnet memiliki dua kutub yaitu kutub utara dan kutub selatan yang saling tarik menarik bila berbeda', 'bobot': 4.0},
            {'jawaban': 'Ekosistem terdiri dari komponen biotik dan abiotik yang saling berinteraksi membentuk keseimbangan', 'bobot': 4.0},
        ]
    },
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
