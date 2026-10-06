# 💡 ADR-002 : Choix de la File d'Attente de Tâches Asynchrones — ARQ vs Celery

**Date** : 2026-10-06  
**Statut** : Accepté  
**Décideur** : DevOps Candidate  

---

## 1. Contexte & Problématique
Dans notre architecture FastAPI, nous devons exécuter des tâches en arrière-plan (envoi d'e-mails, génération de rapports, nettoyage en tâche de fond). FastAPI repose sur la boucle d'événements asynchrone Python (`asyncio`). Il est nécessaire de choisir une file d'attente de tâches qui ne bloque pas l'Event Loop et qui offre une grande légèreté.

---

## 2. Options Étudiées

### Option A : Celery + RabbitMQ / Redis
- **Avantages** : Standard historique en Python, très riche en fonctionnalités (workflows complexes, retries, periodic tasks via Celery Beat).
- **Inconvénients** : Architecture historiquement **synchrone** et lourde. L'intégration avec du code `asyncio` exige d'exécuter des boucles d'événements imbriquées ou des wrappers, ce qui peut générer des blocages de threads ou des fuites de ressources sous forte charge.

### Option B : ARQ (Async Redis Queue) — (Option Retenue)
- **Avantages** :
  - Développé spécifiquement pour **Python `asyncio`** et **Redis**.
  - Intégration à 100% avec le modèle non-bloquant de FastAPI.
  - Extrêmement rapide, léger (< 5 Mo de RAM par worker) et simple à configurer.
  - Réutilisation directe des sessions `asyncpg` et des fonctions `async def`.
- **Inconvénients** : Moins de fonctionnalités avancées que Celery pour des workflows distribués géants (pas besoin pour notre périmètre).

---

## 3. Décision Retenue

> [!IMPORTANT]
> **Choix retenu** : **ARQ (Async Redis Queue)**  
> **Raison principale** : ARQ s'intègre naturellement avec l'écosystème asynchrone de FastAPI et SQLAlchemy 2.0 Async, éliminant les risques d'incompatibilité de threads propres à Celery.

---

## 4. Conséquences & Impacts
- **Impacts Positifs** : Code asynchrone unifié, empreinte mémoire minimale, simplicité de déploiement en conteneur Docker.
- **Compromis** : Utilisation exclusive de Redis comme backend de message broker.
