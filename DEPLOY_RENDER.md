# Déploiement d’Epidemia sur Render

Le dépôt contient un Blueprint Render (`render.yaml`) configuré pour lancer
l’application sur un service web avec un disque persistant. Le disque est
nécessaire pour conserver les comptes, sessions et modifications de la base
SQLite après les redémarrages et les déploiements.

## Mise en ligne

1. Créez un dépôt **privé** sur GitHub et poussez-y les fichiers du projet,
   notamment `epidemiaTH.py`, le dossier `epidemia_app/` et `epidemia.db`.
   La base actuelle sert de données de démonstration et sera utilisée uniquement
   pour initialiser le disque lors du premier démarrage.
2. Dans Render, choisissez **New > Blueprint**, connectez le dépôt privé et
   confirmez la création du service décrit dans `render.yaml`.
3. Attendez que le déploiement passe à l’état **Live**, puis ouvrez l’URL fournie
   par Render.

Au premier démarrage, `start_render.py` copie la base du dépôt vers
`/var/data/epidemia.db`. Les redéploiements suivants gardent la base du disque et
ne remplacent pas les changements enregistrés. Ne supprimez pas le disque Render.

## Avant un usage réel

- Le disque persistant nécessite un service Render payant. L’instance configurée
  est unique ; ne la mettez pas à l’échelle horizontalement avec SQLite.
- Changez le mot de passe du compte administrateur et n’utilisez pas les données
  de démonstration pour des données de santé réelles.
- Exportez régulièrement une sauvegarde de la base depuis le disque Render.
- Toute personne ayant accès au dépôt privé peut lire la base de démonstration.
  Retirez la base du dépôt et choisissez un transfert sécurisé avant d’y stocker
  des données réelles ou confidentielles.
