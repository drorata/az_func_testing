from datetime import datetime

import azure.functions as func
import loguru
from utils import foo
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    foo_bar: str

    @field_validator("foo_bar")
    @classmethod
    def vault_must_be_accessible(cls, v: str) -> str:
        if v.startswith("@Microsoft.KeyVault(SecretUri="):
            err_msg = "Seems like FOO_BAR cannot be read from the key vault"
            logger.error(err_msg)
            # TODO: Figure out where this error is logged
            raise ValueError(err_msg)
        return v


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
    logger.info(f"The value of foo(1) is {foo(1)}")

    if myTimer.past_due:
        logger.info("The timer is past due!")

    logger.info("Great stuff!")
    logger.info(f"Python timer trigger function executed at {datetime.now()}")
