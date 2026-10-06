# 💡 ADR-001 : Choix du Framework Web Python — FastAPI vs Flask vs Django

**Date** : 2026-10-06  
**Statut** : Accepté  
**Décideur** : DevOps Candidate  

---

## 1. Contexte & Problématique
Pour le projet fil rouge "API de Gestion de Tâches", nous devons choisir le framework backend Python principal. Le framework doit offrir des hautes performances I/O (requêtes asynchrones), une validation stricte des données d'entrée/sortie, une documentation API automatique et une grande simplicité d'intégration dans une architecture conteneurisée et testée.

---

## 2. Options Étudiées

### Option A : Django REST Framework (DRF)
- **Avantages** : Batteries incluses (ORM robuste, admin interface, système de gestion des utilisateurs complet).
- **Inconvénients** : Framework très lourd, empreinte mémoire importante, support asynchrone (ASGI) moins mature et historique monolithique.

### Option B : Flask
- **Avantages** : Très léger, flexible, large écosystème de bibliothèques.
- **Inconvénients** : Nécessite l'installation manuelle de nombreuses extensions (Flask-SQLAlchemy, Marshmallow, Flask-JWT), pas de validation native par types Python, WSGI synchrone par défaut.

### Option C : FastAPI (Option Retenue)
- **Avantages** :
  - Support natif du modèle **async/await** avec des performances comparables à Node.js/Go.
  - Validation et sérialisation automatique des données grâce à **Pydantic v2** et aux type hints Python.
  - Génération automatique de la documentation interactive Swagger UI (`/docs`) et ReDoc.
  - Empreinte mémoire faible, idéal pour la conteneurisation Docker et les déploiements cloud légers.
- **Inconvénients** : Pas de panneau d'administration pré-intégré comme Django (nécessite SQLAlchemy-Admin ou développement custom si besoin).

---

## 3. Décision Retenue

> [!IMPORTANT]
> **Choix retenu** : **FastAPI**  
> **Raison principale** : FastAPI offre le meilleur équilibre entre modernité asynchrone, typage strict Pydantic et légèreté d'exécution dans un environnement Docker/Kubernetes.

---

## 4. Conséquences & Impacts
- **Impacts Positifs** : Code API concis, documentation Swagger toujours à jour automatiquement, facililation de la rédaction des tests unitaires et intégration fluide avec SQLAlchemy 2.0 async.
- **Compromis** : Nous devons gérer manuellement la couche ORM (SQLAlchemy) et les migrations (Alembic) au lieu de s'appuyer sur l'ORM clé-en-main de Django.
