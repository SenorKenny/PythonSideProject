from bs4 import BeautifulSoup
import requests
import logging
import time
logging.basicConfig(filename="day_21.log",level=logging.DEBUG)
thislogging=logging.getLogger(__name__)

def scrape():
    
    list=[]
    for x in range(50):
        x+=1
        thisurl=f"https://books.toscrape.com/catalogue/page-{x}.html"
        i=0
        while i<5:
            i+=1
            try:

                raw=requests.get(thisurl).text
                i=5
            except Exception as e:
                logging.error(f"Could not obtain HTML data: {e}")
                logging.error("retrying ")
        
        test=BeautifulSoup(raw,'lxml')
        number=len(test.find_all('article',class_='product_pod'))
        for book in test.find_all('article',class_='product_pod'):
            
            try:
                name=book.h3.a["title"]
                thislogging.info(f"Book title {name} was extracted")
            except Exception as error:
                thislogging.debug("could not get title")
                name=None
            try:
                price= book.find('p',class_="price_color").get_text(strip=True)
                price=price.strip('Â')
                thislogging.info(f"price was extracted")
            except Exception as error:
                thislogging.debug("no price could be found")
                price=None
            try:
                rating=book.find('p',class_="star-rating")["class"][1]
                thislogging.info(f"Rating was extracted")
        
            except:
                thislogging.debug("no rating could be found")
                rating=None
            book_schema={"name":name,
                        "price":price,
                        "rating":rating}
            list.append(book_schema)
        thislogging.info(f"Page {x} scraped, {number} books found ")  
    thislogging.info(f"50 pages scraped, {len(list)} ")
    return list
site_list=scrape()



