from django.shortcuts import render

# Create your views here.
def accueil(request):
    return render(request, 'accueil.html')
def profil(request):
    return render(request, 'profil.html')
def sign_up(request):
    return render(request, 'sign_up.html')
def publish_ride(request):
    return render(request, 'publish_ride.html')
