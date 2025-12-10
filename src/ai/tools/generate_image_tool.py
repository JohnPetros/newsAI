from google.genai import types, Client

from constants import ENV


def generate_image_tool(prompt: str) -> bool:
    """
    Generate an image for a blog post according to the provided content.

    Args:
        prompt(str): The prompt to generate the image.

    Returns:
        bool: True if the image was generated successfully, False otherwise.
    """
    client = Client(api_key=ENV.google_api_key)

    response = client.models.generate_images(
        model="models/imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/jpeg",
            aspect_ratio="1:1",
            image_size="1K",
        ),
    )
    print(response.generated_images)
    if response.generated_images and response.generated_images[0].image is not None:
        response.generated_images[0].image.save("image.png")

    return True
