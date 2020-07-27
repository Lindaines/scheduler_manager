from marshmallow import ValidationError, Schema
from marshmallow.validate import Range
from flask_restplus import fields
from datetime import datetime
import settings

configs = settings.load_config()


def _validate_date_format(data):
    try:
        return datetime.strptime(data.strip(), '%Y-%m-%dT%H:%M:%S')
        # return datetime.strptime(date.strip()[:19], '%Y-%m-%dT%H:%M:%S')
    except:
        raise ValidationError("Invalid format date")


def _validate_description(data):
    if not data in configs.DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA:
        raise ValidationError("This job is not allowed")


def _validate_max_data(data):
    data = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    if data <= datetime.now():
        raise ValidationError("The max data must be greater than now")



