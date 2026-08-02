import requests
import random
import logging
import time
import os
from dotenv import load_dotenv
load_dotenv()
from scheduler import Scheduler
import datetime
import argparse
logging.basicConfig( level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)
def sleeptime(code,key):
    stime=2.0

    if code == "soft":
        if key[code]<15:
             key[code]+=1
             logger.info(f"Soft retry attempt {key[code]}")
             return stime+random.randint(0,20)/20
        else:
            raise RuntimeError("Max soft attempts reached, aborting")
    if code == "medium":
        if key[code]<5:
            key[code]+=1
            logger.info(f"Medium retry attempt {key[code]} ")
            return stime*key[code]+random.randint(0,20)/20
        else:
             raise RuntimeError("Max medium attempts reached, aborting")

def thisrequest(url,key):

    i=True
    while i:
        try: 
            response=requests.get(url)
            status_number=response.status_code
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            if status_number in (401,403,404):
                discnotify(f'bot crashed, error code {status_number}')
                telenotify(f'bot crashed, error code {status_number}')
                logging.error(e)
                i=False
                raise 
            
            elif status_number in (429,503):
                try:
                    stime=sleeptime("medium",key)
                    time.sleep(stime)
                except RuntimeError as e:
                    discnotify(f'bot crashed, error code {status_number}')
                    telenotify(f'bot crashed, error code {status_number}')
                    logging.error(e)
                    i=False
                    raise e
            else:
                raise e
                    
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            try:
                stime=sleeptime("soft",key)
                time.sleep(stime)
            except RuntimeError as e:
                discnotify(f'bot crashed, Timeout/Connection Error')
                telenotify(f'bot crashed, Timeout/Connection Error')
                logging.error(e)
                i=False
                raise e
        except Exception as e:
            logger.error(f'not sure: {e}')
            raise e
def discnotify(message):
    url=os.getenv("DISCURL")
    try:
        response=requests.post(url, json={"content": message })
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Could not send message through discord: {e}")
    except Exception as e:
        logger.error(f"Not sure what the issue is: {e}")
def telenotify(message):
    token=os.getenv("TELETOKEN")
    chatid=os.getenv("TELECHATID")
    if token is None:
        logger.error("No Telegram token posted.")
        return
    url=f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        response=requests.post(url=url,json={"chat_id": chatid, "text": message})
        response.raise_for_status()
    except requests.exceptions.RequestException:
        logger.error("Could not send notification to telegram")
    except Exception as e:
        logger.error(f"Invalid format: {e}")
def encompasser(url,example):
    try:
        global should_stop
        thisrequest(url,example)
    except Exception as e:
        logger.error(f"Hard failure, stopping: {e}")
        should_stop = True
parser=argparse.ArgumentParser(description="Makes a request to a URL repeatedly at a specified time interval")
parser.add_argument("url",
                    type=str,
                    help="The url we will be requesting")
parser.add_argument("seconds",
                    type=float,
                     choices=[0.0,5.0,10.0,15.0],
                     help="The amount of time between the first and second request."
                       )
parser.add_argument('-d','--dry-run',
                    action='store_true',
                    help= "Test for debugging state"
)
        
args=parser.parse_args()
#I want to see what code it is
#then gives a specific amount of tries depending on whether its soft or medium
example={"soft":0,
         "medium":0}
myschedule=Scheduler()
url="https://httpbin.org/status/404"
should_stop=False
myschedule.cyclic(datetime.timedelta(seconds=5),encompasser, args=(url,example))

while should_stop == False:
    try:
        myschedule.exec_jobs()
        time.sleep(1)
    except KeyboardInterrupt:
        logger.info(f"process stopping at {datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')} ")
        break
    