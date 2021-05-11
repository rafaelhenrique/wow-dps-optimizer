from prettyconf import config


class Settings:
    LOG_LEVEL = config("LOG_LEVEL", default="INFO")
    LOGGERS = config("LOGGERS", default="", cast=config.list)
    RAIDER_IO_URL = config("RAIDER_IO_URL")


settings = Settings()
