# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=100, verbose_name=b'Nom')),
                ('adresse', models.CharField(max_length=400, verbose_name=b'Adresse', blank=True)),
                ('compte', models.CharField(max_length=400, verbose_name=b'Adresse publique')),
                ('estRestaurant', models.BooleanField(default=False, verbose_name=b'Est un restaurant ?')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text=b'Le compte utilisateur associ\xc3\xa9 au profil')),
            ],
        ),
    ]
