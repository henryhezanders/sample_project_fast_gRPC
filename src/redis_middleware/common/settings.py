from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    grpc_host: str = "localhost"
    grpc_port: int = 50051

    class Config:
        env_prefix = "APP_"  # prefixes all environment variables with "APP_"

settings = Settings()