# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_auto_20260407_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomorsuratcounter',
            name='jenis_naskah',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='master.jenisnaskahdinas', verbose_name='Jenis Naskah Dinas'),
        ),
    ]
