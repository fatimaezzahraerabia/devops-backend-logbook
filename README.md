# 🚀 DevOps & Backend Engineering Logbook

[![Deploy Docs](https://github.com/fatimaezzahraerabia/devops-backend-logbook/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/fatimaezzahraerabia/devops-backend-logbook/actions/workflows/deploy-docs.yml)
[![Documentation](https://img.shields.io/badge/docs-MkDocs_Material-blue.svg)](https://fatimaezzahraerabia.github.io/devops-backend-logbook/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> Carnet de bord public et portfolio technique documentant mon apprentissage, mes projets, mes choix d'architecture (ADR) et mes retours d'expérience (Postmortems) sur le stack Backend & DevOps.

---

## 🎯 Objectifs

- **Transparence et Méthode** : Prouver mes compétences techniques par du code, de l'infra as code, du monitoring et des retours d'expériences concrets.
- **Couverture SDLC (10 Étapes)** : Couvrir l'intégralité du cycle de vie logiciel (Plan, Code, Build, Test, Security, Release, Infra, Deploy, Monitor, Operate).
- **Contrainte Budget 0 €** : Utilisation exclusive de technologies Open Source et d'hébergements cloud gratuits (GitHub Pages, Koyeb, Neon DB).

---

## 🏗️ Structure du Dépôt

```text
devops-backend-logbook/
├── docs/
│   ├── index.md                 # Page d'accueil & Présentation
│   ├── admin/                   # Interface Web Decap CMS (Edition dynamique)
│   ├── 00-plan/                 # Roadmap 90 Jours
│   ├── 01-journal/              # Notes hebdomadaires (Fait, Cassé, Appris)
│   ├── 02-backend/              # Architecture Python / FastAPI / Postgres / ARQ
│   ├── 03-devops/               # Standards Docker / K8s / Terraform / Helm / Prometheus
│   ├── 04-projets/              # Fiches détaillées des projets
│   ├── 05-incidents/            # Postmortems d'incidents & Chaos Engineering
│   ├── 06-decisions/            # Architecture Decision Records (ADR)
│   └── 07-cheatsheets/          # Fiches mémos (Git, Docker, K8s, Linux, SQL, Redis)
├── .github/workflows/           # CI/CD Déploiement automatique sur GitHub Pages
├── mkdocs.yml                   # Configuration MkDocs Material & Mermaid.js
├── requirements.txt             # Dépendances Python
└── README.md
```

---

## 🛠️ Démarrage Rapide (Local)

### Prérequis
- Python 3.10+
- Git

### Lancer la documentation localement
```bash
# 1. Cloner le dépôt
git clone https://github.com/fatimaezzahraerabia/devops-backend-logbook.git
cd devops-backend-logbook

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer le serveur local MkDocs
mkdocs serve
```
Ouvrez ensuite votre navigateur sur `http://127.0.0.1:8000`.

---

## ✏️ Édition Dynamique via Web CMS (Sans Git Push)

Vous pouvez ajouter des notes de journal ou modifier le plan directement depuis votre navigateur sans toucher au terminal :
1. Accédez à `https://fatimaezzahraerabia.github.io/devops-backend-logbook/admin/`
2. Connectez-vous avec votre compte GitHub.
3. Rédigez ou éditez vos notes, puis cliquez sur **Publish**.
4. GitHub Actions prendra le relais pour compiler et mettre à jour le site automatiquement.

---

## 📜 Licence

- **Code & Scripts** : [MIT License](LICENSE)
- **Documentation & Articles** : [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
