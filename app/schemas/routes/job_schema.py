from marshmallow import ValidationError, Schema, fields
from marshmallow.validate import Range
from datetime import datetime
import settings

configs = settings.load_config()


def _get_formated_date(date):
    try:
        return datetime.strptime(date.strip(), '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(date.strip()[:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            raise ValidationError("Invalid format date")


def _validate_date_format(data):
    try:
        datetime.strptime(data.strip(), '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        try:
            datetime.strptime(data.strip()[:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            raise ValidationError("Invalid format date")


def _validate_description(data):
    if not data in configs.DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA:
        raise ValidationError("This job is not allowed")


def _validate_max_data(data):
    try:
        data = _get_formated_date(data)
    except ValueError:
        raise ValidationError("Invalid format for max value")
    if data <= datetime.now():
        raise ValidationError("The max data must be greater than now")


class JobSchema(Schema):
    description_job = fields.String(required=True, validate=_validate_description)
    maximum_date_finish = fields.String(required=True, validate=[_validate_date_format, _validate_max_data])
    expected_time_in_hours_to_finish = fields.Integer(required=True, validate=Range(max=8))


class JobGetSchema(Schema):
    grouped = fields.Boolean(required=True)
    start_time = fields.String(required=True, validate=_validate_date_format)
    end_time = fields.String(required=True, validate=_validate_date_format)


