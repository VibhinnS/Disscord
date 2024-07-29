# Generated by Django 5.0.7 on 2024-07-29 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disscord_servers', '0001_initial'),
        ('user', '0002_delete_servermembership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_servers', to='user.user'),
        ),
    ]
