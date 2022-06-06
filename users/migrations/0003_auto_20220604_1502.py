# Generated by Django 3.1.14 on 2022-06-04 13:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_gameusers_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameusers',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='gameusers',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='gameusers',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='gameusers',
            name='id_user',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
