from django.shortcuts import render, get_object_or_404,redirect

from django.contrib import messages
from .models import Equipe, Tournoi, Match
from django.utils import timezone



# Create your views here.

def accueil(request):
    """Page d'accueil avec statistiques"""
    equipes = Equipe.objects.all()
    tournois = Tournoi.objects.all()

    context = {
        'nombre_equipes': equipes.count(),
        'nombre_tournois': tournois.count(),
        'dernieres_equipes': equipes.order_by('-date_creation')[:3],
        'prochains_tournois': tournois.order_by('date_debut')[:3],
    }
    return render(request, 'index.html', context)


def liste_equipes(request):
    """Liste de toutes les équipes"""
    equipes = Equipe.objects.all()
    return render(request, 'liste_equipes.html', {'equipes': equipes})


def ajouter_equipe(request):
    """Formulaire d'ajout d'équipe"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        ville = request.POST.get('ville')
        joueurs = request.POST.get('joueurs', 11)

        if nom and ville:
            Equipe.objects.create(
                nom=nom,
                ville=ville,
                joueurs=int(joueurs)
            )
            messages.success(request, f'Équipe "{nom}" ajoutée avec succès ! 🎉')
            return redirect('liste_equipes')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'ajouter_equipe.html')



def detail_equipe(request, equipe_id):
    """Afficher le détail d'une équipe"""
    equipe = get_object_or_404(Equipe, id=equipe_id)
    tournois_equipe = equipe.tournoi_set.all().order_by('-date_debut')

    # Calculs pour les statistiques
    tournois_count = tournois_equipe.count()
    tournois_actifs = tournois_equipe.filter(date_debut__gte=timezone.now().date()).count()
    jours_existence = (timezone.now().date() - equipe.date_creation.date()).days

    context = {
        'equipe': equipe,
        'tournois_equipe': tournois_equipe,
        'tournois_count': tournois_count,
        'tournois_actifs': tournois_actifs,
        'jours_existence': jours_existence,
    }
    return render(request, 'detail_equipe.html', context)


def modifier_equipe(request, equipe_id):
    """Modifier une équipe existante"""
    equipe = get_object_or_404(Equipe, id=equipe_id)

    if request.method == 'POST':
        # Sauvegarder l'ancien nom pour le message
        ancien_nom = equipe.nom

        # Mettre à jour les champs
        equipe.nom = request.POST.get('nom', equipe.nom)
        equipe.ville = request.POST.get('ville', equipe.ville)
        joueurs = request.POST.get('joueurs', equipe.joueurs)

        # Validation du nombre de joueurs
        try:
            joueurs = int(joueurs)
            if joueurs < 11:
                messages.error(request, '❌ Une équipe doit avoir au moins 11 joueurs.')
                return render(request, 'modifier_equipe.html', {'equipe': equipe})
            elif joueurs > 25:
                messages.error(request, '❌ Une équipe ne peut pas avoir plus de 25 joueurs.')
                return render(request, 'modifier_equipe.html', {'equipe': equipe})
            equipe.joueurs = joueurs
        except ValueError:
            messages.error(request, '❌ Le nombre de joueurs doit être un nombre valide.')
            return render(request, 'modifier_equipe.html', {'equipe': equipe})

        # Sauvegarder
        equipe.save()

        # Message de succès personnalisé
        if ancien_nom != equipe.nom:
            messages.success(request, f'✅ Équipe renommée de "{ancien_nom}" à "{equipe.nom}" avec succès !')
        else:
            messages.success(request, f'✅ Équipe "{equipe.nom}" modifiée avec succès !')

        return redirect('detail_equipe', equipe_id=equipe.id)

    return render(request, 'modifier_equipe.html', {'equipe': equipe})


