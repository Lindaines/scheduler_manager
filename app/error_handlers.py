from werkzeug.exceptions import Conflict, NotFound

from app.utils.format_response_api import Response


def configuration(app):
    @app.api.errorhandler(NotFound)
    def not_found(e):
        return Response().send(
            data=None,
            message=e.description,
            code=str(e.name).replace(" ", "_").lower(),
            status=e.code,
        )

    @app.api.errorhandler(Conflict)
    def conflict(e):
        return Response().send(
            data=None,
            message=e.description,
            code=str(e.name).replace(" ", "_").lower(),
            status=e.code,
        )

    @app.api.errorhandler
    def default_error_handler(e):
        raise Exception(e)
