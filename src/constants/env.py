from os import getenv
from typing import NamedTuple


class Env(NamedTuple):
    host: str = str(getenv("HOST"))
    port: int = int(getenv("PORT", 8080))
    blog_api_url: str = str(getenv("BLOG_API_URL"))
    google_api_key: str = str(getenv("GOOGLE_API_KEY"))
    api_key: str = str(getenv("API_KEY"))
