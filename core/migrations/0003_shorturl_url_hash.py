# Generated by Django 3.2.9 on 2021-11-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211115_0627'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='url_hash',
            field=models.CharField(default='', max_length=200),
        ),
    ]