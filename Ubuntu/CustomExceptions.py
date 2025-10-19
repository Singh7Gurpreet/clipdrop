class JWTKeyNotFound(Exception):
    def __init__(self, message="Jwt token is not set as cookie"):
        super().__init__(message)