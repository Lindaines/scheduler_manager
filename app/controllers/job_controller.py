from datetime import datetime
from app.persistences.mongodb_persistence import MongoDB
from app.utils import filter_job_result
from bson.objectid import ObjectId
from app.persistences.rabbitmq import RabbitMQClient
from app.helpers import job
import settings


class JobController:
    def __init__(self):
        self.rabbitmq = RabbitMQClient()
        self._mongo = MongoDB()
        self.configs = settings.load_config()

    def _agregate_result_by_expecteded_execution_time_sum(self, jobs: list):
        return filter_job_result.get_result_filtered(jobs)

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
            job['id'] = id_job
            self.rabbitmq.publish()
            inserted_id = self._mongo.save_one(
                document, collection=self.configs.MONGO_COLLECTION_JOBS
            )
            return inserted_id
        except Exception as e:
            raise Exception(e)

    def get_jobs(self, start_datetime: str, end_datetime: str):
        try:
            if start_datetime and datetime:
                query = {"maximum_date_finish": {"$gte": self._convert_date(start_datetime),
                                                 "$lte": self._convert_date(end_datetime)}}
                result = self._mongo.find_all(self.configs.MONGO_COLLECTION_JOBS, query, sort_key="maximum_date_finish")
            else:
                result = self._mongo.find_all(self.configs.MONGO_COLLECTION_JOBS, sort_key="maximum_date_finish")
            return result
        except Exception as e:
            raise Exception(e)

    def get_jobs_grouped(self, start_datetime: str, end_datetime: str):
        try:
            if start_datetime and datetime:
                query = {"maximum_date_finish": {"$gte": self._convert_date(start_datetime),
                                                 "$lte": self._convert_date(end_datetime)}}
                result = self._mongo.find_all(self.configs.MONGO_COLLECTION_JOBS, query, sort_key="maximum_date_finish")
            else:
                result = self._mongo.find_all(self.configs.MONGO_COLLECTION_JOBS, sort_key="maximum_date_finish")
            return self._agregate_result_by_expecteded_execution_time_sum(result)
        except Exception as e:
            raise Exception(e)

    def update_job(self, id: str, new_status: str):
        try:
            result = self._mongo.update_one(
                self.configs.MONGO_COLLECTION_JOBS,
                {"_id": ObjectId(id)},
                {"$set": {"status_job": new_status}}, upsert=True,
            )
            return result
        except Exception as e:
            raise Exception(e)
