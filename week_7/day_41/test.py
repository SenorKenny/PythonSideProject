import requests
import argparse
from config import key, sites ,levels
import logging
import time
import random
import os

def thisrequest(url,total_runs,parameters=None,header=None):
    logger.info("starting request")
    
    while True:
        try: 
            start=time.perf_counter()
            response=requests.get(url,params=parameters,headers=header)
            end=time.perf_counter()
            latency=end-start
            status_number=response.status_code
            logging.debug(f'status code for this request is {status_number}')
            response.raise_for_status()
            logger.info("connection succeesful.")
            total_runs["latency"].append(latency)
            total_runs["200"]+=1
            return response,total_runs
        except requests.HTTPError as e:
            if status_number in (401,403,404):
                discnotify(f'bot crashed, error code {status_number}')
                telenotify(f'bot crashed, error code {status_number}')
                logger.error(e)
                total_runs["hard"]+=1
                e.total_runs=total_runs
                raise 
            
            elif status_number in (429,503):
                try:
                    total_runs["medium"]+=1
                    stime=sleeptime("medium",total_runs)
                    time.sleep(stime)
                    
                except RuntimeError as e:
                    
                    discnotify(f'bot crashed, error code {status_number}')
                    telenotify(f'bot crashed, error code {status_number}')
                    logger.error(e)
                    e.total_runs=total_runs
                    raise 
            else:
                raise 
                    
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            try:
                total_runs["soft"]+=1
                stime=sleeptime("soft",total_runs)
                time.sleep(stime)
            except RuntimeError as e:
                discnotify(f'bot crashed, Timeout/Connection Error')
                telenotify(f'bot crashed, Timeout/Connection Error')
                
                logger.error(e)
                e.total_runs=total_runs
                raise 
        except Exception as e:
            logger.error(f'not sure: {e}')
            e.total_runs=total_runs
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
def sleeptime(code,key):
    stime=2.0

    if code == "soft":
        if key[code]<15:
             logger.info(f"Soft retry attempt {key[code]}")
             return stime+random.randint(0,20)/20
        else:
            raise RuntimeError("Max soft attempts reached, aborting")
    if code == "medium":
        if key[code]<5:
            logger.info(f"Medium retry attempt {key[code]} ")
            return stime*key[code]+random.randint(0,20)/20
        else:
             raise RuntimeError("Max medium attempts reached, aborting")
def info_parser(response,total_runs):
    price_data={
        "price":None,
        "change":None,
    }
    if response:
        response=response.json()
    else:
        return price_data
    try:
        current=float(response["c"])
        if current > 0:
            price_data["price"]=current
            total_runs["success"]+=1
        else:
            total_runs["data_error"]+=1
            return price_data
    except (ValueError,TypeError,KeyError) as e:
        print('Price could not be parsed')
        total_runs["data_error"]+=1
        return price_data
    try:
            price_data["change"]=float(response["dp"])
            
    except (ValueError,TypeError,KeyError):
            print('Change could not be parsed')
    return price_data
    
       
    
    return price_data
parser=argparse.ArgumentParser(description="Scraper for a full site. Full Demo")
parser.add_argument('--url',
                    type=str,
                    required=True,
                    choices=(sites.keys()),
                    help=f"Target url we wish to scrape, avaialable list of sites are {list(sites)}")
parser.add_argument('--dry',
                    action='store_true',
                    help="To do testing asid from main script")
parser.add_argument('--level',
                    type=str,
                    choices=(levels.keys()),
                    default='i',
                    help=f"Set the desired level reader of your logger. Choices are {list(levels)}"  )
args=parser.parse_args()
logging.basicConfig(level=levels[args.level], 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                    )
logger=logging.getLogger(__name__)
url=sites[args.url]
def summary(stock,price_data,container):
    
    if price_data["price"]:
        if price_data["price"] > 0:
            container.append({stock:price_data})
            print(f'Current price for {stock} is {price_data["price"]}')
            print(f'Price has change by {price_data["change"]}% since yesterday')
        else:
           print (f'Price data for {stock} could not be obtained') 
    else:
        print (f'Price data for {stock} could not be obtained')
def main():
    stocks=["AAPL", "NOTAREAL", "MSFT", "TSLA"]
    container=[]
    total_runs={"success":0,
                    "200":0,
                 "soft":0,
                 "medium":0,
                 "hard":0,
                 "latency":[],
                 "data_error":0}
    for company in stocks:
        if "finnhub" in url:
            try:
                parameters={"symbol": company}
                headers={"X-Finnhub-Token": key['FINN']}
                response,total_runs=thisrequest(url,total_runs,parameters=parameters,header=headers)
                logging.debug(f'info for {response.json()}')
                price_data=info_parser(response,total_runs)
                
                summary(company,price_data,container)
            except Exception as e:
                logging.error(f'Error or above: {e}')
                break
          
        else:
            response,errors=thisrequest(url)
            print(response)
            print(f'status code for {url} is {response.status_code}')

main()