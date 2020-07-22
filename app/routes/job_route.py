from flask_restplus import Resource
from flask import request

from app.handlers.job_handler import JobHandler
from app.restplus import api
from app.schemas.routes.job_schema import JobSchema

ns = api.namespace(path="/jobs", name="Jobs", description="CRUD JOBS")

schema = JobSchema()


@ns.route("")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=404, description="not_found")
class Job(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job = JobHandler()

    @api.response(code=200, description="success", schema=JobSchema)
    def post(self):
        """
        Create a new job
        """
        return self.job.create(request.json)

    def get(self):
        """
        Create a new job
        """
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        return self.health.verify()
