"""
Data migration: seed all master data from SK KPU No. 1257/2024.

- KlasifikasiArsip: 19 top-level + sub-codes
- JenisNaskahDinas: 20 letter types
- UnitKerja: 14 bureaus
- Wilayah: 38 provinces
- PejabatPenandatangan: 6 official types
"""

from django.db import migrations


def seed_klasifikasi_arsip(apps, schema_editor):
    """Seed archive classification codes (Lampiran I)."""
    KlasifikasiArsip = apps.get_model('master', 'KlasifikasiArsip')

    # ── Substantif ──
    substantif = [
        ('PP', 'Persiapan Pemilu atau Pemilihan'),
        ('PL', 'Pelaksanaan Pemilu atau Pemilihan'),
        ('PY', 'Penyelesaian Pemilu atau Pemilihan'),
        ('PAW', 'Penggantian Antar Waktu'),
    ]
    for kode, nama in substantif:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'substantif'},
        )

    # Substantif sub-codes
    pp = KlasifikasiArsip.objects.get(kode='PP')
    pp_subs = [
        ('PP.01', 'Perencanaan Program dan Anggaran'),
        ('PP.02', 'Penataan Organisasi'),
        ('PP.03', 'Pendaftaran Pemantau dan Pemantauan'),
        ('PP.04', 'Pembentukan Badan Penyelenggara'),
        ('PP.05', 'Rapat Kerja dan Rapat Koordinasi'),
        ('PP.06', 'Sosialisasi, Bimtek, Penyuluhan, Publikasi, dan Pendidikan Pemilih'),
        ('PP.07', 'Pengelolaan Data dan Informasi'),
        ('PP.08', 'Logistik Penyelenggaraan Pemilu'),
        ('PP.09', 'Logistik Penyelenggaraan Pemilihan'),
    ]
    for kode, nama in pp_subs:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'substantif', 'parent': pp},
        )

    pl = KlasifikasiArsip.objects.get(kode='PL')
    pl_subs = [
        ('PL.01', 'Pelaksanaan Pemilu'),
        ('PL.02', 'Pelaksanaan Pemilihan'),
    ]
    for kode, nama in pl_subs:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'substantif', 'parent': pl},
        )

    py = KlasifikasiArsip.objects.get(kode='PY')
    py_subs = [
        ('PY.01', 'Penyelesaian Pemilu'),
        ('PY.02', 'Penyelesaian Pemilihan'),
    ]
    for kode, nama in py_subs:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'substantif', 'parent': py},
        )

    paw = KlasifikasiArsip.objects.get(kode='PAW')
    KlasifikasiArsip.objects.get_or_create(
        kode='PAW.01',
        defaults={
            'nama': 'Penggantian Antar Waktu dan Pengisian Anggota DPR, DPD, dan DPRD',
            'jenis': 'substantif',
            'parent': paw,
        },
    )

    # ── Fasilitatif ──
    fasilitatif = [
        ('PR', 'Perencanaan'),
        ('HK', 'Hukum'),
        ('ORT', 'Organisasi dan Ketatalaksanaan'),
        ('TU', 'Ketatausahaan dan Kearsipan'),
        ('RT', 'Kerumahtanggaan'),
        ('PK', 'Persidangan dan Keprotokolan'),
        ('HM', 'Kehumasan'),
        ('PUS', 'Kepustakaan'),
        ('PLB', 'Penelitian, Pengembangan, Pendidikan dan Pelatihan'),
        ('TIK', 'Teknologi Informasi dan Komunikasi'),
        ('PW', 'Pengawasan'),
        ('PBJ', 'Pengadaan Barang dan Jasa'),
        ('LPSE', 'Layanan Pengadaan Secara Elektronik'),
        ('SDM', 'Kepegawaian'),
        ('KU', 'Keuangan'),
    ]
    for kode, nama in fasilitatif:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif'},
        )

    # Fasilitatif sub-codes (level 2 only for commonly used ones)
    pr = KlasifikasiArsip.objects.get(kode='PR')
    for kode, nama in [
        ('PR.01', 'Pokok-Pokok Kebijakan'),
        ('PR.02', 'Rencana Kerja Tahunan'),
        ('PR.03', 'Penetapan/Kontrak Kinerja'),
        ('PR.04', 'Laporan'),
        ('PR.05', 'Dokumen Rapat Dengar Pendapat'),
        ('PR.06', 'Evaluasi Program'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': pr},
        )

    hk = KlasifikasiArsip.objects.get(kode='HK')
    for kode, nama in [
        ('HK.01', 'Program Legislasi'),
        ('HK.02', 'Peraturan KPU'),
        ('HK.03', 'Keputusan'),
        ('HK.04', 'Instruksi/Surat Edaran'),
        ('HK.05', 'Nota Kesepahaman/MoU dan Kerja Sama'),
        ('HK.06', 'Sosialisasi/Penyuluhan Pembinaan Hukum'),
        ('HK.07', 'Bantuan/Konsultasi Hukum/Advokasi'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': hk},
        )

    tu = KlasifikasiArsip.objects.get(kode='TU')
    for kode, nama in [
        ('TU.01', 'Persuratan'),
        ('TU.02', 'Kearsipan'),
        ('TU.03', 'Pengelolaan Informasi dan Dokumentasi'),
        ('TU.04', 'Ekspedisi dan Pengantar Surat'),
        ('TU.05', 'Penggandaan'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': tu},
        )

    sdm = KlasifikasiArsip.objects.get(kode='SDM')
    for kode, nama in [
        ('SDM.01', 'Formasi dan Bezetting'),
        ('SDM.02', 'Pengadaan dan Seleksi Pegawai'),
        ('SDM.03', 'Mutasi Jabatan dan Kepangkatan'),
        ('SDM.04', 'Kinerja dan Disiplin'),
        ('SDM.05', 'Penghargaan'),
        ('SDM.06', 'Peningkatan Kompetensi'),
        ('SDM.07', 'Kesejahteraan'),
        ('SDM.08', 'Pemeriksaan Kesehatan'),
        ('SDM.09', 'Berkas Perseorangan ASN'),
        ('SDM.10', 'Berkas Perseorangan Anggota KPU'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': sdm},
        )

    ku = KlasifikasiArsip.objects.get(kode='KU')
    for kode, nama in [
        ('KU.01', 'RAPBN'),
        ('KU.02', 'Penyusunan APBN'),
        ('KU.03', 'Pelaksanaan Anggaran'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': ku},
        )

    tik = KlasifikasiArsip.objects.get(kode='TIK')
    for kode, nama in [
        ('TIK.01', 'Pengembangan Aplikasi'),
        ('TIK.02', 'Infrastruktur Jaringan'),
        ('TIK.03', 'Pengelolaan Data Pemilu'),
        ('TIK.04', 'Keamanan Informasi'),
        ('TIK.05', 'Layanan Teknologi Informasi'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': tik},
        )

    rt = KlasifikasiArsip.objects.get(kode='RT')
    for kode, nama in [
        ('RT.01', 'Pengelolaan Aset dan Persediaan'),
        ('RT.02', 'Perjalanan Dinas'),
        ('RT.03', 'Pengurusan Kendaraan Dinas'),
        ('RT.04', 'Pemeliharaan Gedung dan Taman'),
        ('RT.05', 'Telekomunikasi'),
        ('RT.06', 'Pengelolaan Jaringan Listrik, Air, Telepon'),
        ('RT.07', 'Administrasi Penggunaan Fasilitas Kantor'),
        ('RT.08', 'Administrasi Penyediaan Konsumsi dan Akomodasi'),
        ('RT.09', 'Ketertiban dan Keamanan'),
        ('RT.10', 'Administrasi Pengelolaan Parkir'),
        ('RT.11', 'Administrasi Pakaian Dinas Pegawai'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': rt},
        )

    pk_obj = KlasifikasiArsip.objects.get(kode='PK')
    for kode, nama in [
        ('PK.01', 'Persidangan'),
        ('PK.02', 'Keprotokolan'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': pk_obj},
        )

    hm = KlasifikasiArsip.objects.get(kode='HM')
    for kode, nama in [
        ('HM.01', 'Dokumentasi/Liputan Kegiatan Dinas'),
        ('HM.02', 'Pengumpulan, Pengolahan, dan Penyajian Informasi'),
        ('HM.03', 'Hubungan KPU dengan Badan Pemerintahan/Instansi'),
        ('HM.04', 'Master Publikasi Media Cetak dan Elektronik'),
        ('HM.05', 'Duplikasi Publikasi Media Cetak dan Elektronik'),
        ('HM.06', 'Pameran/Sayembara/Lomba/Festival'),
        ('HM.07', 'Penghargaan/Tanda Kenang-Kenangan'),
        ('HM.08', 'Ucapan Terima Kasih, Selamat, Belasungkawa'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': hm},
        )

    pus = KlasifikasiArsip.objects.get(kode='PUS')
    for kode, nama in [
        ('PUS.01', 'Penyimpanan Deposit Bahan Pustaka'),
        ('PUS.02', 'Pengadaan dan Pengelolaan Bahan Pustaka'),
        ('PUS.03', 'Pembentukan Keanggotaan Perpustakaan'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': pus},
        )

    plb = KlasifikasiArsip.objects.get(kode='PLB')
    for kode, nama in [
        ('PLB.01', 'Penelitian dan Pengembangan'),
        ('PLB.02', 'Pendidikan dan Pelatihan'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': plb},
        )

    pw = KlasifikasiArsip.objects.get(kode='PW')
    for kode, nama in [
        ('PW.01', 'Audit Kinerja dan Keuangan'),
        ('PW.02', 'Reviu Laporan Keuangan'),
        ('PW.03', 'Pemeriksaan Dengan Tujuan Tertentu'),
        ('PW.04', 'Evaluasi'),
        ('PW.05', 'Pengaduan Masyarakat'),
        ('PW.06', 'Tindak Lanjut Hasil Pengawasan'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': pw},
        )

    pbj = KlasifikasiArsip.objects.get(kode='PBJ')
    for kode, nama in [
        ('PBJ.01', 'Perencanaan PBJ'),
        ('PBJ.02', 'Pemilihan Penyedia'),
        ('PBJ.03', 'Pelaksanaan Kontrak'),
        ('PBJ.04', 'Serah Terima Pekerjaan'),
        ('PBJ.05', 'Swakelola'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': pbj},
        )

    lpse = KlasifikasiArsip.objects.get(kode='LPSE')
    for kode, nama in [
        ('LPSE.01', 'Pengelolaan Sistem E-Procurement'),
        ('LPSE.02', 'Registrasi dan Verifikasi'),
        ('LPSE.03', 'Layanan Helpdesk'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': lpse},
        )

    ort = KlasifikasiArsip.objects.get(kode='ORT')
    for kode, nama in [
        ('ORT.01', 'Organisasi'),
        ('ORT.02', 'Ketatalaksanaan'),
        ('ORT.03', 'Pendayagunaan Aparatur Negara'),
        ('ORT.04', 'Reformasi Birokrasi'),
    ]:
        KlasifikasiArsip.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'jenis': 'fasilitatif', 'parent': ort},
        )


def seed_jenis_naskah(apps, schema_editor):
    """Seed letter type codes (Lampiran II)."""
    JenisNaskahDinas = apps.get_model('master', 'JenisNaskahDinas')

    types = [
        # Arahan - Pengaturan (no classification code in numbering)
        ('Peraturan', 'Peraturan KPU', 'arahan_pengaturan', False),
        ('Instruksi', 'Instruksi', 'arahan_pengaturan', False),
        ('SE', 'Surat Edaran', 'arahan_pengaturan', False),
        ('SOP', 'Standar Operasional Prosedur', 'arahan_pengaturan', False),
        # Arahan - Penetapan
        ('Keputusan', 'Keputusan', 'arahan_penetapan', False),
        # Arahan - Penugasan
        ('SPt', 'Surat Perintah', 'penugasan', True),
        ('ST', 'Surat Tugas', 'penugasan', True),
        # Korespondensi
        ('ND', 'Nota Dinas', 'korespondensi', True),
        ('LD', 'Lembar Disposisi', 'korespondensi', True),
        ('MM', 'Memorandum', 'korespondensi', True),
        ('SD', 'Surat Dinas', 'korespondensi', True),
        ('Und', 'Surat Undangan', 'korespondensi', True),
        # Khusus
        ('NK', 'Nota Kesepahaman', 'khusus', True),
        ('PKS', 'Perjanjian Kerja Sama', 'khusus', True),
        ('SU', 'Surat Kuasa', 'khusus', True),
        ('BA', 'Berita Acara', 'khusus', True),
        ('Kt', 'Surat Keterangan', 'khusus', True),
        ('SR', 'Surat Pengantar', 'khusus', True),
        ('Pu', 'Pengumuman', 'khusus', True),
        ('Sg', 'Surat Panggilan', 'khusus', True),
        ('Rk', 'Rekomendasi', 'khusus', True),
        ('SP', 'Surat Peringatan', 'khusus', True),
        ('LP', 'Laporan', 'khusus', True),
        ('TI', 'Telaah', 'khusus', True),
        ('NT', 'Notula', 'khusus', True),
    ]
    for kode, nama, kategori, uses_code in types:
        JenisNaskahDinas.objects.get_or_create(
            kode=kode,
            defaults={
                'nama': nama,
                'kategori': kategori,
                'uses_klasifikasi_code': uses_code,
            },
        )


def seed_unit_kerja(apps, schema_editor):
    """Seed organizational units - Biro level (Lampiran II)."""
    UnitKerja = apps.get_model('master', 'UnitKerja')

    biros = [
        ('01', 'Biro Perencanaan dan Organisasi'),
        ('02', 'Biro Keuangan'),
        ('03', 'Biro Umum'),
        ('04', 'Biro Sumber Daya Manusia'),
        ('05', 'Biro Pengadaan Barang/Jasa dan BMN'),
        ('06', 'Biro Teknis Penyelenggaraan Pemilu'),
        ('07', 'Biro Logistik'),
        ('08', 'Biro Hukum'),
        ('09', 'Biro Partisipasi dan Hubungan Masyarakat'),
        ('10', 'Inspektorat Wilayah I'),
        ('11', 'Inspektorat Wilayah II'),
        ('12', 'Inspektorat Wilayah III'),
        ('13', 'Pusat Data dan Teknologi Informasi'),
        ('14', 'Pusat Pengembangan Kompetensi SDM'),
    ]
    for kode, nama in biros:
        UnitKerja.objects.get_or_create(
            kode=kode,
            parent=None,
            defaults={'nama': nama, 'level': 'biro'},
        )


def seed_wilayah(apps, schema_editor):
    """Seed province-level regions (Lampiran II)."""
    Wilayah = apps.get_model('master', 'Wilayah')

    provinces = [
        ('11', 'Aceh'),
        ('12', 'Sumatera Utara'),
        ('13', 'Sumatera Barat'),
        ('14', 'Riau'),
        ('15', 'Jambi'),
        ('16', 'Sumatera Selatan'),
        ('17', 'Bengkulu'),
        ('18', 'Lampung'),
        ('19', 'Kepulauan Bangka Belitung'),
        ('21', 'Kepulauan Riau'),
        ('31', 'DKI Jakarta'),
        ('32', 'Jawa Barat'),
        ('33', 'Jawa Tengah'),
        ('34', 'DI Yogyakarta'),
        ('35', 'Jawa Timur'),
        ('36', 'Banten'),
        ('51', 'Bali'),
        ('52', 'Nusa Tenggara Barat'),
        ('53', 'Nusa Tenggara Timur'),
        ('61', 'Kalimantan Barat'),
        ('62', 'Kalimantan Tengah'),
        ('63', 'Kalimantan Selatan'),
        ('64', 'Kalimantan Timur'),
        ('65', 'Kalimantan Utara'),
        ('71', 'Sulawesi Utara'),
        ('72', 'Sulawesi Tengah'),
        ('73', 'Sulawesi Selatan'),
        ('74', 'Sulawesi Tenggara'),
        ('75', 'Gorontalo'),
        ('76', 'Sulawesi Barat'),
        ('81', 'Maluku'),
        ('82', 'Maluku Utara'),
        ('91', 'Papua'),
        ('92', 'Papua Barat'),
        ('93', 'Papua Selatan'),
        ('94', 'Papua Tengah'),
        ('95', 'Papua Pegunungan'),
        ('96', 'Papua Barat Daya'),
    ]
    for kode, nama in provinces:
        Wilayah.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama, 'level': 'provinsi'},
        )


def seed_pejabat(apps, schema_editor):
    """Seed signing official type codes (Lampiran II)."""
    PejabatPenandatangan = apps.get_model('master', 'PejabatPenandatangan')

    officials = [
        ('K', 'Ketua/Anggota KPU'),
        ('S', 'Sekretaris Jenderal KPU'),
        ('D', 'Deputi'),
        ('IR', 'Inspektur Utama'),
        ('Sek-Prov', 'Sekretaris KPU Provinsi'),
        ('Sek-Kab/Kota', 'Sekretaris KPU Kabupaten/Kota'),
    ]
    for kode, nama in officials:
        PejabatPenandatangan.objects.get_or_create(
            kode=kode,
            defaults={'nama': nama},
        )


def noop(apps, schema_editor):
    """No-op reverse migration."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_auto_20260325_1131'),
    ]

    operations = [
        migrations.RunPython(seed_klasifikasi_arsip, noop),
        migrations.RunPython(seed_jenis_naskah, noop),
        migrations.RunPython(seed_unit_kerja, noop),
        migrations.RunPython(seed_wilayah, noop),
        migrations.RunPython(seed_pejabat, noop),
    ]
