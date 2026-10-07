import structlog
from arq.connections import RedisSettings
from app.core.config import settings

logger = structlog.get_logger()


async def send_task_email_notification(ctx: dict, task_id: int, email: str, _correlation_id: str | None = None) -> bool:
    log = logger.bind(correlation_id=_correlation_id, task_id=task_id, target_email=email)
    log.info("Traitement de la notification de tâche asynchrone démarré")
    
    # Simulation d'envoi d'email asynchrone
    log.info("Email de notification de tâche envoyé avec succès")
    return True


class WorkerSettings:
    functions = [send_task_email_notification]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