def supprimer_equipe(request, equipe_id):
    """Supprimer une équipe avec confirmation"""
    equipe = get_object_or_404(Equipe, id=equipe_id)
    tournois_count = equipe.tournoi_set.count()

    if request.method == 'POST':
        nom_equipe = equipe.nom
        equipe.delete()
        messages.success(request, f'🗑️ Équipe "{nom_equipe}" supprimée avec succès.')
        return redirect('liste_equipes')

    context = {
        'equipe': equipe,
        'tournois_count': tournois_count,
    }
    return render(request, 'confirmer_suppression_equipe.html', context)

def liste_tournois(request):
    """Liste de tous les tournois"""
    tournois = Tournoi.objects.all()
    return render(request, 'liste_tournois.html', {'tournois': tournois})


def ajouter_tournoi(request):
    """Formulaire d'ajout de tournoi"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        date_debut = request.POST.get('date_debut')
        lieu = request.POST.get('lieu')

        if nom and date_debut and lieu:
            Tournoi.objects.create(
                nom=nom,
                date_debut=date_debut,
                lieu=lieu
            )
            messages.success(request, f'Tournoi "{nom}" créé avec succès ! 🏆')
            return redirect('liste_tournois')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'ajouter_tournoi.html')


def liste_tournois(request):
    """Liste de tous les tournois"""
    tournois = Tournoi.objects.all().order_by('-date_debut')
    return render(request, 'liste_tournois.html', {'tournois': tournois})


def ajouter_tournoi(request):
    """Formulaire d'ajout de tournoi"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        date_debut = request.POST.get('date_debut')
        lieu = request.POST.get('lieu')

        if nom and date_debut and lieu:
            Tournoi.objects.create(
                nom=nom,
                date_debut=date_debut,
                lieu=lieu
            )
            messages.success(request, f'Tournoi "{nom}" créé avec succès ! 🏆')
            return redirect('liste_tournois')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'ajouter_tournoi.html')


def detail_tournoi(request, tournoi_id):
    """Afficher le détail d'un tournoi avec gestion des équipes"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)
    equipes_participantes = tournoi.equipes.all()
    toutes_equipes = Equipe.objects.exclude(id__in=equipes_participantes.values_list('id', flat=True))

    # Calculs pour les statistiques
    total_joueurs = sum(equipe.joueurs for equipe in equipes_participantes)
    nb_equipes = equipes_participantes.count()
    matchs_possibles = (nb_equipes * (nb_equipes - 1)) // 2 if nb_equipes > 1 else 0

    context = {
        'tournoi': tournoi,
        'equipes_participantes': equipes_participantes,
        'toutes_equipes': toutes_equipes,
        'total_joueurs': total_joueurs,
        'matchs_possibles': matchs_possibles,
    }
    return render(request, 'detail_tournoi.html', context)


def ajouter_equipe_tournoi(request, tournoi_id):
    """Ajouter une équipe à un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    if request.method == 'POST':
        equipe_id = request.POST.get('equipe_id')
        if equipe_id:
            equipe = get_object_or_404(Equipe, id=equipe_id)

            # Vérifier que l'équipe n'est pas déjà dans le tournoi
            if equipe not in tournoi.equipes.all():
                tournoi.equipes.add(equipe)
                messages.success(request, f'🎉 Équipe "{equipe.nom}" ajoutée au tournoi "{tournoi.nom}" !')
            else:
                messages.warning(request, f'⚠️ L\'équipe "{equipe.nom}" participe déjà à ce tournoi.')
        else:
            messages.error(request, '❌ Veuillez sélectionner une équipe.')

    return redirect('detail_tournoi', tournoi_id=tournoi_id)


