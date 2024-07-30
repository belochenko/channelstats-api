from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATA_FILE: str = "data/service_data.parquet"

settings = Settings()
