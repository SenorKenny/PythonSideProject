from bs4 import BeautifulSoup
import requests
import logging
import time
import json
import datetime
import random
logging.basicConfig(filename="day_22.log",level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
thislogging=logging.getLogger(__name__)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

def scrape(our_progress):
    next_url=our_progress["next_url"]
    count=0
    default="https://books.toscrape.com/catalogue/page-1.html"
    if not next_url:
        thisurl=default
        number_of_books=0
    else:
        thisurl=next_url
        number_of_books=our_progress["book_count"]

    while thisurl :
        count+=1
        
        thispage=thisurl.replace("https://books.toscrape.com/catalogue/","")
        test=requester(thisurl)
        book_list={}

        try:
            thesebooks=test.find_all('article',class_='product_pod')
            if count == 28: #This is a test
                raise Exception("Simulated network failure")
            if not thesebooks:
                raise ValueError()
            
        except Exception as error:
            thislogging.error(f"HTML data could not be returned, Breaking Script: {error}")
            our_progress["pages_failed"].add(thispage)
            file_saver(book_list,our_progress)
            return
        thislogging.info(f"Attempting page {count}")
        book_list={}

        scrape_loop(thesebooks,book_list)
        if len(book_list) == 0:
            thislogging.warning(f"Page {thisurl} returned zero books — possibly blocked")
            # decide: skip, retry, or stop entirely
        elif len(book_list) < 5:
            thislogging.warning(f"Only {len(book_list)} books on page — investigate")
        number_of_books=number_of_books+len(book_list)
        thislogging.info(f"Page scraped, {len(book_list)} books found ")
        seconds=1
        thislogging.info(f"Waiting {seconds} seconds for next page")
        time.sleep(seconds)
        newpage=test.find('li',class_='next')
        our_progress["pages_scraped"].add(thispage)
        our_progress["book_count"]=number_of_books
        our_progress["time_stamp"]= str(datetime.datetime.now())
        if newpage:
            newpage=newpage.a['href']
            thisurl=f"https://books.toscrape.com/catalogue/{newpage}"
            our_progress["next_url"]=thisurl
        else:
            thisurl= None
            thislogging.info("No more pages")
            our_progress["next_url"]=thisurl
        
        file_saver(book_list,our_progress)
    thislogging.info(f"{len(our_progress["pages_scraped"])} pages scraped, {our_progress["book_count"]} books found.")
    return 
def file_loader():
    our_progress = {"book_count":0,
                    "next_url":None,
                    "pages_scraped":set(),
                    "pages_failed":set(),
                    "time_stamp":None}
    try:
        with open("progress.json") as f:
            our_progress=json.load(f)
            our_progress["pages_scraped"]=set(our_progress["pages_scraped"])
            our_progress["pages_failed"]=set(our_progress["pages_failed"])
            
    except FileNotFoundError:
        thislogging.info("No progress.json found. Will create")
    except json.JSONDecodeError:
        thislogging.error("progress.json corrupted.")
            
    return our_progress
def file_saver(book_list,our_progress):

    if book_list:
        pass
    else:
        logging.info("No pages to append")
        return
    try:
        with open ("books.json",'r') as file:
            TempList=json.load(file)
    except FileNotFoundError:
        thislogging.info(f"creating books.json")
        TempList={}
    except json.JSONDecodeError:
        thislogging.error(f"books.json corrupted. Creating new file")
        TempList={}
    with open ("books.json",'w') as file:
        TempList=book_list|TempList
        json.dump(TempList,file,indent=4)
    thislogging.info("books.json saved and updated")

    with open ("progress.json",'w') as file:
        json.dump(our_progress,file,indent=4, cls=SetEncoder)
    thislogging.info("progress.json saved and update")
def scrape_retry(our_progress):
    redos=our_progress["pages_failed"]
    if not redos:
        thislogging.info("No more pages")
        return
    
    for newpage in list(redos):
        thisurl=f"https://books.toscrape.com/catalogue/{newpage}"
        number_of_books=our_progress["book_count"]
        book_list={}
        test=requester(thisurl)
        try:
            thesebooks=test.find_all('article',class_='product_pod')
            if not thesebooks:
                
                raise ValueError()
            
        except:
            thislogging.error("HTML data could not be returned, Breaking Script")
            our_progress["pages_failed"].add(newpage)
            file_saver(book_list,our_progress)
            return
       
        number_on_page=len(thesebooks)
        number_of_books=number_of_books+number_on_page
        scrape_loop(thesebooks,book_list)
        if len(book_list) == 0:
            thislogging.warning(f"Page {thisurl} returned zero books — possibly blocked")
            # decide: skip, retry, or stop entirely
        elif len(book_list) < 5:
            thislogging.warning(f"Only {len(book_list)} books on page — investigate")
        our_progress["book_count"]=number_of_books
        our_progress["time_stamp"]= str(datetime.datetime.now())
        our_progress["pages_scraped"].add(newpage)
        our_progress["pages_scraped"]=sorted(our_progress["pages_scraped"])
        redos.discard(newpage)

        seconds=1
        thislogging.info(f"Waiting {seconds} seconds for next page")
        time.sleep(seconds)
        file_saver(book_list,our_progress)
    thislogging.info(f"{len(our_progress["pages_scraped"])} pages scraped, {number_of_books} books found.")   
def scrape_loop(thesebooks,book_list):
    for book in thesebooks:
            
            try:
                name=book.h3.a["title"]
                thislogging.debug(f"Book title {name} was extracted")
            except Exception as error:
                thislogging.error("could not get title")
                name=None
                continue
            try:
                price= book.find('p',class_="price_color").get_text(strip=True)
                price=price.strip('Â')
                thislogging.debug(f"price was extracted")
            except Exception as error:
                thislogging.error("no price could be found")
                price=None
            try:
                rating=book.find('p',class_="star-rating")["class"][1]
                thislogging.debug(f"Rating was extracted")
        
            except Exception as error:
                thislogging.info("no rating could be found")
                rating=None
            book_list[name]={"price":price,
                        "rating":rating}
    return     
def requester(url):
    test=[]
    NumOfRetries=0
    while NumOfRetries<5:
        NumOfRetries+=1
        try:
            raw=requests.get(url, timeout=3)#converts 1st page
            raw.raise_for_status()
            test=BeautifulSoup(raw.text,'lxml')
            return test
        except requests.exceptions.ConnectionError:
                thislogging.error("Connection error. Check URL")
        except requests.exceptions.ConnectTimeout:
                thislogging.error("Connection timeout. Delay your requests")
        except requests.exceptions.Timeout:
                thislogging.error("Reader timeout. Server may be busy ")
        except requests.exceptions.HTTPError as error:
                thislogging.error(f"HTTP error code: {error}")
                return None
        except Exception as othererror:
                thislogging.error(f"Error is : {othererror}")
        thislogging.info("request Attempt failed, retrying")
        sleepfloat=float(random.randint(30,50)/10)
        time.sleep(sleepfloat)
    return None
our_progress=file_loader() 
scrape(our_progress)
if our_progress["pages_failed"]:
    thislogging.info("Attempting to scrape failed pages")
    scrape_retry(our_progress)


min()