import requests
from bs4 import BeautifulSoup
import logging
import re
import logging
logging.basicConfig(filename="day_23.log",level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger=logging.getLogger(__name__)

class webscraper_adapter:
    def __init__(self):
        self.urlpath=("a[href]", "href",True)
        self.namepath= ("a[href]", "title",True)
        self.pricepath=("[itemprop='price']", None,True)
        self.ratingpath= ("p[data-rating]", "data-rating",False)
        self.descriptionpath= ("p.description.card-text", None,False)
        self.catalog="div[itemtype='https://schema.org/Product']"
        self.website="https://webscraper.io"
        self.pagination=False

    def schema(self,card):
        ourschema={}
        keys={ "url":self.urlpath,
              "name":self.namepath,
              "price":self.pricepath,
              "rating":self.ratingpath,
              "description":self.descriptionpath}
        
        for ProdAttribute, (thispath, attribute,needed) in keys.items():
            thisvar=extractor(card,thispath,attribute)
            if not check(thisvar,ProdAttribute,needed):
                if needed:
    
                        return None,ourschema.get("url")
            ourschema[ProdAttribute]=thisvar
        currency, price = price_formatter(ourschema["price"])
        ourschema["price"] = price
        ourschema["currency"] = currency
        return ourschema,None
    def nextpage(self,data):
        return None
class book_adapter:
    def __init__(self):
        self.website="https://books.toscrape.com/catalogue/"
        self.urlpath=("h3 a","href",True)
        self.namepath=("img.thumbnail","alt",True)
        self.pricepath=("p.price_color", None, True)
        self.ratingpath=("p.star-rating","star-rating",None)
        self.catalog="article.product_pod"
    def schema(self,product):
        ourschema={}
        keys={ "url":self.urlpath,
              "name":self.namepath,
              "price":self.pricepath,
              "rating":self.ratingpath,
              }
        for ProdAttribute, (thispath, attribute,needed) in keys.items():
            thisvar=extractor(product,thispath,attribute)
            if not check(thisvar,ProdAttribute,needed):
                if needed:
    
                        return None,ourschema.get("url")
            ourschema[ProdAttribute]=thisvar
        currency, price = price_formatter(ourschema["price"])
        ourschema["price"] = price
        ourschema["currency"] = currency
        return ourschema,None
    def nextpage(self,data):
        next=data.select_one("li.next a")
        if next:
            next=next["href"]
            return self.website+next
       
def request_url(url,header=None,timeout=5):
    
    i=0
    if not url:
        print("No URL input detected")
        return None

    while i<5:
        i+=1
        try:
            response=requests.get(url,headers=header,timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as error:
            return None
        except requests.exceptions.ConnectionError:
            print("Issue connecting with server")
        except requests.exceptions.ConnectTimeout:
            print("Server response time exceeded set timeout")
        except requests.exceptions.InvalidURL:
            print("Invalid URL format")
        except Exception as error:
            print(f"Unknown error, error code:{error}")
def extractor(html,path,attribute=None):
    path=str(path)
    value=html.select_one(path)
    if value is None:
        logger.info(f"path {path} giving none-type. Check if path exist/correct spelling")
        return None
    if attribute:
        attribute=str(attribute)
        try:
            return value[attribute]
        except KeyError:
            logger.info(f"attribute:{attribute} giving none type. Check if key exist/correct spelling")
            return None
    else: 
        return value.get_text(strip=True)
def check(val,val_name="value",req= False):
    if not val:
        if req:
            logger.error(f'could not extract {val_name}, skipping item')
            return False
        else:
            logger.error(f'could not extract{val_name}')
            return False
    else:
        logger.debug(f'{val_name} was extracted: {val}')
        return True
def price_formatter(price):
    prod_currency=None
    currency_list=["aud","cad","$","€","£","¥","rmb","cny","chf","sek","nok","dkk","kr","r$","₹","₽","₩"]
    if not price:
        logger.debug("Cannot be parsed, no value")
        return None,None
    price=price.lower()
    if "," in price:
        price=price.replace(",","") #replaces , with nothing
    for currency in currency_list:
        if currency in price:
            prod_currency=currency
            price=price.replace(currency,"") #replaces currency with nothing
            break
    if "k" in price:
        price = float(re.sub(r'[^\d.]', '', price))
        price=price*1000
    
    try:
       price = float(price)
    except ValueError:
        logger.debug(f"Could not convert '{price}' to float")
        return None, None
    return prod_currency, price
def scraper(data,adapter,cat="none"):
    
    attempts=0
    success=0
    failed=0
    our_list=[]
    failed_links=[]
    category=cat #some category we proobably put as a parameter
    prod_container=data.select(adapter.catalog )
    if not prod_container:
        return None,None #
    for products in prod_container:
        attempts+=1
        schema,bad_url=adapter.schema(products)
        if schema:
            success+=1
            schema["category"]=category
            
            our_list.append(schema)
        else:
            failed+=1
            if bad_url:
                failed_links.append(bad_url)
    logger.info(f'Attempted to scrape {attempts} items.')
    logger.info(f'{failed} failed, {success} succeded')
    return our_list,failed_links
if __name__ == "__main__":
    our_config={(webscraper_adapter,"laptop","/test-sites/e-commerce/allinone/computers/laptops"),
                (webscraper_adapter,"tablets","/test-sites/e-commerce/allinone/computers/tablets"),
                (webscraper_adapter,"touch phones","/test-sites/e-commerce/allinone/phones/touch"),
                (book_adapter, None,"page-1.html")
    }
    
    for thisadapter, category, extension in our_config:
        
        testadapter=thisadapter()
        data_entries=[]
        failed_link=[]
        url=str(testadapter.website+extension)
        while url:
            response=request_url(url)
            if response:
                response=BeautifulSoup(response,'lxml')
            else:
                break
            our_list,our_fail=scraper(response,testadapter,category) 
            url=testadapter.nextpage(response)
            if our_list:
                data_entries.extend(our_list)
            if our_fail:
                failed_link.extend(our_fail)
        print(f"for {testadapter.website} the following products were scraped:")
        print("="*40)
        print("="*40)
        print(data_entries)
        print("="*40)
        
        print("The following are faild entries")
        print(failed_link)
        print("="*40)
      