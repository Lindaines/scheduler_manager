from marshmallow import fields, ValidationError, Schema
from marshmallow.validate import Range
from flask_restplus import fields
from app.restplus import api
from app.schemas.routes import response_serializer
from datetime import datetime
import settings

configs = settings.load_config()


def _validate_description(data):
    if not data in configs.DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA:
        raise ValidationError("This job is not allowed")


def _validate_max_data(data):
    data = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    if data <= datetime.now():
        raise ValidationError("The max data must be greater than now")


class JobSchema(Schema):
    description_job = fields.String(required=True, validate=_validate_description)
    maximum_date_finish = fields.String(required=True, validate=_validate_max_data)
    expected_time_in_hours_to_finish = fields.Integer(required=True, validate=Range(max=8))


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
            'expected_time_in_hours_to_finish': fields.Integer(max=8),
        }
