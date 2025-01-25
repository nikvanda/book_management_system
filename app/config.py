from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str = '5432'
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
