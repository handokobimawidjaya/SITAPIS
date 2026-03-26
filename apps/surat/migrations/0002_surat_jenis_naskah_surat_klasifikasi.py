# Migration to add jenis_naskah and klasifikasi fields to Surat model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surat', '0001_initial'),
        ('master', '0006_alter_mastersurat_jenis_naskah_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='surat',
            name='jenis_naskah',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master.jenisnaskahdinas', verbose_name='Jenis Naskah Dinas'),
        ),
        migrations.AddField(
            model_name='surat',
            name='klasifikasi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master.klasifikasiarsip', verbose_name='Klasifikasi Arsip'),
        ),
    ]
