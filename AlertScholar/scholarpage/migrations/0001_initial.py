# Generated by Django 4.2.2 on 2023-07-23 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(null=True, upload_to='imagenes/', verbose_name='Imagen')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('cedula', models.CharField(max_length=11)),
                ('curso', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
                ('correo', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(null=True, upload_to='imagenes/', verbose_name='Imagen')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=11)),
                ('password', models.CharField(max_length=128)),
                ('correo', models.EmailField(max_length=100)),
            ],
        ),
    ]
