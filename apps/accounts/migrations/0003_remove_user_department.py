# Migration to remove department field from User

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_satker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
    ]
