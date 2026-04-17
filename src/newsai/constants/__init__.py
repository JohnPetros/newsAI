from .env import Env
from .http_headers import HttpHeaders

ENV = Env()

HTTP_HEADERS = HttpHeaders()

__all__ = ["ENV", "HTTP_HEADERS"]
