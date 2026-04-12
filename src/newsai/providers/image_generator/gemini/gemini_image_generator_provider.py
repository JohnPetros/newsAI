from google.genai import types, Client


from newsai.constants import ENV


class GeminiImageGeneratorProvider:
    def generate(self, prompt: str) -> bool:
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
