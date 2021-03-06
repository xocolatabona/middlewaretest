# Generated by Django 3.2.5 on 2021-07-24 21:27

from django.db import migrations, models
import objetos.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Objeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=300)),
                ('SKU', models.CharField(max_length=20, unique=True)),
                ('tags', models.TextField(validators=[objetos.validators.validate_tags])),
                ('costo', models.FloatField()),
                ('estatus', models.CharField(choices=[('AC', 'Active'), ('AR', 'Archived'), ('DR', 'Draft')], default='AC', max_length=2)),
                ('tallas', models.TextField(validators=[objetos.validators.validate_tallas])),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fecha_actualizacion', models.DateTimeField()),
            ],
        ),
    ]