def retirer_equipe_tournoi(request, tournoi_id, equipe_id):
    """Retirer une équipe d'un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)
    equipe = get_object_or_404(Equipe, id=equipe_id)

    if equipe in tournoi.equipes.all():
        tournoi.equipes.remove(equipe)
        messages.success(request, f'✅ Équipe "{equipe.nom}" retirée du tournoi "{tournoi.nom}".')
    else:
        messages.error(request, f'❌ Cette équipe ne participe pas à ce tournoi.')

    return redirect('detail_tournoi', tournoi_id=tournoi_id)


def modifier_tournoi(request, tournoi_id):
    """Modifier un tournoi existant"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    if request.method == 'POST':
        tournoi.nom = request.POST.get('nom', tournoi.nom)
        tournoi.date_debut = request.POST.get('date_debut', tournoi.date_debut)
        tournoi.lieu = request.POST.get('lieu', tournoi.lieu)
        tournoi.save()

        messages.success(request, f'🏆 Tournoi "{tournoi.nom}" modifié avec succès !')
        return redirect('detail_tournoi', tournoi_id=tournoi.id)

    return render(request, 'modifier_tournoi.html', {'tournoi': tournoi})


def supprimer_tournoi(request, tournoi_id):
    """Supprimer un tournoi avec confirmation"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    if request.method == 'POST':
        nom_tournoi = tournoi.nom
        tournoi.delete()
        messages.success(request, f'🗑️ Tournoi "{nom_tournoi}" supprimé avec succès.')
        return redirect('liste_tournois')

    return render(request, 'confirmer_suppression_tournoi.html', {'tournoi': tournoi})


def matchs_tournoi(request, tournoi_id):
    """Afficher tous les matchs d'un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)
    matchs = tournoi.matchs.all().order_by('numero_match')

    # Statistiques
    matchs_termines = matchs.filter(statut='TERMINE').count()
    matchs_a_venir = matchs.filter(statut='A_VENIR').count()

    context = {
        'tournoi': tournoi,
        'matchs': matchs,
        'matchs_termines': matchs_termines,
        'matchs_a_venir': matchs_a_venir,
    }
    return render(request, 'matchs_tournoi.html', context)



def saisir_resultat(request, match_id):
    """Saisir le résultat d'un match"""
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        try:
            score_domicile = int(request.POST.get('score_domicile', 0))
            score_exterieur = int(request.POST.get('score_exterieur', 0))

            if score_domicile < 0 or score_exterieur < 0:
                raise ValueError("Les scores ne peuvent pas être négatifs")

            match.score_domicile = score_domicile
            match.score_exterieur = score_exterieur
            match.statut = 'TERMINE'
            match.notes = request.POST.get('notes', '')
            match.save()

            # Recalculer le classement
            match.tournoi.calculer_classement()

            messages.success(request,
                             f'✅ Résultat enregistré: {match.equipe_domicile.nom} {score_domicile}-{score_exterieur} {match.equipe_exterieur.nom}')
            return redirect('matchs_tournoi', tournoi_id=match.tournoi.id)

        except ValueError as e:
            messages.error(request, f'❌ Erreur dans les scores: {str(e)}')

    return render(request, 'saisir_resultat.html', {'match': match})


def classement_tournoi(request, tournoi_id):
    """Afficher le classement d'un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    # Recalculer le classement pour être sûr
    classements = tournoi.calculer_classement()

    context = {
        'tournoi': tournoi,
        'classements': classements,
    }
    return render(request, 'classement_tournoi.html', context)


def detail_match(request, match_id):
    """Détail d'un match spécifique"""
    match = get_object_or_404(Match, id=match_id)

    context = {
        'match': match,
        'tournoi': match.tournoi,
    }
    return render(request, 'detail_match.html', context)


# ===== VUES POUR LES MATCHS =====

