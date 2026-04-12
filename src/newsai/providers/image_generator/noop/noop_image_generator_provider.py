from newsai.core.interfaces.image_generator_provider import ImageGeneratorProvider


class NoopImageGeneratorProvider(ImageGeneratorProvider):
    def generate(self, prompt: str) -> bool:
        _ = prompt
        return False
