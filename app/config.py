from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_HOST: str = 'localhost'
    DB_NAME: str = 'book_management'
    DB_PORT: str = '5432'
    SECRET_KEY: str = 'cc8a59b6b70c94d9d6ec025ceb1a5ebb2f242d0a6007be084850d2bae473a484'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENVIRONMENT: str = 'test'

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
