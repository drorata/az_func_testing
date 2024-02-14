from datetime import datetime

import azure.functions as func
import loguru
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    foo_bar: str


settings = Settings()

app = func.FunctionApp()


@app.schedule(
    schedule="*/30 * * * * *",
    arg_name="myTimer",
    run_on_startup=True,
    use_monitor=False,
)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    logger.info(f"Loguru version is {loguru.__version__}")
    logger.info(f"The value of FOO_BAR is: {settings.foo_bar}")

    if myTimer.past_due:
        logger.info("The timer is past due!")

    logger.info("Great stuff!")
    logger.info(f"Python timer trigger function executed at {datetime.now()}")
