from json import loads as load_json
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential
from newsai.ai.agno.squad import Squad
from newsai.core.entities import Post
from newsai.core.errors.app_error import AppError
from newsai.core.interfaces.generate_post_workflow import GeneratePostWorkflow


class AgnoGeneratePostWorkflow(GeneratePostWorkflow):
    squad: Squad = Squad()

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15)
    )
    def generate_post(self, post_category: str) -> Post:
        post = None
        team_response = self._run_team(post_category)
        print("team_response", team_response)

        post = self._convert_to_post(team_response, post_category)

        image_agent_response = self._run_image_agent(post.content)
        print("image_agent_response", image_agent_response)
        image_data = self._load_json(image_agent_response)
        post.image_alt = image_data["image_alt"]

        return post

    def _run_team(self, post_category: str) -> str:
        team_response = None
        try:
            team_response = self.team.run(
                f"Crie um post de blog sobre o assunto de {post_category}",
                show_full_reasoning=False,
                stream=True,
            )
        except Exception as exception:
            raise AppError("AI Error", str(exception)) from exception

        final_response = ""
        can_include_content = False
        for chunk in team_response:
            print("chunk", str(chunk.content))
            if "```json" in str(chunk.content):
                can_include_content = True
            if can_include_content:
                final_response += str(chunk.content)

        print("final_response", final_response)

        if not final_response:
            raise AppError("AI Error", "No response from the news writing team")

        return final_response

    def _run_image_agent(self, team_response: str) -> str:
        agent_response = None
        try:
            agent_response = self.squad.image_generator_agent.run(
                team_response, stream=True
            )
        except Exception as exception:
            raise AppError("AI Error", str(exception)) from exception

        print("agent_response", agent_response)

        final_response = ""
        can_include_content = False
        for chunk in agent_response:
            if "```json" in str(chunk.content):
                can_include_content = True
            if can_include_content:
                final_response += str(chunk.content)

        if not final_response:
            raise AppError("AI Error", "No response from the image agent")

        return final_response

    def _load_json(self, response: str) -> dict[str, Any]:
        start = response.find("{")
        end = response.rfind("}") + 1
        json_text = response[start:end]
        return dict(load_json(json_text))

    def _convert_to_post(self, response: str, post_category: str) -> Post:
        data = self._load_json(response)

        return Post(
            title=data["title"],
            content=data["content"],
            category=post_category,
            reading_time=int(data["reading_time"]),
            image_alt="",
            tags=data["tags"],
        )
