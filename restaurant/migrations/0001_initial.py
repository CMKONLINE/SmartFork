# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0002_auto_20170402_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=500, verbose_name=b'Commentaire')),
                ('note', models.IntegerField(default=5)),
                ('date', models.DateTimeField(auto_now=True)),
                ('block', models.CharField(max_length=500, verbose_name=b'Block', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('liste', models.CharField(max_length=500, verbose_name=b'Liste Facture')),
                ('montant', models.FloatField(default=0, verbose_name=b'Montant Facture en ETH')),
                ('date', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(related_name='client', to='utilisateur.UserProfile')),
                ('restaurateur', models.ForeignKey(related_name='restaurateur', to='utilisateur.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('block', models.CharField(max_length=500, verbose_name=b'Block', blank=True)),
                ('facture', models.OneToOneField(to='restaurant.Facture')),
            ],
        ),
        migrations.AddField(
            model_name='commentaire',
            name='transaction',
            field=models.OneToOneField(to='restaurant.Transaction'),
        ),
    ]
