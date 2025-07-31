import pathlib

from google.genai import types, Client

from constants import ENV


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
    client = Client(api_key=ENV.google_api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["Text", "Image"]),
    )

    save_image(response, "image.png")

    return True
