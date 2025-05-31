from django.contrib import admin
from django.contrib import admin
from .models import Equipe, Tournoi
from .models import Match, Classement


# Register your models here.

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'joueurs', 'date_creation']
    list_filter = ['ville', 'joueurs']
    search_fields = ['nom', 'ville']
    ordering = ['nom']

@admin.register(Tournoi)
class TournoiAdmin(admin.ModelAdmin):
    list_display = ['nom', 'date_debut', 'lieu', 'nombre_equipes']
    list_filter = ['date_debut', 'lieu']
    search_fields = ['nom', 'lieu']
    filter_horizontal = ['equipes']
    ordering = ['-date_debut']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'tournoi', 'phase', 'score_format', 'statut', 'date_heure']
    list_filter = ['tournoi', 'phase', 'statut']
    search_fields = ['equipe_domicile__nom', 'equipe_exterieur__nom']
    ordering = ['tournoi', 'phase', 'numero_match']

@admin.register(Classement)
class ClassementAdmin(admin.ModelAdmin):
    list_display = ['equipe', 'tournoi', 'position', 'points', 'matchs_joues', 'difference_buts']
    list_filter = ['tournoi']
    ordering = ['tournoi', 'position']