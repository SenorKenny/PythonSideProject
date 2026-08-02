import requests
import random
import logging
import time
import os
import json
import pathlib
from dotenv import load_dotenv
from scheduler import Scheduler
import datetime
import argparse
load_dotenv()


logging.basicConfig( level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)
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
    logger.info("starting request")
    counter={"success":0,
             "soft":0,
             "medium":0,
             "hard":0,
             }
    while True:
        try: 
            start=time.perf_counter()
            response=requests.get(url)
            end=time.perf_counter()
            latency=end-start
            status_number=response.status_code
            response.raise_for_status()
            logger.info("connection succeesful.")
            return response,latency,counter
        except requests.HTTPError as e:
            if status_number in (401,403,404):
                discnotify(f'bot crashed, error code {status_number}')
                telenotify(f'bot crashed, error code {status_number}')
                logger.error(e)
                counter["hard"]+=1
                e.counter=counter
                raise 
            
            elif status_number in (429,503):
                try:
                    counter["medium"]+=1
                    stime=sleeptime("medium",key)
                    time.sleep(stime)
                    
                except RuntimeError as e:
                    
                    discnotify(f'bot crashed, error code {status_number}')
                    telenotify(f'bot crashed, error code {status_number}')
                    logger.error(e)
                    e.counter=counter
                    raise 
            else:
                raise 
                    
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            try:
                counter["soft"]+=1
                stime=sleeptime("soft",key)
                time.sleep(stime)
            except RuntimeError as e:
                discnotify(f'bot crashed, Timeout/Connection Error')
                telenotify(f'bot crashed, Timeout/Connection Error')
                
                logger.error(e)
                e.counter=counter
                raise 
        except Exception as e:
            logger.error(f'not sure: {e}')
            e.counter=counter
            raise 
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
def encompasser(url,example,total_runs):
    try:
        global should_stop
        response,latency,counter=thisrequest(url,example)
        for x in counter.keys():
            total_runs[x]=total_runs[x]+counter[x]
        total_runs["latency"].append(latency)
    except Exception as e:
        logger.error(f"Hard failure, stopping: {e}")
        should_stop = True
        for x in e.counter.keys():
            total_runs[x]=total_runs[x]+e.counter[x]
        time_to_stop(total_runs)
def time_to_stop(total_runs):
    stop_time=datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')
    logger.info(f"process stopping at {stop_time} ")
    filename="data.json"
    all_runs=[]
    total_runs["stop_time"]=stop_time
    if pathlib.Path(filename).exists():
        try:
            with open(filename,'r',encoding='utf-8') as file:
                all_runs=json.load(file)
        except json.JSONDecodeError:
                logger.error("File is corrupted. Making new one")
    all_runs.append(total_runs)
    with open(filename,'w',encoding='utf-8') as file:
        json.dump(all_runs,file, indent=2)


parser=argparse.ArgumentParser(description="Makes a request to a URL repeatedly at a specified time interval")
parser.add_argument("--url",
                    type=str,
                    required=True,
                    help="The url we will be requesting")
parser.add_argument("--seconds",
                    type=float,
                    required=True,
                     choices=[0.0,5.0,10.0,15.0],
                     help="The amount of time between the first and second request."
                       )
parser.add_argument('-d','--dry-run',
                    action='store_true',
                    help= "Test for debugging state"
)
args=parser.parse_args()
filename="data.json"
total_runs={"success":0,
             "soft":0,
             "medium":0,
             "hard":0,
             "latency":[]
}

#then gives a specific amount of tries depending on whether its soft or medium
example={"soft":0,
         "medium":0}
myschedule=Scheduler()
should_stop=False

myschedule.cyclic(datetime.timedelta(seconds=args.seconds),encompasser, args=(args.url,example,total_runs))


while should_stop == False:
    try:
        myschedule.exec_jobs()
        time.sleep(1)
    except KeyboardInterrupt:
        time_to_stop(total_runs)
        break


