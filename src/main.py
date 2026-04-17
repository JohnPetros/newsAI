from sys import path as sys_path
from os import path as os_path

from dotenv import load_dotenv
from uvicorn import run


load_dotenv()

from newsai.app import FastApiApp  # noqa: E402

sys_path.append(os_path.dirname(os_path.abspath(__file__)))

app = FastApiApp.register()

if __name__ == "__main__":
    from newsai.constants import ENV

    run("main:app", host=ENV.host, port=ENV.port, reload=True)
