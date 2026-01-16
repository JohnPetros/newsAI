from inngest import Inngest, fast_api
from logging import getLogger
from fastapi import FastAPI

from constants import ENV
from messaging.jobs import GeneratePostJob


class InngestMessaging:
    @staticmethod
    def register(app: FastAPI) -> Inngest:
        inngest = Inngest(
            app_id="News AI Messaging",
            logger=getLogger("uvicorn"),
            signing_key=ENV.inngest_signing_key,
        )

        fast_api.serve(app, inngest, [GeneratePostJob.handle(inngest)])

        return inngest
