# Generated by Django 4.1 on 2022-08-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='admin',
            field=models.PositiveSmallIntegerField(choices=[(0, '否'), (1, '是')], default=0, verbose_name='管理员'),
            preserve_default=False,
        ),
    ]