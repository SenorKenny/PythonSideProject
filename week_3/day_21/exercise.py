from bs4 import BeautifulSoup
import requests
import logging
logging.basicConfig(filename="day_21.log",level=logging.DEBUG)
thislogging=logging.getLogger(__name__)

def scrape():
    raw=requests.get("https://books.toscrape.com").text
    test=BeautifulSoup(raw,'lxml')
    list=[]
    for book in test.find_all('article',class_='product_pod'):
        try:
            name=book.h3.a["title"]
        except Exception as error:
            thislogging.debug("could not get title")
            name=None
        try:
            price= book.find('p',class_="price_color").get_text(strip=True)
            price=price.strip('Â')
            
        except Exception as error:
            thislogging.debug("no price could be found")
            price=None
        try:
            rating=book.find('p',class_="star-rating")["class"][1]
    
        except:
            thislogging.debug("no rating could be found")
            rating=None
        book_schema={"name":name,
                     "price":price,
                     "rating":rating}
        list.append(book_schema)
    return list
site_list=scrape()

print(site_list)


