class HttpServiceUnvailable(Exception):

    def __init__(self, message: str) -> None:
        
        self.message = message
        self.status_code = 503
        self.name = "ServiceUnvailable"