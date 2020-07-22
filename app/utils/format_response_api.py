import json

from flask import make_response
from flask import redirect

from app.utils.format_encoder_object import format_encoder_object


class Response:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}

    def send(
        self, data=None, status=200, message: str = None, code: str = None, headers=None
    ):

        if status in [204]:
            response = {}
        else:
            data = json.loads(json.dumps(data, default=format_encoder_object))

            response = {
                "status": status,
                "message": message,
                "code": code,
                "data": data,
            }

        headers = self.__format_headers(headers)
        return make_response(json.dumps(response), status, headers)

    @staticmethod
    def redirect(url, code=302):
        return redirect(url, code=code)

    def __format_headers(self, headers=None) -> dict:
        if headers is None:
            headers = {}

        try:
            for k, v in self.headers.items():
                if k.lower() not in list(map(str.lower, headers.keys())):
                    headers[k] = v
        except Exception:
            headers = self.headers
        finally:
            return headers
