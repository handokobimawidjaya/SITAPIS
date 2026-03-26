# Migration to remove master_surat field and add jenis_naskah/klasifikasi

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surat', '0002_surat_jenis_naskah_surat_klasifikasi'),
        ('master', '0006_alter_mastersurat_jenis_naskah_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surat',
            name='master_surat',
        ),
    ]
