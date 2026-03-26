# Migration to remove kategori and uses_klasifikasi_code from JenisNaskahDinas

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0007_cleanup_unused_models'),
    ]

    operations = [
        # Database is already updated (columns removed), just update Django's state
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterModelOptions(
                    name='jenisnaskahdinas',
                    options={'ordering': ['kode'], 'verbose_name': 'Jenis Naskah Dinas', 'verbose_name_plural': 'Jenis Naskah Dinas'},
                ),
                migrations.RemoveField(
                    model_name='jenisnaskahdinas',
                    name='kategori',
                ),
                migrations.RemoveField(
                    model_name='jenisnaskahdinas',
                    name='uses_klasifikasi_code',
                ),
            ],
            database_operations=[],
        ),
    ]
