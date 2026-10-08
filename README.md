# Epidemia — Dashboard épidémiologique de la RDC

Epidemia est une application web interactive construite avec Streamlit. Elle
permet d’explorer et de simuler la propagation d’une maladie infectieuse dans
les zones de santé de la République démocratique du Congo, en tenant compte de
la mobilité entre infrastructures et des capacités hospitalières.

## Fonctionnalités

- **Comptes et accès** : connexion, demande d’inscription avec approbation
  administrative, changement de mot de passe et déconnexion.
- **Administration** : approbation ou refus des demandes, gestion des statuts
  et des rôles, consultation des utilisateurs et journal des activités.
- **Simulation épidémiologique** : modèles SIR/SEIR configurés par maladie,
  sélection d’une province, choix aléatoire ou manuel du foyer initial,
  durée de simulation et taux d’hospitalisation ajustables.
- **Mobilité et propagation spatiale** : intensité de mobilité et friction avec
  la distance réglables, avec option d’inclure des infrastructures proches dans
  les provinces voisines.
- **Résultats interactifs** :
  - courbes épidémiologiques à l’échelle provinciale et par zone de santé ;
  - carte de propagation avec évolution dans le temps ;
  - indicateurs de pics, de lits nécessaires et de déficit capacitaire ;
  - analyse de sensibilité et comparaison de scénarios d’hospitalisation ;
  - tableaux de synthèse, d’évolution journalière et de cas par zone.
- **Exports** : rapports Excel et téléchargements de tableaux et de graphiques.

Les provinces, maladies, zones de santé et infrastructures sont chargées depuis
la base de données SQLite. Les options de maladie et leurs paramètres sont donc
déterminés par le contenu de `epidemia.db`.

## Technologies

- Python et Streamlit
- NumPy, Pandas et SciPy pour les calculs et le traitement des données
- SQLAlchemy et SQLite pour les données et les comptes
- Plotly et Matplotlib pour les graphiques
- Folium/Streamlit-Folium pour les visualisations cartographiques compatibles
- OpenPyXL pour la génération des rapports Excel

## Prérequis

- Python 3.11 ou 3.12
- Git (pour cloner le projet)
- Le fichier `epidemia.db` fourni avec l’application

La base doit contenir les tables suivantes :

| Table | Colonnes utilisées par l’application |
| --- | --- |
| `zonesante` | `idZone`, `NomZone`, `province`, `population_2026`, `capacite_totale` |
| `infrastructures` | `idZone`, un nom d’infrastructure, `latitude`, `longitude` |
| `maladie` | `NomMaladie`, `modele`, `Ro`, `D`, `E`, `DureeSejourLits` |

Le nom de la colonne d’infrastructure est détecté automatiquement. L’application
lit aussi la colonne facultative `TauxHospitalisation` lorsqu’elle est présente.
Elle crée au premier démarrage les tables `utilisateurs`,
`activites_dashboard` et `sessions_auth` si elles ne sont pas déjà présentes.

## Installation et lancement local

Depuis PowerShell :

```powershell
git clone https://github.com/VuningomaClemence/Epidemia-TH.git
cd Epidemia-TH
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install streamlit numpy pandas scipy sqlalchemy plotly matplotlib folium streamlit-folium openpyxl
streamlit run epidemiaTH.py
```

Le fichier `epidemia.db` doit se trouver à la racine du projet, à côté de
`epidemiaTH.py`. Pour utiliser une autre base, définissez la variable
`EPIDEMIA_DB_PATH` avant le lancement :

```powershell
$env:EPIDEMIA_DB_PATH = "C:\chemin\vers\epidemia.db"
streamlit run epidemiaTH.py
```

Streamlit affiche ensuite une adresse locale, généralement
`http://localhost:8501`.

## Première connexion et comptes

La base incluse peut déjà contenir des comptes. Connectez-vous avec un compte
administrateur configuré dans cette base ; les identifiants ne sont pas publiés
dans ce README. Un utilisateur sans compte peut soumettre une demande d’accès,
qui doit être approuvée par un administrateur avant la connexion.

Après une approbation ou un rejet, Epidemia envoie un courriel au demandeur.
L’envoi utilise Gmail SMTP et nécessite un mot de passe d’application Gmail
(l’authentification à deux facteurs doit être activée sur le compte expéditeur).
L’application essaie d’abord STARTTLS sur le port 587, puis utilise TLS sur le
port 465 si la connexion est coupée avant l’envoi. Une coupure pendant l’envoi
n’entraîne pas de nouvel essai automatique, afin d’éviter les courriels en double.
Configurez les secrets suivants dans **Manage app > Settings > Secrets** sur
Streamlit Community Cloud :

```toml
[email]
sender_email = "votre-adresse@gmail.com"
app_password = "mot-de-passe-d-application"
```

En local, placez la même configuration dans `.streamlit/secrets.toml` à la
racine du projet. Ce fichier ne doit jamais être ajouté au dépôt. Si les secrets
ne sont pas configurés ou si Gmail refuse l’envoi, la décision d’accès reste
enregistrée et l’administrateur voit un avertissement dans le panneau.

Si l’application est lancée avec une base ne contenant encore aucun compte
administrateur, elle crée un compte initial :

- Identifiant : `admin`
- Mot de passe : `admin123`

Ce mot de passe initial n’est créé que lorsqu’aucun administrateur n’existe.
Changez-le immédiatement si ce compte est utilisé. Ne réutilisez pas la base de
démonstration ni ses comptes pour un déploiement avec des données réelles.

## Utilisation du tableau de bord

1. Connectez-vous. Les administrateurs peuvent basculer entre le tableau de bord
   épidémiologique et l’espace **Supervision & Administration**.
2. Dans la barre latérale, choisissez une province et une maladie.
3. Choisissez un foyer initial aléatoire (avec possibilité de fixer la graine
   pour reproduire le tirage) ou une infrastructure précise.
4. Réglez le taux d’hospitalisation, la durée, la mobilité et la friction
   spatiale. Activez éventuellement l’inclusion des zones proches des provinces
   voisines et définissez la distance maximale.
5. Lancez la simulation, puis explorez les onglets **Courbes
   Épidémiologiques**, **Carte Interactive de la Province**, **Analyse de
   Sensibilité**, **Synthèse & Données Détaillées** et **Exportation Excel**.

## Données et déploiement

La base SQLite conserve les comptes, les sessions, les activités et les données
de référence. Protégez `epidemia.db` et les sauvegardes ; ne placez pas de
données de santé personnelles ou confidentielles dans un dépôt accessible au
public.

Pour héberger l’application, le fichier SQLite doit être stocké sur un volume
persistant et son chemin fourni via `EPIDEMIA_DB_PATH`. Une instance Streamlit
unique est recommandée avec SQLite ; le système de fichiers éphémère d’un
hébergeur ne convient pas à la conservation de la base après redémarrage.