def generer_matchs(request, tournoi_id):
    """Générer les matchs d'un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    if request.method == 'POST':
        format_choisi = request.POST.get('format', 'championnat')

        if format_choisi == 'championnat':
            success, message = tournoi.generer_matchs_championnat()
        else:
            success, message = False, "Format non supporté pour le moment"

        if success:
            messages.success(request, f'🎉 {message}')
            return redirect('matchs_tournoi', tournoi_id=tournoi.id)  # ← REDIRECTION VERS LES MATCHS
        else:
            messages.error(request, f'❌ {message}')

    return render(request, 'generer_matchs.html', {'tournoi': tournoi})
def tirage_sort(request, tournoi_id):
    """Effectuer un nouveau tirage au sort"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    if request.method == 'POST':
        # Supprimer les anciens matchs
        tournoi.matchs.all().delete()

        # Régénérer avec nouveau tirage
        if tournoi.nombre_equipes() in [4, 8, 16, 32]:
            success, message = tournoi.generer_matchs_elimination()
        else:
            success, message = tournoi.generer_matchs_championnat()

        if success:
            messages.success(request, f'🎲 Nouveau tirage effectué ! {message}')
        else:
            messages.error(request, f'❌ {message}')

        return redirect('matchs_tournoi', tournoi_id=tournoi.id)

    # Page de confirmation simple
    context = {'tournoi': tournoi}
    return render(request, 'confirmer_tirage.html', context)


def classement_tournoi(request, tournoi_id):
    """Afficher le classement d'un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    # Recalculer le classement pour être sûr
    classements = tournoi.calculer_classement()

    # Statistiques du tournoi
    matchs = tournoi.matchs.all()
    matchs_termines = matchs.filter(statut='TERMINE').count()
    matchs_restants = matchs.count() - matchs_termines

    # Calcul du total de buts
    total_buts = 0
    for match in matchs.filter(statut='TERMINE'):
        if match.score_domicile is not None and match.score_exterieur is not None:
            total_buts += match.score_domicile + match.score_exterieur

    context = {
        'tournoi': tournoi,
        'classements': classements,
        'matchs_termines': matchs_termines,
        'matchs_restants': matchs_restants,
        'total_buts': total_buts,
    }
    return render(request, 'classement_tournoi.html', context)


def detail_match(request, match_id):
    """Détail d'un match spécifique"""
    match = get_object_or_404(Match, id=match_id)

    context = {
        'match': match,
        'tournoi': match.tournoi,
    }
    return render(request, 'detail_match.html', context)


def saisir_resultat(request, match_id):
    """Saisir le résultat d'un match"""
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        try:
            score_domicile = int(request.POST.get('score_domicile', 0))
            score_exterieur = int(request.POST.get('score_exterieur', 0))

            match.score_domicile = score_domicile
            match.score_exterieur = score_exterieur
            match.statut = 'TERMINE'
            match.save()

            # Recalculer le classement
            match.tournoi.calculer_classement()

            messages.success(request,
                             f'✅ Résultat enregistré: {match.equipe_domicile.nom} {score_domicile}-{score_exterieur} {match.equipe_exterieur.nom}')
            return redirect('matchs_tournoi', tournoi_id=match.tournoi.id)

        except ValueError:
            messages.error(request, '❌ Erreur dans les scores')

    return render(request, 'saisir_resultat.html', {'match': match})


def generer_matchs(request, tournoi_id):
    """Générer les matchs d'un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)

    if request.method == 'POST':
        format_choisi = request.POST.get('format', 'championnat')

        if format_choisi == 'championnat':
            success, message = tournoi.generer_matchs_championnat()
        else:
            success, message = False, "Format non supporté pour le moment"

        if success:
            messages.success(request, f'🎉 {message}')
            return redirect('detail_tournoi', tournoi_id=tournoi.id)  # Retour au détail
        else:
            messages.error(request, f'❌ {message}')

    return render(request, 'generer_matchs.html', {'tournoi': tournoi})


def tirage_sort(request, tournoi_id):
    """Effectuer un nouveau tirage au sort"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)
    messages.info(request, '🎲 Fonction de tirage au sort en cours de développement...')
    return redirect('detail_tournoi', tournoi_id=tournoi.id)


def matchs_tournoi(request, tournoi_id):
    """Afficher tous les matchs d'un tournoi"""
    tournoi = get_object_or_404(Tournoi, id=tournoi_id)
    matchs = tournoi.matchs.all() if hasattr(tournoi, 'matchs') else []

    context = {
        'tournoi': tournoi,
        'matchs': matchs,
    }
    return render(request, 'matchs_tournoi.html', context)
