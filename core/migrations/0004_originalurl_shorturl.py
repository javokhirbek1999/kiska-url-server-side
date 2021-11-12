# Generated by Django 3.2.9 on 2021-11-12 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_user_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('shorten_count', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.URLField()),
                ('visit_count', models.IntegerField()),
                ('original_url', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.originalurl')),
            ],
        ),
    ]