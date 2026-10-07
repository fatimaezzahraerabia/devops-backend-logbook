.PHONY: up down migrate seed test lint help

help:
	@echo "Commandes disponibles:"
	@echo "  make up       - Demarrer la stack Docker & appliquer les migrations DB"
	@echo "  make down     - Arreter la stack & supprimer les volumes"
	@echo "  make migrate  - Appliquer les migrations Alembic"
	@echo "  make seed     - Peupler la base avec les donnees de demonstration"
	@echo "  make test     - Executer les tests Pytest avec couverture"
	@echo "  make lint     - Linter le code Python et Dockerfile"

up:
	docker compose up -d --build
	@echo "Attente du demarrage de PostgreSQL..."
	sleep 5
	docker compose exec api alembic upgrade head

migrate:
	docker compose exec api alembic upgrade head

seed: migrate
	docker compose exec api python -m app.db.seed

test:
	docker compose exec api pytest --cov=app --cov-report=term-missing

down:
	docker compose down -v

lint:
	ruff check .
