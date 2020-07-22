from datetime import datetime
from logzero import logger

from app.persistences.mongodb_persistence import MongoDB


class HealthController:
    def __init__(self):
        self._mongo = MongoDB()

    def verify(self):
        try:
            self._health_check_mongodb()

            data = {
                "datetime": datetime.now().isoformat()
            }
            return data
        except Exception as e:
            raise Exception(e)

    def _health_check_mongodb(self) -> None:
        try:
            return self._mongo.test_ping()
        except Exception as e:
            logger.error(f"Failed to check mongodb: {str(e)}")
            raise Exception("Database service unavailable.")
