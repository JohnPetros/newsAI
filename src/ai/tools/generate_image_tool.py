import os
import google.genai as genai
from google.genai import types
import pathlib
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"],
)

MODEL_ID = "gemini-2.0-flash-exp-image-generation"


def save_image(response: types.GenerateContentResponse, path: str) -> None:
    for part in response.candidates[0].content.parts:  # type: ignore
        if part.text is not None:
            continue

        if part.inline_data is not None:
            data = part.inline_data.data
            pathlib.Path(path).write_bytes(data)  # type: ignore


def generate_image_tool(prompt: str) -> bool:
    """
    Generate an image for a blog post according to the provided content.

    Args:
        prompt(str): The prompt to generate the image.

    Returns:
        bool: True if the image was generated successfully, False otherwise.
    """

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["Text", "Image"]),
    )

    save_image(response, "image.png")

    return True
