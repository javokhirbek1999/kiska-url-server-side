# Generated by Django 3.2.9 on 2021-11-27 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_originalurl_visited'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShortURL',
        ),
    ]
