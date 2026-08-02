import logging
from scheduler import Scheduler
import datetime
import schedule
import requests
import random
import time
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)
def foo():
    print("hi")
def job():
    logger.info(f"Doing job at {datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')}, every 5 seconds")
    requests.get("https://httpbin.org/delay/2")
    return

"""
-----
schedule.every(datetime.timedelta(seconds=5).seconds).seconds.do(job)
try:
    while True:
        jitter=random.uniform(0,.50)
        schedule.run_pending()
        time.sleep(jitter)
except KeyboardInterrupt:
    logger.info(f"process stopping at {datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')} ")
-------
"""

"""
our_start=time.time()
i=1
try:
    while True:
        jitter=random.uniform(-.50,.50)
        next_run=our_start+i*5+jitter
        i+=1
        job()
        current=time.time()
        diff=next_run-current
        if diff > 0 :
            time.sleep(diff)
        else:
            logger.warning(f"Job overran its interval by {-diff:.2f}s")
except KeyboardInterrupt:
    logger.info(f"process stopping at {datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')} ")

    -------------------
    """
schedule=Scheduler()
schedule.cyclic(datetime.timedelta(seconds=5), foo)
try:
    while True:
        schedule.exec_jobs()
        
except KeyboardInterrupt:
    logger.info(f"process stopping at {datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')} ")
        