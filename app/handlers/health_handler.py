from app.controllers.health_controller import HealthController
from app.utils.format_response_api import Response


class HealthHandler:
    def __init__(self):
        self.controller = HealthController()
        self._response = Response()

    def verify(self) -> Response:
        try:
            result = self.controller.verify()
            return self._response.send(
                data=result,
                message="All right with the service",
                code="success",
                status=200,
            )
        except Exception as e:
            return self._response.send(
                data=None, message=str(e), code="error", status=500
            )
