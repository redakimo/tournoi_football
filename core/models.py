from django.db import models

# Create your models here.
from django.db import models


class Equipe(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de l'équipe")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    joueurs = models.IntegerField(default=11, verbose_name="Nombre de joueurs")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    def __str__(self):
        return f"{self.nom} ({self.ville})"

    class Meta:
        verbose_name = "Équipe"
        verbose_name_plural = "Équipes"
        ordering = ['nom']


class Tournoi(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom du tournoi")
    date_debut = models.DateField(verbose_name="Date de début")
    lieu = models.CharField(max_length=100, verbose_name="Lieu")
    equipes = models.ManyToManyField(Equipe, blank=True, verbose_name="Équipes participantes")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    def nombre_equipes(self):
        return self.equipes.count()

    def peut_commencer(self):
        """Vérifier si le tournoi a assez d'équipes pour commencer"""
        return self.equipes.count() >= 4

    def total_joueurs(self):
        """Calculer le nombre total de joueurs dans le tournoi"""
        return sum(equipe.joueurs for equipe in self.equipes.all())

    # À ajouter dans la classe Tournoi dans core/models.py

    def generer_matchs_elimination(self):
        """Générer les matchs en élimination directe"""
        equipes = list(self.equipes.all())
        nb_equipes = len(equipes)

        # Vérifier que c'est une puissance de 2
        if nb_equipes not in [4, 8, 16, 32]:
            return False, f"Élimination directe nécessite 4, 8, 16 ou 32 équipes. Vous avez {nb_equipes} équipes."

        # Mélanger les équipes (tirage au sort)
        import random
        random.shuffle(equipes)

        # Supprimer les anciens matchs
        self.matchs.all().delete()

        # Générer les matchs du premier tour
        matchs = []
        for i in range(0, nb_equipes, 2):
            match = Match.objects.create(
                tournoi=self,
                equipe_domicile=equipes[i],
                equipe_exterieur=equipes[i + 1],
                phase='DEMI' if nb_equipes == 4 else 'QUART' if nb_equipes == 8 else 'HUITIEME',
                numero_match=(i // 2) + 1,
                terrain=f"Terrain {(i // 2) + 1}"
            )
            matchs.append(match)

        return True, f"{len(matchs)} matchs générés pour le premier tour !"

    # À ajouter dans la classe Tournoi dans core/models.py

    def generer_matchs_championnat(self):
        """Générer tous les matchs en championnat (tous contre tous)"""
        equipes = list(self.equipes.all())
        nb_equipes = len(equipes)

        if nb_equipes < 3:
            return False, "Il faut au moins 3 équipes pour un championnat."

        # Supprimer les anciens matchs
        self.matchs.all().delete()

        # Générer tous les matchs possibles
        matchs = []
        numero = 1
        for i in range(nb_equipes):
            for j in range(i + 1, nb_equipes):
                match = Match.objects.create(
                    tournoi=self,
                    equipe_domicile=equipes[i],
                    equipe_exterieur=equipes[j],
                    phase='POULES',
                    numero_match=numero,
                    terrain=f"Terrain {numero}"
                )
                matchs.append(match)
                numero += 1

        return True, f"{len(matchs)} matchs générés pour le championnat !"

    def calculer_classement(self):
        """Calculer le classement du tournoi"""
        # Supprimer l'ancien classement
        self.classements.all().delete()

        # Créer le classement pour chaque équipe
        classements_data = []

        for equipe in self.equipes.all():
            classement = Classement.objects.create(
                tournoi=self,
                equipe=equipe
            )

            # Calculer les statistiques
            matchs_domicile = self.matchs.filter(equipe_domicile=equipe, statut='TERMINE')
            matchs_exterieur = self.matchs.filter(equipe_exterieur=equipe, statut='TERMINE')

            for match in matchs_domicile:
                classement.matchs_joues += 1
                classement.buts_pour += match.score_domicile or 0
                classement.buts_contre += match.score_exterieur or 0

                if match.score_domicile is not None and match.score_exterieur is not None:
                    if match.score_domicile > match.score_exterieur:
                        classement.victoires += 1
                        classement.points += 3
                    elif match.score_domicile == match.score_exterieur:
                        classement.nuls += 1
                        classement.points += 1
                    else:
                        classement.defaites += 1

            for match in matchs_exterieur:
                classement.matchs_joues += 1
                classement.buts_pour += match.score_exterieur or 0
                classement.buts_contre += match.score_domicile or 0

                if match.score_domicile is not None and match.score_exterieur is not None:
                    if match.score_exterieur > match.score_domicile:
                        classement.victoires += 1
                        classement.points += 3
                    elif match.score_exterieur == match.score_domicile:
                        classement.nuls += 1
                        classement.points += 1
                    else:
                        classement.defaites += 1

            classement.save()
            classements_data.append(classement)

        # Trier par points, puis différence de buts
        classements_data.sort(key=lambda x: (x.points, x.buts_pour - x.buts_contre, x.buts_pour), reverse=True)

        # Attribuer les positions
        for i, classement in enumerate(classements_data, 1):
            classement.position = i
            classement.save()

        return classements_data
    class Meta:
        verbose_name = "Tournoi"
        verbose_name_plural = "Tournois"
        ordering = ['-date_debut']



class Match(models.Model):
    PHASES = [
        ('POULES', 'Phase de poules'),
        ('HUITIEME', 'Huitième de finale'),
        ('QUART', 'Quart de finale'),
        ('DEMI', 'Demi-finale'),
        ('FINALE', 'Finale'),
        ('PETITE_FINALE', 'Petite finale'),
    ]

    STATUTS = [
        ('A_VENIR', 'À venir'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('REPORTE', 'Reporté'),
    ]

    tournoi = models.ForeignKey(Tournoi, on_delete=models.CASCADE, related_name='matchs')
    equipe_domicile = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='matchs_domicile')
    equipe_exterieur = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='matchs_exterieur')

    # Informations du match
    phase = models.CharField(max_length=20, choices=PHASES, default='POULES')
    numero_match = models.IntegerField(default=1)
    date_heure = models.DateTimeField(null=True, blank=True)
    terrain = models.CharField(max_length=100, blank=True, default="Terrain principal")

    # Résultats
    score_domicile = models.IntegerField(null=True, blank=True)
    score_exterieur = models.IntegerField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='A_VENIR')

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.equipe_domicile.nom} vs {self.equipe_exterieur.nom}"

    def est_termine(self):
        return self.statut == 'TERMINE' and self.score_domicile is not None and self.score_exterieur is not None

    def equipe_gagnante(self):
        if not self.est_termine():
            return None
        if self.score_domicile > self.score_exterieur:
            return self.equipe_domicile
        elif self.score_exterieur > self.score_domicile:
            return self.equipe_exterieur
        return None  # Match nul

    def score_format(self):
        if self.est_termine():
            return f"{self.score_domicile} - {self.score_exterieur}"
        return "- - -"

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matchs"
        ordering = ['date_heure', 'numero_match']


class Classement(models.Model):
    """Classement des équipes dans un tournoi"""
    tournoi = models.ForeignKey(Tournoi, on_delete=models.CASCADE, related_name='classements')
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)

    # Statistiques
    matchs_joues = models.IntegerField(default=0)
    victoires = models.IntegerField(default=0)
    nuls = models.IntegerField(default=0)
    defaites = models.IntegerField(default=0)
    buts_pour = models.IntegerField(default=0)
    buts_contre = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    # Position
    position = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.equipe.nom} - {self.points} pts"

    @property
    def difference_buts(self):
        return self.buts_pour - self.buts_contre

    def pourcentage_victoires(self):
        if self.matchs_joues == 0:
            return 0
        return round((self.victoires / self.matchs_joues) * 100, 1)

    class Meta:
        verbose_name = "Classement"
        verbose_name_plural = "Classements"
        ordering = ['-points', '-buts_pour', 'buts_contre']  # CORRIGÉ
        unique_together = ['tournoi', 'equipe']