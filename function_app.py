import logging
from datetime import datetime
import azure.functions as func

app = func.FunctionApp()


@app.schedule(
    schedule="*/30 * * * * *",
    arg_name="myTimer",
    run_on_startup=True,
    use_monitor=False,
)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Great stuff!")
    logging.info(f"Python timer trigger function executed at {datetime.now()}")
