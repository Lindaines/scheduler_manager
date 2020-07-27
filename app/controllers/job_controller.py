from datetime import datetime, timedelta
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
        try:
            return datetime.strptime(date.strip(), '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return datetime.strptime(date.strip()[:19], '%Y-%m-%dT%H:%M:%S')

    def _convert_date_to_str(self, date):
        return date.strftime('%Y-%m-%dT%H:%M:%S')

    def create_job(self, description_job: str, maximum_date_finish: str,
                   expected_time_in_hours_to_finish: str):
        start_date = self._convert_date(maximum_date_finish) - timedelta(hours=8)
        document = {
            "description_job": description_job,
            "maximum_date_finish": self._convert_date(maximum_date_finish),
            "expexted_time_in_hours_to_finish": int(expected_time_in_hours_to_finish),
            "start_date": start_date,
            "status_job": "CREATED"
        }

        try:
            inserted_id = self._mongo.save_one(
                document, collection=self.configs.MONGO_COLLECTION_JOBS
            )
            job.package['id_job'] = str(inserted_id)
            job.package['start_date'] = self._convert_date_to_str(start_date)
            job.package['status_job'] = job.CREATE
            self.rabbitmq.publish(exchange=self.configs.EXCHANGE_NAME, message=job.package,
                                  routing_key=description_job)
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

    def update_job(self, id_job: str, new_status: str, description: str):
        try:
            result = self._mongo.update_one(
                self.configs.MONGO_COLLECTION_JOBS,
                {"_id": ObjectId(id_job)},
                {"$set": {"status_job": new_status}}, upsert=True,
            )
            job.package['id_job'] = id_job
            job.package['status_job'] = new_status
            self.rabbitmq.publish(exchange=self.configs.EXCHANGE_NAME, message=job.package,
                                  routing_key=description)

            return result
        except Exception as e:
            raise Exception(e)
