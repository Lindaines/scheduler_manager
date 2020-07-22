from flask_marshmallow import Schema
from marshmallow import fields, ValidationError, validate

import uuid


def _generate_uuid():
    return str(uuid.uuid4())


class JobSchema(Schema):
    id_job = fields.String(required=True)
    description_job = fields.DateTime(required=True)
    maximum_date_finish = fields.DateTime(required=True)
    expected_time_in_hours_to_finish = fields.DateTime(required=True)
    status_job = fields.String(required=True)
    expected_time_alert_triggered = fields.Bool(required=False)
