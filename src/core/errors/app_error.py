class AppError(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
