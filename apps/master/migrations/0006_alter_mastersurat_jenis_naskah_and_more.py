# Generated manually to make jenis_naskah and klasifikasi nullable

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_seed_tata_naskah_dinas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastersurat',
            name='jenis_naskah',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master.jenisnaskahdinas', verbose_name='Jenis Naskah Dinas'),
        ),
        migrations.AlterField(
            model_name='mastersurat',
            name='klasifikasi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master.klasifikasiarsip', verbose_name='Klasifikasi Arsip'),
        ),
    ]
