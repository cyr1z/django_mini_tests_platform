# Generated by Django 3.1.4 on 2021-01-12 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_testsuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsuser',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatar.png', null=True, upload_to='avatars', verbose_name='avatar'),
        ),
    ]
