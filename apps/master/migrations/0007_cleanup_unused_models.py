# Migration to clean up unused models and fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0006_alter_mastersurat_jenis_naskah_and_more'),
    ]

    operations = [
        # Create NomorSuratCounter model
        migrations.CreateModel(
            name='NomorSuratCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tahun', models.PositiveIntegerField(verbose_name='Tahun')),
                ('last_number', models.PositiveIntegerField(default=0, verbose_name='Nomor Terakhir')),
                ('jenis_naskah', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='master.jenisnaskahdinas', verbose_name='Jenis Naskah Dinas')),
                ('satker', models.ForeignKey(blank=True, help_text='Null = KPU Pusat', null=True, on_delete=django.db.models.deletion.PROTECT, to='master.wilayah', verbose_name='Satuan Kerja')),
            ],
            options={
                'verbose_name': 'Counter Nomor Surat',
                'verbose_name_plural': 'Counter Nomor Surat',
                'ordering': ['-tahun', 'jenis_naskah'],
                'unique_together': {('jenis_naskah', 'satker', 'tahun')},
            },
        ),
        # Delete unused models
        migrations.DeleteModel(
            name='Departemen',
        ),
        migrations.DeleteModel(
            name='MasterSurat',
        ),
        migrations.DeleteModel(
            name='PejabatPenandatangan',
        ),
        # Remove unique_together constraint from UnitKerja
        migrations.AlterUniqueTogether(
            name='unitkerja',
            unique_together=set(),
        ),
        # Remove fields from UnitKerja
        migrations.RemoveField(
            model_name='unitkerja',
            name='level',
        ),
        migrations.RemoveField(
            model_name='unitkerja',
            name='parent',
        ),
    ]
