from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8080, alias="PORT")
    blog_api_url: str = Field(alias="BLOG_API_URL")
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    exa_api_key: str = Field(alias="EXA_API_KEY")
    firecrawl_api_key: str = Field(alias="FIRECRAWL_API_KEY")
    api_key: str = Field(alias="API_KEY")
    inngest_signing_key: str = Field(alias="INNGEST_SIGNING_KEY")
