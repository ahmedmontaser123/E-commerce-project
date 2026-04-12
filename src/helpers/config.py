from pydantic_settings import BaseSettings
class settings(BaseSettings):
    APP_NAME : str
    APP_VERSION : str
    Postgress_USERNAME: str
    Postgress_PASSWORD: str
    Postgress_HOST: str
    Postgress_PORT: int
    Postgress_MAIN_DATABASE: str

    class config:
        env_file = ".env"

    

def get_settings():
    return settings()   




