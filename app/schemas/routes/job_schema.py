from flask_marshmallow import Schema
from marshmallow import fields, validate


class JobSchema(Schema):
    id_job = fields.String(required=True)
    description_job = fields.String(required=True)
    maximum_date_finish = fields.String(required=True)
    expected_time_in_hours_to_finish = fields.String(required=True)
    status_job = fields.String(required=True)
    expected_time_alert_triggered = fields.Bool(required=False)
