import logging

def setup_logger():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    # Глушим излишнюю болтливость httpx (используется внутри PTB)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    return logging.getLogger("schedule_bot")

logger = setup_logger()