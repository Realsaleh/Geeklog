# Generated by Django 3.1.5 on 2021-03-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210207_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_special',
            field=models.BooleanField(default=False, verbose_name='پست ویژه'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('d', 'پیش نویس'), ('p', 'منتشرشده'), ('i', 'درحال بررسی'), ('b', 'رد شده')], max_length=1, verbose_name='وضعیت انتشار'),
        ),
    ]