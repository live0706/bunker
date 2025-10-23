Application de Tableau de Bord Bancaire (Python/Tkinter)
Ceci est une application de bureau simple simulant un tableau de bord bancaire. Elle a été développée en Python en utilisant la bibliothèque tkinter pour l'interface graphique (GUI) et matplotlib pour la visualisation des données.

L'application présente une interface en thème sombre ("Dark Mode") et permet des opérations bancaires de base.

Fonctionnalités
Système de Connexion : Une fenêtre de connexion simple vérifiant un nom d'utilisateur et un ID de compte.

Tableau de Bord : Affiche le solde du compte en temps réel après une connexion réussie.

Opérations Bancaires : Permet à l'utilisateur d'effectuer des dépôts et des retraits.

Mise à jour instantanée : Le solde affiché est mis à jour immédiatement après chaque opération.

Visualisation Graphique : Génère un graphique (dans une nouvelle fenêtre) montrant l'évolution du solde au cours de la session actuelle, en utilisant matplotlib.

Prérequis
Pour exécuter cette application, vous aurez besoin de :

Python 3.11 ou plus

tkinter (généralement inclus dans l'installation standard de Python)

matplotlib (une bibliothèque tierce pour les graphiques)

Installation
Assurez-vous que Python 3 est installé sur votre machine.

Clonez ce dépôt ou téléchargez les fichiers du projet.

Installez la bibliothèque matplotlib si elle n'est pas déjà présente, en utilisant pip :

Bash

pip install matplotlib
Structure du Projet
Pour que l'application fonctionne, les deux fichiers principaux doivent être dans le même répertoire :

/votre-projet
|
|-- main_app.py        (Le script principal de l'application Tkinter que vous m'avez donné)
|-- Account_class.py   (Le fichier contenant la définition de la classe 'account')
|-- README.md          (Ce fichier)
(Assurez-vous que votre fichier Account_class.py est bien présent et contient la classe account utilisée par le script principal.)

Lancement de l'application
Pour démarrer l'application, exécutez le script principal depuis votre terminal :

Bash

python main_app.py
(Remplacez main_app.py par le nom réel de votre fichier si vous l'avez renommé.)

Données de Test
L'application est pré-configurée avec deux comptes de démonstration (codés en dur). Utilisez les identifiants suivants sur l'écran de connexion pour tester :

Compte 1 :

Nom : Ross

ID du compte : 9502018482

Compte 2 :

Nom : Rachel

ID du compte : 1945729572
