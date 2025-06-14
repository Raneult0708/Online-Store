# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Conversation(models.Model):
    date_creation = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey('Utilisateur', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Conversation'


class Demandecovoiturage(models.Model):
    passager = models.ForeignKey('Utilisateur', models.DO_NOTHING)
    point_depart = models.CharField(max_length=255)
    point_arrivee = models.CharField(max_length=255)
    heure_depart_souhaitee = models.DateTimeField()
    date_publication = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DemandeCovoiturage'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, models.DO_NOTHING)
    expediteur = models.ForeignKey('Utilisateur', models.DO_NOTHING)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Message'


class Offrecovoiturage(models.Model):
    conducteur = models.ForeignKey('Utilisateur', models.DO_NOTHING)
    point_depart = models.CharField(max_length=255)
    point_arrivee = models.CharField(max_length=255)
    heure_depart = models.DateTimeField()
    places_disponibles = models.IntegerField()
    date_publication = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OffreCovoiturage'


class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_telephone = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=255)
    mot_de_passe = models.CharField(max_length=255)
    est_conducteur = models.IntegerField(blank=True, null=True)
    photo_profil = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Utilisateur'


class Vehicule(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, models.DO_NOTHING)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    places_disponibles = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Vehicule'


class Bookings(models.Model):
    ride = models.ForeignKey('Rides', models.DO_NOTHING)
    passager = models.ForeignKey(Utilisateur, models.DO_NOTHING)
    nb_places_reservees = models.IntegerField(blank=True, null=True)
    statut = models.CharField(max_length=9, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookings'


class MatchingHistory(models.Model):
    ride = models.ForeignKey('Rides', models.DO_NOTHING)
    request = models.ForeignKey(Demandecovoiturage, models.DO_NOTHING)
    score_compatibilite = models.DecimalField(max_digits=5, decimal_places=2)
    distance_km = models.DecimalField(max_digits=8, decimal_places=2)
    difference_horaire_minutes = models.IntegerField()
    statut = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matching_history'


class Rides(models.Model):
    conducteur = models.ForeignKey(Utilisateur, models.DO_NOTHING)
    vehicule = models.ForeignKey(Vehicule, models.DO_NOTHING, blank=True, null=True)
    point_depart = models.CharField(max_length=500)
    point_arrivee = models.CharField(max_length=500)
    latitude_depart = models.DecimalField(max_digits=10, decimal_places=8)
    longitude_depart = models.DecimalField(max_digits=11, decimal_places=8)
    latitude_arrivee = models.DecimalField(max_digits=10, decimal_places=8)
    longitude_arrivee = models.DecimalField(max_digits=11, decimal_places=8)
    heure_depart = models.DateTimeField()
    heure_arrivee_prevue = models.DateTimeField(blank=True, null=True)
    nb_places_disponibles = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=11, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rides'
