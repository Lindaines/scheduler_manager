from flask_restplus import fields
from app.restplus import api
from app.schemas.routes import response_serializer

class JobModel():
    def __init__(self):
        self._name = "Job"

    @property
    def job(self):
        """
        Job's serializer
        """
        return api.inherit(self._name, self._obj_job)

    @property
    def response_job(self):
        """
        Job's response serializer
        """
        return response_serializer(
            data=self.job, name_model=f"{self._name}Response", multiple=False
        )

    @property
    def _obj_job(self):
        return {
            'description_job': fields.String,
            'maximum_date_finish': fields.DateTime,
            'expected_time_in_hours_to_finish': fields.Integer(max=8)
        }
