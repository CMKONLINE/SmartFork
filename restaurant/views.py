from django.shortcuts import render,render_to_response,redirect
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponsePermanentRedirect,HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required,permission_required
from django.core.urlresolvers import reverse
from datetime import datetime,date,timedelta
from utilisateur.models import UserProfile
from restaurant.models import Facture,Transaction,Commentaire,FactureForm
from django.utils import timezone

# Create your views here.
def metamask(request):
	return render_to_response('restaurant/metamask.html',{},context_instance=RequestContext(request))

@login_required
def index(request):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	return render_to_response('restaurant/index.html',{'userPro':userPro},context_instance=RequestContext(request))

@login_required
def balance(request):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	compte=userPro.compte
	return render_to_response('restaurant/balance.html',{'compte':compte},context_instance=RequestContext(request))

@login_required
def comment(request,id_transaction):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	if Transaction.objects.filter(id=id_transaction).exists():
		transaction=Transaction.objects.filter(id=id_transaction)[0]
		facture=transaction.facture
		if (facture.client==userPro):
			if request.method=="POST":
				note=request.POST["note"]
				comment=request.POST["commentaire"]
				block=request.POST["block"]
				print(block)
				commentaire1=Commentaire(note=note,comment=comment,transaction=transaction,block=block)
				commentaire1.save()
				messages.add_message(request, messages.INFO, "Merci pour votre commentaire.")
				return HttpResponseRedirect('/restaurant/comment_list')
			else:
				if Commentaire.objects.filter(transaction=transaction).exists():
					messages.add_message(request, messages.ERROR, "Vous avez deja commente ce restaurant.")	
					return HttpResponseRedirect('/restaurant/')			
				else:
					return render_to_response('restaurant/comment.html',{'transaction':transaction},context_instance=RequestContext(request))
	messages.add_message(request, messages.ERROR, "Vous n etes pas autorise a faire cela.")
	return HttpResponseRedirect('/restaurant/')
	

@login_required
def comment_list(request):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	liste_factures=Facture.objects.filter(client=userPro)
	liste_transactions=[]
	for fact in liste_factures:
		if Transaction.objects.filter(facture=fact).exists():
			transac=Transaction.objects.filter(facture=fact)[0]
			liste_transactions.append(transac)
	liste_non_comment=[]
	liste_non_comment_old=[]
	liste_comment=[]
	for transac in liste_transactions:
		if Commentaire.objects.filter(transaction=transac).exists():
			liste_comment.append(transac)
		else:
			if timezone.now()-transac.date > timedelta(days=7):
				liste_non_comment_old.append(transac)
			else:
				print(transac)
				liste_non_comment.append(transac)
	return render_to_response('restaurant/comment_list.html',{'liste_comment':liste_comment,'liste_non_comment':liste_non_comment,'liste_non_comment_old':liste_non_comment_old},context_instance=RequestContext(request))

@login_required
def payment(request):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	if Facture.objects.filter(client=userPro).exists():
		last_bill=Facture.objects.filter(client=userPro).order_by('-date')[0]
		if Transaction.objects.filter(facture=last_bill).exists():
			messages.add_message(request, messages.ERROR, "Vous avez deja paye votre facture.")
			return HttpResponseRedirect('/restaurant/')
		else:
			return render_to_response('restaurant/payment.html',{'last_bill':last_bill},context_instance=RequestContext(request))
	else:
		messages.add_message(request, messages.ERROR, "Vous n avez pas de facture en cours.")
		return HttpResponseRedirect('/restaurant/')

@login_required
def payment_accepted(request):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	if Facture.objects.filter(client=userPro).exists():
		last_bill=Facture.objects.filter(client=userPro).order_by('-date')[0]
		if request.method == 'POST':
			block=request.POST["block"]
			transaction=Transaction(facture=last_bill,block=block)
			transaction.save()
		else:
			transaction=Transaction.objects.filter(facture=last_bill).order_by('-date')[0]
		return render_to_response('restaurant/payment_accepted.html',{'transaction':transaction},context_instance=RequestContext(request))	
	else:
		messages.add_message(request, messages.ERROR, "Vous n avez pas eu de facture.")
	return render_to_response('restaurant/payment_accepted.html',{},context_instance=RequestContext(request))

def restaurant_list(request):
	userPros=UserProfile.objects.filter(estRestaurant=True)
	return render_to_response('restaurant/restaurant_list.html',{'userPros':userPros},context_instance=RequestContext(request))

def review_list(request,id_restaurant):
	if Facture.objects.filter(restaurateur__id=id_restaurant).exists():
		factures=Facture.objects.filter(restaurateur__id=id_restaurant).order_by('-date')
		resto=UserProfile.objects.filter(id=id_restaurant)[0]
		commentaires=[]
		transactions=[]
		moyenne=0;somme=0;
		for fact in factures:
			if Transaction.objects.filter(facture=fact).exists():
				trans=Transaction.objects.filter(facture=fact)[0]
				if Commentaire.objects.filter(transaction=trans).exists():
					com=Commentaire.objects.filter(transaction=trans)[0]
					commentaires.append(com)
					transactions.append(trans)
					somme+=com.note;
		comTrans= zip(commentaires, transactions)
		moyenne= float (somme)/len(commentaires)
		return render_to_response('restaurant/review_list.html',{'comTrans':comTrans,'resto':resto,'moyenne':moyenne},context_instance=RequestContext(request))
	else:
		messages.add_message(request, messages.ERROR, "Ce restaurant n a pas de commentaire ou n existe pas.")
	return HttpResponseRedirect('/restaurant/')

@login_required
def new_bill(request):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	if userPro.estRestaurant:
		if request.method == 'POST':
			form=FactureForm(request.POST)
			form2=form.save(commit=False)
			form2.restaurateur=userPro
			form2.save()
			messages.add_message(request, messages.INFO, "Facture bien ajoutee.")
			return HttpResponseRedirect('/restaurant/')
		else:
			form=FactureForm()
			return render_to_response('restaurant/new_bill.html',{'form':form},context_instance=RequestContext(request))
	else:
		messages.add_message(request, messages.ERROR, "Vous ne pouvez pas ajouter de nouvelles factures.")
		return render_to_response('restaurant/new_bill.html',{},context_instance=RequestContext(request))

@login_required
def create_contract(request):
	userPro=UserProfile.objects.filter(user=request.user)[0]
	if request.method=="POST":
		contrat=request.POST["contrat"]
		if userPro.estRestaurant:
			userPro.compte_contrat=contrat
			userPro.save()
			messages.add_message(request, messages.INFO, "Un smart contrat vient d etre cree. Felicitations")
			return HttpResponseRedirect('/restaurant/')
	return render_to_response('restaurant/create_contract.html',{'userPro':userPro},context_instance=RequestContext(request))