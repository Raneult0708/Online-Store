from django.shortcuts import render,redirect
from .models import Utilisateur

# Create your views here.
def accueil(request):
    return render(request, 'accueil.html')
def profil(request):
    return render(request, 'profil.html')
def sign_up(request):
    if request.method == 'POST' :
        utilisateur = Utilisateur()
        utilisateur.nom = request.POST.get('nom')
        utilisateur.save()
        return render(request, 'profil.html')

    return render(request, 'sign_up.html')
def publish_ride(request):
    return render(request, 'publish_ride.html')






def junio(request):
    return render(request, "sign.html")