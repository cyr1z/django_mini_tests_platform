# Generated by Django 3.1.4 on 2021-01-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0011_auto_20210112_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsuser',
            name='about',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
    ]