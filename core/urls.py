from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.accueil, name='accueil'),

    # Équipes
    path('equipes/', views.liste_equipes, name='liste_equipes'),
    path('equipes/ajouter/', views.ajouter_equipe, name='ajouter_equipe'),
    path('equipes/<int:equipe_id>/', views.detail_equipe, name='detail_equipe'),
    path('equipes/<int:equipe_id>/modifier/', views.modifier_equipe, name='modifier_equipe'),
    path('equipes/<int:equipe_id>/supprimer/', views.supprimer_equipe, name='supprimer_equipe'),

    # Tournois
    path('tournois/', views.liste_tournois, name='liste_tournois'),
    path('tournois/ajouter/', views.ajouter_tournoi, name='ajouter_tournoi'),
    path('tournois/<int:tournoi_id>/', views.detail_tournoi, name='detail_tournoi'),
    path('tournois/<int:tournoi_id>/modifier/', views.modifier_tournoi, name='modifier_tournoi'),
    path('tournois/<int:tournoi_id>/supprimer/', views.supprimer_tournoi, name='supprimer_tournoi'),

    # Gestion équipes dans tournois
    path('tournois/<int:tournoi_id>/ajouter-equipe/', views.ajouter_equipe_tournoi, name='ajouter_equipe_tournoi'),
    path('tournois/<int:tournoi_id>/retirer-equipe/<int:equipe_id>/', views.retirer_equipe_tournoi,
         name='retirer_equipe_tournoi'),

    # ✅ NOUVELLES ROUTES POUR LES MATCHS - À AJOUTER
    path('tournois/<int:tournoi_id>/generer-matchs/', views.generer_matchs, name='generer_matchs'),
    path('tournois/<int:tournoi_id>/tirage-sort/', views.tirage_sort, name='tirage_sort'),
    path('tournois/<int:tournoi_id>/matchs/', views.matchs_tournoi, name='matchs_tournoi'),
    path('tournois/<int:tournoi_id>/classement/', views.classement_tournoi, name='classement_tournoi'),
    path('matchs/<int:match_id>/', views.detail_match, name='detail_match'),
    path('matchs/<int:match_id>/resultat/', views.saisir_resultat, name='saisir_resultat'),

# AJOUTER CES LIGNES dans core/urls.py
path('tournois/<int:tournoi_id>/generer-matchs/', views.generer_matchs, name='generer_matchs'),
path('tournois/<int:tournoi_id>/tirage-sort/', views.tirage_sort, name='tirage_sort'),
path('tournois/<int:tournoi_id>/matchs/', views.matchs_tournoi, name='matchs_tournoi'),

]