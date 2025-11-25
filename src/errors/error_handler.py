from src.errors.types.http_bad_request import HttpBadRequest
from src.errors.types.http_internal_server_error import HttpInternalServerError
from src.errors.types.http_service_unvailable import HttpServiceUnvailable
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntity

from src.main.http_types.http_response import HttpResponse


def error_handler(error):

    if (isinstance(error, (HttpUnprocessableEntity, HttpBadRequest, HttpInternalServerError, HttpServiceUnvailable))):

        return HttpResponse(
            status_code= error.status_code,
            body={
                "errors":[{
                "title": error.name,
                "message": error.message
                }]
            })

    else:

          return HttpResponse(
                status_code=500,
                body={
                "errors":[{
                    "title": "Error Server",
                    "message": str(error)
                }]
                }
            )