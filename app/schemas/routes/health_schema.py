from flask_restplus import fields
from app.restplus import api
from app.schemas.routes import response_serializer


class HealthSchema:
    def __init__(self):
        self._name = "Health"

    @property
    def health(self):
        """
        Health's serializer
        """
        return api.inherit(self._name, self._obj_health)

    @property
    def response_health(self):
        """
        Serializer de resposta do health
        """
        return response_serializer(
            data=self.health, name_model=f"{self._name}Response", multiple=False
        )

    @property
    def _obj_health(self):
        return {"datetime": fields.String(readonly=True)}
