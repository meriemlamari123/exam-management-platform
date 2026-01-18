# 🎓 Plateforme de Gestion des Examens Universitaires

Application web développée avec **Streamlit** pour la gestion et la planification automatique des examens universitaires.

## 📊 Caractéristiques

- **13,000 étudiants** répartis dans 70 formations
- **1,000 professeurs** dans 7 départements
- **400 modules** d'enseignement
- **150 salles** (amphithéâtres et salles de classe)
- **Planification automatique** des examens avec détection de conflits
- **Statistiques en temps réel** avec graphiques interactifs
- **Interface multipage** intuitive

## 🚀 Installation Locale

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes

1. **Cloner le projet**
   ```bash
   git clone https://github.com/VOTRE-USERNAME/exam-management-platform.git
   cd exam-management-platform
   ```

2. **Créer un environnement virtuel** (recommandé)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialiser la base de données**
   ```bash
   python database/init_db.py
   ```

5. **Lancer l'application**
   ```bash
   streamlit run app.py
   ```

6. **Accéder à l'application**
   
   Ouvrez votre navigateur et allez sur : `http://localhost:8501`

## 📁 Structure du Projet

```
ExamProject_22222/
├── app.py                      # Page d'accueil et tableau de bord
├── requirements.txt            # Dépendances Python
├── database/
│   ├── university.db          # Base de données SQLite
│   ├── schema.sql             # Structure des tables
│   ├── init_db.py             # Script d'initialisation
│   └── data_loader.py         # Chargement des données
├── logic/
│   └── scheduler.py           # Algorithme de planification
└── pages/
    ├── 1_Administration.py    # Gestion des données
    ├── 2_Statistiques.py      # Analyses et graphiques
    ├── 3_Départements.py      # Vue par département
    └── 4_Consultation.py      # Consultation des plannings
```

## 🌐 Déploiement

Consultez le [Guide d'Hébergement Complet](guide_hebergement_complet.md) pour déployer cette application sur :

- **Streamlit Cloud** (gratuit, recommandé)
- **Render** (gratuit)
- **Railway** (5$/mois)
- **VPS** (contrôle total)

## 🛠️ Technologies Utilisées

- **Frontend** : Streamlit
- **Backend** : Python 3.11
- **Base de données** : SQLite (local) / PostgreSQL (production)
- **Visualisation** : Plotly
- **Génération de données** : Faker

## 📖 Fonctionnalités

### 1. Tableau de Bord
- Vue d'ensemble des statistiques
- Répartition des salles par type
- Distribution des professeurs par département

### 2. Administration
- Génération automatique des plannings d'examens
- Détection des conflits (salles, formations)
- Sauvegarde en base de données

### 3. Statistiques
- Graphiques interactifs
- Analyses par département
- Taux d'occupation des salles

### 4. Consultation
- Recherche par étudiant, professeur ou module
- Affichage des plannings personnalisés
- Export des données

## 🔧 Configuration

### Variables d'Environnement

Pour utiliser PostgreSQL en production, définissez :

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
```

### Fichiers de Configuration

- `.gitignore` : Fichiers à exclure de Git
- `render.yaml` : Configuration pour Render
- `Procfile` : Configuration pour Heroku/Railway
- `setup.sh` : Script d'initialisation

## 🐛 Dépannage

### Problème : "ModuleNotFoundError"
**Solution** : Installez les dépendances
```bash
pip install -r requirements.txt
```

### Problème : "Database is locked"
**Solution** : Fermez toutes les instances de l'application et relancez

### Problème : Port 8501 déjà utilisé
**Solution** : Changez le port
```bash
streamlit run app.py --server.port=8502
```

## 📝 Licence

Ce projet est développé à des fins éducatives.

## 👥 Auteur

Développé pour la gestion des examens universitaires.

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation Streamlit : [docs.streamlit.io](https://docs.streamlit.io)
2. Vérifiez les logs de l'application
3. Ouvrez une issue sur GitHub

---

**Bon déploiement ! 🚀**
