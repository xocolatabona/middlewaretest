# Generated by Django 3.2.5 on 2021-07-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objetos', '0006_alter_objeto_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='corregida',
            field=models.BooleanField(default=False),
        ),
    ]
