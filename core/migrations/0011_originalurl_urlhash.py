# Generated by Django 3.2.9 on 2021-11-26 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='originalurl',
            name='urlHash',
            field=models.CharField(default='', max_length=200),
        ),
    ]
