# Generated by Django 3.2.5 on 2021-07-24 21:36

from django.db import migrations, models
import objetos.validators


class Migration(migrations.Migration):

    dependencies = [
        ('objetos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='objeto',
            old_name='SKU',
            new_name='sku',
        ),
        migrations.AlterField(
            model_name='objeto',
            name='costo',
            field=models.FloatField(validators=[objetos.validators.validate_costo]),
        ),
    ]
