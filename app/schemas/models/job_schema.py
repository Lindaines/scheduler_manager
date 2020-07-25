from flask_marshmallow import Schema
from marshmallow import fields, ValidationError, validate
from datetime import datetime
from app.helpers import job
import uuid
import settings

configs = settings.load_config()


def _generate_uuid():
    return str(uuid.uuid4())


def _validate_description(data):
    if not data in configs.DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA:
        raise ValidationError("Job not supported")


def _validate_expected_time(data):
    max_time_allowed = configs.MAX_TIME_ALLOWEWD
    if data > max_time_allowed:
        raise ValidationError(f"Max time allowed is {max_time_allowed} hours")


def _validate_max_data(data):
    if data <= datetime.now():
        raise ValidationError("Max data must be greater than now")


def _validate_status(data):
    if data not in (job.CREATE, job.CANCEL, job.DELETE):
        raise ValidationError("Status does not exists")


class JobSchema(Schema):
    description_job = fields.String(required=True, validate=_validate_description)
    maximum_date_finish = fields.DateTime(required=True)
    expected_time_in_hours_to_finish = fields.DateTime(required=True, validate=_validate_max_data)
    status_job = fields.String(required=True)
    expected_time_alert_triggered = fields.Bool(required=False)
