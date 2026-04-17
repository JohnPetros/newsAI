from fastmcp import FastMCP
from fastmcp.server.http import StarletteWithLifespan
from starlette.middleware import Middleware

from newsai.ai.fast_mcp.tools import (
    UpdatePostContentTool,
    UpdatePostImageTool,
    UpdatePostReviewStatusTool,
    UpdatePostSlugTool,
    UpdatePostTitleTool,
)
from newsai.rest.middlewares.verify_api_key_middleware import VerifyApiKeyMiddleware


class FastMcpApp:
    @staticmethod
    def register() -> StarletteWithLifespan:
        mcp = FastMCP("News AI Mcp")

        UpdatePostContentTool.handle(mcp)
        UpdatePostImageTool.handle(mcp)
        UpdatePostTitleTool.handle(mcp)
        UpdatePostSlugTool.handle(mcp)
        UpdatePostReviewStatusTool.handle(mcp)

        return mcp.http_app(path="/", middleware=[Middleware(VerifyApiKeyMiddleware)])
