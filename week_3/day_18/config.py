

import os
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)

load_dotenv()
try:
    config={
        "url":os.getenv("API"),
        "MAX_BUYPRICE":float(os.getenv("MAX_BUY")),
        "MAX_WATCHPRICE":float(os.getenv("MAX_WATCH")),
        "MIN_BUYPRICE":float(os.getenv("MIN_BUY")),
        "MIN_WATCHPRICE":float(os.getenv("MIN_WATCH")),
        "CATEGORIES":{"1st":os.getenv("CATEGORY1").lower().strip(),
                    "2cd":os.getenv("CATEGORY2").lower().strip(),
                    "3rd":os.getenv("CATEGORY3").lower().strip(),},
        "RETRY_ATTEMPTS":int(os.getenv("MAX_RETRIES"))
    }
except:
    logger.exception("could not pull specific variables from config")
    