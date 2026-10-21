from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    database_url: str
    db_user: str
    db_password: str
    db_name: str
    debug: bool = False
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int

settings = Settings()