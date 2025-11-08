from pydantic_settings import BaseSettings
from pydantic import Field
class Settings(BaseSettings):
	DATABASE_URL: str = Field(..., env="DATABASE_URL")
	SECRET_KEY: str = Field(..., env="SECRET_KEY")
	ALGORITHM: str = Field("HS256", env="ALGORITHM")
	ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")

	class Config:
		env_file = ".env"

settings = Settings()
