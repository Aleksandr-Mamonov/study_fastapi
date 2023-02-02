from pydantic import BaseSettings

# Checking and validating env variables. Using lowercase to name parameters, because pydantic is case-insensitive
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"


# Store all env variables in Settings instance. We can access those variables not revealing them. i.e. settings.SECRET_KEY
settings = Settings()
