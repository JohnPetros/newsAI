from sys import path as sys_path
from os import path as os_path

from dotenv import load_dotenv

load_dotenv()

from ai.news_workflow import NewsWorkflow


sys_path.append(os_path.dirname(os_path.abspath(__file__)))


# from fastapi import FastAPI


# app = FastAPI()


# @app.get("/")
# def read_root() -> dict[str, str]:
#     return {"message": "News AI is coming soon"}


if __name__ == "__main__":
    workflow = NewsWorkflow()
    workflow.start()
