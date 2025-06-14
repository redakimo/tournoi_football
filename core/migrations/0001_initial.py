# Generated by Django 5.2.1 on 2025-05-23 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name="Nom de l'équipe")),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('joueurs', models.IntegerField(default=11, verbose_name='Nombre de joueurs')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
            ],
            options={
                'verbose_name': 'Équipe',
                'verbose_name_plural': 'Équipes',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Tournoi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, verbose_name='Nom du tournoi')),
                ('date_debut', models.DateField(verbose_name='Date de début')),
                ('lieu', models.CharField(max_length=100, verbose_name='Lieu')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('equipes', models.ManyToManyField(blank=True, to='core.equipe', verbose_name='Équipes participantes')),
            ],
            options={
                'verbose_name': 'Tournoi',
                'verbose_name_plural': 'Tournois',
                'ordering': ['-date_debut'],
            },
        ),
    ]
