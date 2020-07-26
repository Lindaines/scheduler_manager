from flask_marshmallow import Schema
from marshmallow import fields, ValidationError, validate
from datetime import datetime
import settings

configs = settings.load_config()


def _validate_description(data):
    if not data in configs.DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA:
        raise ValidationError("This job is not supported")


def _validate_expected_time(data):
    if data > 8:
        raise ValidationError("Max time allowed is 8 hours")


def _validate_max_data(data):
    if data <= datetime.now():
        raise ValidationError("The max data must be greater than now")


class JobSchema(Schema):
    description_job = fields.String(required=True, validate=_validate_description)
    maximum_date_finish = fields.String(required=True, validate=_validate_max_data)
    expected_time_in_hours_to_finish = fields.String(required=True, validate=_validate_expected_time)
    status_job = fields.String(required=True)
    expected_time_alert_triggered = fields.Bool(required=False)
