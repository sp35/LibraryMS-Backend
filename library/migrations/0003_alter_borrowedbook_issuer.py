# Generated by Django 3.2.8 on 2021-10-06 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20211006_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='issuer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='library.librarian'),
        ),
    ]