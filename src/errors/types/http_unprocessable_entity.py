class HttpUnprocessableEntity(Exception):

    def __init__(self, message: str) -> None:
        
        self.message = message
        self.status_code = 422
        self.name = "UnprocessableEntity"