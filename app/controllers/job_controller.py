from datetime import datetime
from app.persistences.mongodb_persistence import MongoDB
import settings


class JobController:
    def __init__(self):
        self._mongo = MongoDB()
        self.configs = settings.load_config()

    def create_job(self, id_job: str, description_job: str, maximum_date_finish: str,
                   expected_time_in_hours_to_finish: str):
        document = {
            "id_job": id_job,
            "description_job": description_job,
            "maximum_date_finish": datetime.strptime(maximum_date_finish, '%Y-%m-%d %H:%M:%S')
            ,
            "expexted_time_in_hours_to_finish": expected_time_in_hours_to_finish,
            "expected_time_alert_triggered": False,
            "status_job": "CREATED"
        }
        try:
            inserted_id = self._mongo.save_one(
                document, collection=self.configs.MONGO_COLLECTION_JOBS
            )
            return inserted_id
        except Exception as e:
            raise Exception(e)
