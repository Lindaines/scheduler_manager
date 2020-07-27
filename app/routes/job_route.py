from flask import request

from app.handlers.job_handler import JobHandler
from app.restplus import api
from flask_restplus import Resource, fields

from app.schemas.routes.job_schema import JobSchema, JobGetSchema
from app.schemas.models.job_schema import JobModel
from app.utils.format_response_api import Response

model = api.model('Job', {
    'description_job': fields.String,
    'maximum_date_finish': fields.DateTime,
    'expected_time_in_hours_to_finish': fields.Integer(max=8),
})
schema = JobModel()

ns = api.namespace(path="/jobs", name="Jobs", description="Create and get jobs")


@ns.route("")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=404, description="not_found")
@api.response(code=400, description="bad_request")
class Job(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job = JobHandler()

    @api.expect(model)
    @api.response(code=201, description="created", model=schema.response_job)
    def post(self):
        """
        Create a new job
        """
        data, errors = JobSchema().loads(request.data)

        if errors:
            return Response().send(
                data=None, status=400, code="bad_request", message=errors
            )
        return self.job.create(request.json)

    @api.doc(params={'start_time': 'Start date window in format 2020-07-27T15:10:21',
                     'end_time': 'End date window in format 2020-07-27T15:10:21',
                     'grouped': 'bool indicating if the jobs must be grouped in sublists'})
    def get(self):
        """
        Get jobs possibly filtered by window update and grouped or not by expected finish time job sublists that sum 8 hours max each
        """
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        grouped = request.args.get('grouped')
        if isinstance(grouped, str):
            grouped = False if grouped.upper() == "FALSE" else True
        data, errors = JobGetSchema().load({'start_time': start_time, 'end_time': end_time, 'grouped': grouped})
        if errors:
            return Response().send(
                data=None, status=400, code="bad_request", message=errors
            )

        if grouped:
            return self.job.get_grouped_jobs(start_time, end_time)
        else:
            return self.job.get(start_time, end_time)
