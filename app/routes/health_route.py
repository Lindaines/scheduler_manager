from flask_restplus import Resource

from app.handlers.health_handler import HealthHandler
from app.restplus import api
from app.schemas.routes.health_schema import HealthSchema

ns = api.namespace(path="/health", name="Health", description="Check service life")

schema = HealthSchema()


@ns.route("")
@api.doc(security=None)
@api.response(code=500, description="internal_error")
@api.response(code=404, description="not_found")
class Health(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health = HealthHandler()

    @api.response(code=200, model=schema.response_health, description="success")
    def get(self):
        """
        Check if everything is ok with the service
        """
        return self.health.verify()
