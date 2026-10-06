# 🐳 DevOps, Infra & Continuous Operations

> Cette section synthétise la vision, la pile d'outils et les meilleures pratiques d'infrastructure automatisée, de sécurité et d'observabilité appliquées sur tous nos projets.

---

## ⚡ Expérience Développeur & La Règle des 3 Minutes (Recruteurs)

Un recruteur ou Tech Lead passe **moins de 5 minutes** sur un projet. L'environnement doit pouvoir s'initialiser, exécuter les migrations DB et se tester en **une seule commande** grâce à un `Makefile` universel :

```bash
# 1. Lancer l'intégralité du stack & appliquer automatiquement les migrations Alembic
make up

# 2. Peupler la base de données avec des données de test de démonstration
make seed

# 3. Lancer la suite de tests et afficher le rapport de couverture Pytest
make test
```

### Extrait du `Makefile` Standard
```makefile
.PHONY: up down migrate seed test lint

up:
	docker compose up -d --build
	@echo "Attente du démarrage de PostgreSQL..."
	docker compose exec api alembic upgrade head

migrate:
	docker compose exec api alembic upgrade head

seed: migrate
	docker compose exec api python -m app.db.seed

test:
	docker compose exec api pytest --cov=app --cov-report=term-missing

lint:
	ruff check . && hadolint Dockerfile
```

---

## ☁️ Hébergement Cloud Gratuit (0 €) : Koyeb + Neon DB

Pour éviter les pièges classiques des hébergeurs gratuits (comme la mise en veille agressive de 50s et la suppression de base après 90 jours sur Render) :

| Composant | Service Gratuit | Pourquoi ce choix ? |
|---|---|---|
| **API Conteneurisée** | **Koyeb** (ou Hugging Face Spaces Docker) | Hébergement Docker fluide sans suppression de conteneur, réponse rapide. |
| **Base de Données** | **Neon DB** | PostgreSQL Serverless gratuit **pérenne** (0.5 Go), sans suppression automatique de base au bout de 90 jours. |
| **Pinger Keep-Alive** | **UptimeRobot** / **Cron-Job.org** | Envoi d'un ping HTTP `GET /health` toutes les 10 min pour maintenir le conteneur éveillé 24/7. |

---

## 🔒 Authentification Decap CMS (Gatekeeper OAuth Proxy)

Decap CMS (situé dans `docs/admin/`) est hébergé sur GitHub Pages (statique). Pour permettre l'authentification OAuth GitHub depuis le navigateur :
1. Un proxy OAuth léger (**Gatekeeper**) est déployé sur Koyeb/Cloudflare Worker.
2. Il gère l'échange sécurisé du `code` OAuth contre un `access_token` GitHub sans exposer de secrets client dans le navigateur.

---

## 📊 Auto-Provisioning Grafana

Au lieu de demander à l'utilisateur de configurer les Data Sources Grafana à la main, tout est automatisé au démarrage du conteneur via le dossier `grafana/provisioning/` :
- **DataSources** : Connexion automatique à Prometheus (`http://prometheus:9090`).
- **Dashboards** : Importation automatique des fichiers JSON représentant le taux de requêtes, le P95 de latence et le statut du pool DB.
