# FinTrack

Application de bureau pour suivre ses finances personnelles : enregistrer ses revenus et ses dépenses, consulter l'historique dans un tableau et suivre son solde en temps réel. Les données sont sauvegardées automatiquement dans un fichier JSON.

Projet réalisé en **Python** avec **Tkinter**, dans le but de mettre en pratique les notions d'une formation Python complète : variables, conditions, listes, boucles, fonctions, programmation orientée objet, fichiers, exceptions, environnements virtuels et décorateurs.

## Fonctionnalités

- Ajout d'une transaction (description, montant, type Dépense ou Revenu)
- Tableau de l'historique avec date, description, type et montant
- Calcul automatique du solde (vert si positif, rouge si négatif)
- Sauvegarde automatique dans `sauvegarde.json` et rechargement au démarrage
- Validation de la saisie : montant numérique, strictement positif, plafonné à 10 000 000 FCFA, description non vide
- Messages d'erreur clairs directement dans l'interface, sans plantage
- Bouton **Initialiser** (avec confirmation) pour remettre les transactions et le solde à zéro
- Journal d'exécution et chronométrage des actions grâce à des décorateurs

## Structure du projet


ProjetDev/
├── fintrack/
│   ├── main.py            # Interface Tkinter et logique principale
│   ├── Transaction.py     # Classe de base (description, montant, date)
│   ├── Depense.py         # Sous-classe : effet négatif sur le solde
│   ├── Revenu.py          # Sous-classe : effet positif sur le solde
│   └── decorateur.py      # Décorateurs @log_action et @chronometre
├── sauvegarde.json        # Données enregistrées (créé automatiquement)
├── requirements.txt
└── README.md


## Prérequis

- Python 3.10 ou plus récent
- Tkinter (inclus avec l'installation standard de Python sous Windows)

Aucune bibliothèque externe n'est nécessaire.

## Installation

1. Récupérer le projet :
   git clone <url-du-depot>

2. Créer et activer un environnement virtuel :
   python -m venv env
   venv\Scripts\activate

3. Installer les dépendances :
   pip install -r requirements.txt

## Lancement

Le plus simple est de lancer `fintrack/main.py` depuis PyCharm (clic droit sur le fichier, puis *Run*).

En ligne de commande, depuis la racine du projet :
python fintrack/main.py

## Utilisation

1. Saisir une **description** et un **montant** en FCFA.
2. Choisir le **type** : Dépense ou Revenu.
3. Cliquer sur **Ajouter** : la transaction apparaît dans le tableau et le solde est mis à jour.
4. Fermer et rouvrir l'application : les transactions sont retrouvées automatiquement.
5. Cliquer sur **Initialiser** pour tout effacer (une confirmation est demandée).

## Notions Python mises en pratique

| Notion | Où dans le projet |
|--------|-------------------|
| Variables et constantes | `Devise`, `Montant_Max` |
| Conditions | Validation du montant et du type |
| Listes et boucles | Liste des transactions, calcul du solde, remplissage du tableau |
| Fonctions | `ajouter()`, `calcule_solde()`, `sauv()`, `charger()`, `initialiser()` |
| Objets et héritage | `Transaction` → `Depense` et `Revenu` (polymorphisme via `effet_sur_solde()`) |
| Interface graphique | Tkinter : `Entry`, `Radiobutton`, `Button`, `ttk.Treeview`, `Scrollbar` |
| Fichiers et dictionnaires | Sauvegarde et chargement JSON avec `to_dict()` |
| Exceptions | `try/except`, exception personnalisée `DescriptionVideError` |
| Environnement virtuel | `env` et `requirements.txt` |
| Décorateurs | `@log_action` et `@chronometre` (avec `functools.wraps`) |
