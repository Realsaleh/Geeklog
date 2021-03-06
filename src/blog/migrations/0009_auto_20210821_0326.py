# Generated by Django 3.1.5 on 2021-08-20 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_post_hits'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostHit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.ipaddress')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='hits', through='blog.PostHit', to='blog.IPAddress', verbose_name='بازدیدها'),
        ),
    ]
