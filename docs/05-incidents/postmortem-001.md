# 🚨 Postmortem #001 — Saturation de la base PostgreSQL par latence Redis (Chaos Test)

**Date de l'incident** : 2026-10-06  
**Auteur / Lead Incident** : DevOps Candidate  
**Sévérité** : P2 (Majeur)  
**Durée de la panne** : 25 minutes  

---

## 1. Résumé Exécutif
Dans le cadre d'un test de **Chaos Engineering**, une panne de la mémoire cache Redis a été simulée. L'absence de mécanisme de *Circuit Breaker* ou de *Fallback Graceful* sur l'API FastAPI a entraîné une redirection massive et simultanée de toutes les requêtes de lecture vers la base PostgreSQL, provoquant une saturation immédiate du pool de connexions et des erreurs HTTP 500 pour 65% des utilisateurs.

---

## 2. Impact Métier & Technique
- **Impact Utilisateur** : Indisponibilité partielle de la consultation des tâches pendant 25 minutes.
- **Services impactés** : API FastAPI (Task Manager Service), PostgreSQL Database.
- **Perte de données** : Aucune.

---

## 3. Chronologie des Événements (UTC)

| Heure | Événement / Action |
|---|---|
| **10:00** | Extinction volontaire du conteneur Redis (`docker stop redis-cache`). |
| **10:02** | Augmentation du trafic simulé avec k6 (100 utilisateurs virtuels simultanés). |
| **10:03** | Alerte Grafana déclenchée : `PostgresPoolSaturation (> 90%)` et `HTTP5xxRate (> 15%)`. |
| **10:07** | Inspection des logs via Loki : Présence massive de `sqlalchemy.exc.TimeoutError`. |
| **10:15** | Implémentation du patch de fallback dans FastAPI pour intercepter les exceptions Redis Connection. |
| **10:20** | Redéploiement à chaud du service API FastAPI (`docker compose up -d --build`). |
| **10:25** | Rétablissement du conteneur Redis et confirmation de la stabilisation des métriques HTTP 200. |

---

## 4. Cause Racine (Root Cause)
Le code Python appelait Redis sans bloc `try/except RedisError` avec un timeout trop long. Lorsque Redis est devenu injoignable, chaque Worker Uvicorn restait bloqué pendant 5 secondes avant d'exécuter la requête directement en base de données SQL. Le pool de connexions SQLAlchemy (limité à 20 connexions) a été instantanément saturé par le Thundering Herd.

---

## 5. Actions Préventives & Correctives (CAPA)

| Action | Type | Responsable | Statut |
|---|---|---|---|
| Encapsuler les appels Redis dans un fallback dégradé silencieux avec timeout court (200ms) | Correctif code | Backend Dev | ✅ Fait |
| Augmenter la taille du pool SQLAlchemy et activer le mode `recycle` | Infrastructure | DevOps | ✅ Fait |
| Créer un test automatisé de Chaos Engineering dans la CI avec Toxiproxy | Automatisations | DevOps | 🔄 En cours |
