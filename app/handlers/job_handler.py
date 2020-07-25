from app.controllers.job_controller import JobController
from app.utils.format_response_api import Response
from datetime import datetime


class JobHandler:
    def __init__(self):
        self.controller = JobController()
        self._response = Response()

    def verify(self) -> Response:
        try:
            result = self.controller.create_job()
            return self._response.send(
                data=result,
                message="Job created",
                code="success",
                status=201,
            )
        except Exception as e:
            return self._response.send(
                data=None, message=str(e), code="error", status=500
            )

    def create(self, data) -> Response:
        try:
            result = self.controller.create_job(data.get('id_job'), data.get('description_job'),
                                                data.get('maximum_date_finish'),
                                                data.get('expected_time_in_hours_to_finish'))
            return self._response.send(
                data=result,
                message="Job created",
                code="success",
                status=201,
            )
        except Exception as e:
            return self._response.send(
                data=None, message=str(e), code="error", status=500
            )

    def get_grouped_jobs(self, start_datetime: str, end_datetime: str) -> Response:
        try:
            result = self.controller.get_jobs_grouped(start_datetime, end_datetime)
            return self._response.send(
                data=result,
                message="Jobs list",
                code="success",
                status=200,
            )
        except Exception as e:
            return self._response.send(
                data=None, message=str(e), code="error", status=500
            )

    def get(self, start_datetime: str, end_datetime: str) -> Response:
        try:
            result = self.controller.get_jobs(start_datetime, end_datetime)
            return self._response.send(
                data=result,
                message="Jobs list",
                code="success",
                status=200,
            )
        except Exception as e:
            return self._response.send(
                data=None, message=str(e), code="error", status=500
            )

    def update(self, job: dict) -> Response:
        try:
            result = self.controller.update_job(job.get('id'), job.get('status'))
            return self._response.send(
                data=result,
                message="Job Updated",
                code="success",
                status=204,
            )
        except Exception as e:
            return self._response.send(
                data=None, message=str(e), code="error", status=500
            )
