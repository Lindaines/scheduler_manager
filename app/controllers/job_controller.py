from datetime import datetime
from app.persistences.mongodb_persistence import MongoDB
import settings


class JobController:
    def __init__(self):
        self._mongo = MongoDB()
        self.configs = settings.load_config()

    def _agregate_result_by_expecteded_execution_time_sum(self, jobs: list):
        pass
    def _convert_date(self, date):
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    def create_job(self, id_job: str, description_job: str, maximum_date_finish: str,
                   expected_time_in_hours_to_finish: str):
        document = {
            "id_job": id_job,
            "description_job": description_job,
            "maximum_date_finish": self._convert_date(maximum_date_finish),
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

    def get_jobs_by_date_interval(self, start_datetime: str, end_datetime: str):
        try:
            if start_datetime and datetime:
                query = {"maximum_date_finish": {"$gte": self._convert_date(start_datetime),
                                                 "$lte": self._convert_date(end_datetime)}}
                result = self._mongo.find_all(self.configs.MONGO_COLLECTION_JOBS, query, sort_key="maximum_date_finish")
            result = self._mongo.find_all(self.configs.MONGO_COLLECTION_JOBS, sort_key="maximum_date_finish")
        except Exception as e:
            raise Exception(e)
