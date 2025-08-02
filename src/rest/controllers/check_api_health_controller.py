from fastapi import APIRouter


class CheckApiHealthController:
    def __init__(self, router: APIRouter) -> None:
        @router.get("/health")
        async def _() -> dict[str, str]:
            return {"status": "healthy"}
