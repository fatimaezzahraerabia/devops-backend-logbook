# 🐍 Backend Standards & Architecture

> Cette section regroupe les principes de conception, les standards de code et les choix d'architecture appliqués aux projets Backend Python (FastAPI / PostgreSQL / ARQ Redis).

---

## 🏗️ Structure de Projet Cible (Clean Architecture)

Les projets backend sont découpés par **domaines/fonctionnalités** ou par couches clairement isolées pour garantir la testabilité et la maintenabilité :

```text
app/
├── api/                   # Handlers d'API / Routers FastAPI
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   └── api.py
├── core/                  # Configurations, Sécurité & Singletons
│   ├── config.py          # Pydantic BaseSettings (variables d'environnement)
│   ├── security.py        # Hachage mdp, création token JWT
│   └── database.py        # Engine Async SQLAlchemy & Session Local
├── models/                # Modèles ORM SQLAlchemy (Entités DB)
├── schemas/               # Schemas Pydantic (Validation DTO Input/Output)
├── services/              # Logique métier (Services isolés)
├── workers/               # Tâches asynchrones ARQ (Redis Queue)
├── db/
│   ├── seed.py            # Script de remplissage de démonstration
│   └── migrations/        # Fichiers de migration Alembic
└── main.py                # Point d'entrée de l'application FastAPI
```

---

## 🛠️ Stack Technique Backend & Exigences

| Composant | Technologie | Justification |
|---|---|---|
| **Framework Web** | **FastAPI** | Asynchrone (async/await), validation stricte avec Pydantic v2, documentation OpenAPI/Swagger auto-générée. |
| **Base de Données** | **PostgreSQL** | Base relationnelle ACID, support des requêtes JSONB et des extensions (pgvector). |
| **ORM & Migrations** | **SQLAlchemy 2.0 Async + Alembic** | Typage strict (`Mapped[]`), requêtes asynchrones, gestion versionnée des schémas DB. |
| **Cache & Worker** | **Redis + ARQ** | File d'attente nativement asynchrone (`asyncio`) sans les contraintes de blocage de threads de Celery. |
| **Authentification** | **JWT (OAuth2 avec Bearer)** | Tokens d'accès stateless avec expiration et clés de signature sécurisées. |
| **Tests & Qualité** | **Pytest + pytest-asyncio** | Suite de tests isolée avec rollback automatique des transactions SQL et `NullPool`. Coverage ≥ 70%. |

---

## 🔍 Traçabilité des Logs & Propagation du Correlation ID dans ARQ

Pour garantir l'observabilité de bout en bout dans Grafana/Loki, le `correlation_id` généré par le middleware FastAPI lors de la requête HTTP est automatiquement transmis dans les arguments du job **ARQ** :

```python
# 1. Dans le Router FastAPI (Envoi du Job ARQ avec le Correlation ID)
@router.post("/tasks/{task_id}/notify")
async def trigger_task_notification(task_id: int, request: Request):
    correlation_id = request.state.correlation_id
    await redis_pool.enqueue_job("send_task_email_job", task_id, _correlation_id=correlation_id)
    return {"message": "Notification en cours de traitement"}

# 2. Dans le Worker ARQ (Extraction et injection du Correlation ID dans Structlog)
async def send_task_email_job(ctx, task_id: int, _correlation_id: str = None):
    logger = structlog.get_logger().bind(correlation_id=_correlation_id, task_id=task_id)
    logger.info("Début du traitement de la notification email")
    # Logique d'envoi d'e-mail...
    logger.info("Notification email envoyée avec succès")
```

---

## 🧪 Stratégie de Test Pytest Async (Gestion du Pool DB)

Pour éviter d'épuiser les connexions PostgreSQL ou d'avoir des fuites de boucle d'événements entre les tests async :
1. **Isolation par Transaction Rollback** : Chaque test s'exécute dans une transaction SQL dédiée qui est systématiquement annulée (`await session.rollback()`) à la fin du test.
2. **Usage de `NullPool`** : Durant la suite de tests, l'objet `AsyncEngine` SQLAlchemy est instancié avec `poolclass=NullPool` pour ouvrir et fermer proprement les connexions sans les maintenir dans un pool global partagé.
