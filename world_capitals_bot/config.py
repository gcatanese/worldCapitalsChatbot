import os
import logging


class DefaultConfig:
    PORT = int(os.environ.get("PORT", 3978))
    APP_ID = os.environ.get("MICROSOFT_APP_ID", "")
    APP_PASSWORD = os.environ.get("MICROSOFT_APP_PWD", "")

    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            level=DefaultConfig.LOG_LEVEL)
