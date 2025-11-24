class HttpInternalServerError(Exception):

    def __init__(self, message: str) -> None:

        self.message = message
        self.status_code = 500
        self.name = "InternarlServerError"