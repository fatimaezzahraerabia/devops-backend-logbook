import asyncio
import structlog
from sqlalchemy import select
from app.core import security
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority

logger = structlog.get_logger()


async def seed_data():
    async with AsyncSessionLocal() as session:
        logger.info("Vérification des données de démonstration...")
        result = await session.execute(select(User).where(User.email == "demo@example.com"))
        user = result.scalar_one_or_none()

        if not user:
            logger.info("Création de l'utilisateur demo@example.com...")
            user = User(
                email="demo@example.com",
                hashed_password=security.get_password_hash("DemoPassword123!"),
                full_name="Démo DevOps User",
                is_active=True,
                is_superuser=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

            logger.info("Création des tâches de démonstration...")
            tasks = [
                Task(
                    title="Mettre en place le pipeline CI/CD GitHub Actions",
                    description="Configurer Ruff, Pytest, Gitleaks, Hadolint et Trivy.",
                    status=TaskStatus.COMPLETED,
                    priority=TaskPriority.HIGH,
                    owner_id=user.id
                ),
                Task(
                    title="Déployer l'infrastructure sur Koyeb & Neon DB",
                    description="Provisionner PostgreSQL serverless et le conteneur FastAPI.",
                    status=TaskStatus.IN_PROGRESS,
                    priority=TaskPriority.HIGH,
                    owner_id=user.id
                ),
                Task(
                    title="Configurer le tableau de bord Grafana",
                    description="Connecter Prometheus et vérifier le P95 de latence.",
                    status=TaskStatus.PENDING,
                    priority=TaskPriority.MEDIUM,
                    owner_id=user.id
                ),
            ]
            session.add_all(tasks)
            await session.commit()
            logger.info("Seeding terminé avec succès !")
        else:
            logger.info("L'utilisateur de démonstration existe déjà. Seeding ignoré.")


if __name__ == "__main__":
    asyncio.run(seed_data())
