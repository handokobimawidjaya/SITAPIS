# Migration to add satker field to User model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('master', '0006_alter_mastersurat_jenis_naskah_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='satker',
            field=models.ForeignKey(blank=True, help_text='KPU Provinsi/Kabupaten/Kota tempat user bertugas', null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.wilayah', verbose_name='Satuan Kerja'),
        ),
    ]
