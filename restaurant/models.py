# -*- coding: utf-8 -*-
from django.db import models
from utilisateur.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.forms import ModelForm

class Facture(models.Model):
	liste=models.TextField('Liste Facture',max_length=500)
	montant=models.FloatField('Montant Facture en ETH',default=0)
	restaurateur=models.ForeignKey(UserProfile,related_name='restaurateur')
	client=models.ForeignKey(UserProfile,related_name='client')
	date=models.DateTimeField(auto_now=True)

class FactureForm(forms.ModelForm):
	class Meta:
		model=Facture
		fields=('liste','montant','client')

class Transaction(models.Model):
	facture=models.OneToOneField(Facture)
	date=models.DateTimeField(auto_now=True)
	block=models.CharField('Block',blank=True,max_length=500)

class Commentaire(models.Model):
	transaction=models.OneToOneField(Transaction)
	comment=models.TextField('Commentaire',max_length=500)
	note=models.IntegerField(default=5)
	date=models.DateTimeField(auto_now=True)
	block=models.CharField('Block',blank=True,max_length=500)
