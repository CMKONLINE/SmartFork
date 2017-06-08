# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='comment',
            field=models.TextField(max_length=500, verbose_name=b'Commentaire'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='liste',
            field=models.TextField(max_length=500, verbose_name=b'Liste Facture'),
        ),
    ]
