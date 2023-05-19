# Rest Framework
from rest_framework import status
from rest_framework import exceptions


# Ejemplo de excepcion api, retorna un Response
class CustomValidationAPIException(exceptions.APIException):
    """CustomValidationAPIException.

    Esta excepción retorna un Response, por ejemplo, como lo hace el raise serializers.ValidationError
    de un serializador invocado desde una Vista.
    """

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail):
        self.default_detail = detail
        super(CustomValidationAPIException, self).__init__()


class NoExpectedResultException(Exception):
    """ Excepcion para indicar que una solicitud no retornó el resultado esperado. """
    pass


class FacturaExistenteAPIException(CustomValidationAPIException):
    pass