# Generated by Django 3.1.7 on 2021-03-20 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news_api', '0002_comments_history_hotword_newssimilar_recommend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommend',
            name='newsid',
        ),
        migrations.AddField(
            model_name='recommend',
            name='newsid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='news_api.newsdetail'),
            preserve_default=False,
        ),
    ]
