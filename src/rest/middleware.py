from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from constants import ENV


class Middleware:
    @staticmethod
    def verify_api_key(
        api_key: str = Depends(APIKeyHeader(name="X-Api-Key", auto_error=False)),
    ) -> str:
        print(api_key)
        print(ENV.api_key)
        if api_key != ENV.api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return api_key
