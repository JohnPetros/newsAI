from inngest import Inngest, fast_api
from logging import getLogger
from fastapi import FastAPI

from constants import ENV
from pubsub.jobs import GeneratePostJob


class InngestPubSub:
    @staticmethod
    def register(app: FastAPI) -> Inngest:
        inngest = Inngest(
            app_id="News AI PubSub",
            logger=getLogger("uvicorn"),
            signing_key=ENV.inngest_signing_key,
        )

        fast_api.serve(app, inngest, [GeneratePostJob.handle(inngest)])

        return inngest
