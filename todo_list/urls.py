from django.urls import path
from . import views

urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('profil/', views.profil, name='profil'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('publish_ride/', views.publish_ride, name='publish_ride')
]