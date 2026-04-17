from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from newsai.ai.fast_mcp.mcp import FastMcpApp
from newsai.exception_handler import ExceptionHandler
from newsai.core.errors import AppError
from newsai.rest.router import Router
from newsai.pubsub.inngest_pubsub import InngestPubSub


class FastApiApp:
    @staticmethod
    def register() -> FastAPI:
        mcp_app = FastMcpApp.register()

        app = FastAPI(title="News AI", version="0.1.0", lifespan=mcp_app.lifespan)

        app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        InngestPubSub.register(app)

        app.add_exception_handler(AppError, ExceptionHandler.handle)

        app.include_router(Router.register())

        return app
