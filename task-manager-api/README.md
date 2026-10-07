# 🚀 Task Manager API — Backend Microservice

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1.svg)](https://www.postgresql.org/)
[![Redis ARQ](https://img.shields.io/badge/Redis-ARQ-DC382D.svg)](https://arq-docs.helpmanual.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> API REST asynchrone de gestion de tâches hautement performante et sécurisée conçue avec FastAPI, SQLAlchemy 2.0 Async, PostgreSQL, ARQ Redis et supervisée avec Prometheus & Grafana.

---

## 🏗️ Architecture & Composants

```text
task-manager-api/
├── app/
│   ├── api/                  # Endpoints REST V1 (Auth, Tasks) & Dépendances deps.py
│   ├── core/                 # Config Pydantic v2, Security Bcrypt/JWT & Async Engine DB
│   ├── models/               # Modèles ORM SQLAlchemy 2.0 (User, Task)
│   ├── schemas/              # DTOs Pydantic (Validation & Sérialisation)
│   ├── services/             # Logique métier & Middleware Correlation ID
│   ├── workers/              # Worker asynchrone ARQ Redis
│   └── main.py               # Point d'entrée FastAPI & Metrics Prometheus
├── tests/                    # Suite Pytest (NullPool & Transaction Rollback)
├── alembic/                  # Migrations DB versionnées
├── monitoring/               # Auto-provisioning Prometheus & Grafana
├── docker-compose.yml        # Stack globale (API, DB, Redis, Worker, Prom, Grafana)
├── Dockerfile                # Multi-stage build Python 3.12 non-root
├── Makefile                  # Règle des 3 Minutes (make up, make seed, make test)
└── .env.example              # Variables d'environnement exemple
```

---

## ⚡ Démarrage Rapide en 1 Commande (3-Minute Rule)

### Prérequis
- Docker & Docker Compose

### Lancer la Stack complète & appliquer les migrations
```bash
make up
```

### Remplir la base de données avec des données de démonstration
```bash
make seed
```

### Exécuter la suite de tests avec couverture de code
```bash
make test
```

---

## 📊 Endpoints & Dashboards

- **Documentation OpenAPI / Swagger** : `http://localhost:8000/docs`
- **Endpoint Health Check** : `http://localhost:8000/health`
- **Métriques Prometheus** : `http://localhost:8000/metrics`
- **Prometheus UI** : `http://localhost:9090`
- **Grafana Dashboards** : `http://localhost:3000` (Login: `admin` / Password: `admin`)

---

## 🔒 Sécurité & Traçabilité

- **Authentification JWT** : Jetons signés avec expiration et chiffrement des mots de passe avec Bcrypt.
- **Correlation ID Header** : En-tête `X-Correlation-ID` injecté à chaque requête et transmis dans les jobs ARQ pour un suivi de bout en bout des logs dans Loki/Grafana.
