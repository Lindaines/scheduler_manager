from http import HTTPStatus

from werkzeug.exceptions import NotFound
from werkzeug.routing import RequestRedirect

from app.utils.format_response_api import Response


def configuration(app):
    @app.before_request
    def before_request():
        ...

    @app.after_request
    def after_request(response):
        """
        Function triggered when the request is finish, in this case to prevent cache
        """
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Cache-Control", "no-store")
        response.headers.add("Pragma", "no-cache")
        response.headers.add("Server", "no-server")
        return response

    @app.errorhandler(Exception)
    def handle_exception(err):
        if isinstance(err, NotFound):
            return Response().send(
                code="not_found",
                status=HTTPStatus.NOT_FOUND,
                message="The route you entered was not found",
            )
        elif isinstance(err, RequestRedirect):
            return err
        else:
            return Response().send(
                code="internal_error",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=str(err),
            )
