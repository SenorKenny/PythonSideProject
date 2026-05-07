
import requests
import random
import time
import config
import logging

logger = logging.getLogger(__name__)


def  url_requester(url,Timeout_val=None,Param_val=None,header_val=None):
#We want to get response in json and status code. Configurable retry (from env) with sleep built in
    i=0
    try:
        retry=config.config["RETRY_ATTEMPTS"]
    except Exception as error:
        logger.exception(f"config value unabled to be retrieved. {error}")
        retry=3
    while i<retry:
        i+=1
        print(f"Attempt {i}")
        try:
            response=requests.get(url,timeout=Timeout_val,params=Param_val,headers=header_val)
            response.raise_for_status()
            logging.info("connection succesful")
            return response.json(),response.status_code
        except requests.exceptions.ConnectionError as error:
            logger.exception(f"Error: {error}")
        except requests.exceptions.ConnectTimeout as error:
            logger.exception(f"Connection timeout. Delay your requests {error}")
        except requests.exceptions.Timeout as error:
            logger.exception(f"Reader timeout. Server may be busy {error}")
        except requests.exceptions.HTTPError as error:
            logger.exception(f"HTTP error code: {error}")
            return None, response.status_code
        except Exception as othererror:
            logger.exception(f"Error is : {othererror}")
        logger.debug("retrying..")
        sleepfloat=float(random.randint(30,50)/10)
        logger.debug(f"retrying in {sleepfloat}")
        time.sleep(sleepfloat)
    return None,None