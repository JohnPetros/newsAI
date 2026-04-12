from newsai.ai.agno import AgnoGeneratePostWorkflow
from newsai.core.interfaces.generate_post_workflow import GeneratePostWorkflow


class AiPipe:
    @staticmethod
    def get_generate_post_workflow() -> GeneratePostWorkflow:
        return AgnoGeneratePostWorkflow()
