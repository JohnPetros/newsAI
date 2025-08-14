from fastapi import APIRouter, Depends

from rest.middleware import Middleware


class CheckApiHealthController:
    def __init__(self, router: APIRouter) -> None:
        @router.get("/health", dependencies=[Depends(Middleware.verify_api_key)])
        async def _() -> dict[str, str]:
            return {"status": "healthy"}
