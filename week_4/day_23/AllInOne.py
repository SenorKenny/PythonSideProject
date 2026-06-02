import requests
from bs4 import BeautifulSoup
import logging
import re
import datetime
logging.basicConfig(filename="day_23.log",level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger=logging.getLogger(__name__)
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
def item_grabber(info,category,failed_links):
    grab_success=False

    url=extractor(info,"a[href]","href")
    if not check(url,"url",True):
        return grab_success,None
    name=extractor(info,"a[href]","title",)
    if not check(name,"name",True):
        failed_links.append(url)
        return grab_success,None
    price=extractor(info,"[itemprop='price']")
    currency,price=price_formatter(price)
    if not check(price,"price",True):
        failed_links.append(url)
        return grab_success,None

    grab_success=True
    rating=extractor(info,"p[data-rating]","data-rating")
    check(rating,"rating")
    descrip=extractor(info,"p.description.card-text")
    check(descrip,"description")
    

    schema={"name":name,
        "price":price,
        "currency":currency,
        "sub_category":category,
        "rating":rating,
        "url":url,
        "first_seen":datetime.datetime.now().isoformat(),
        "last_seen":datetime.datetime.now().isoformat(),
        "prod_desc":descrip}
    return grab_success,schema
def scraper(data, extension):
    attempts=0
    success=0
    failed=0
    our_list=[]
    failed_links=[]
    category=data.select_one("a.active span").text
    sub_category=data.select_one(f"a[href='{extension}'] span").text
    try:
        prod_container=data.select("div [itemtype='https://schema.org/Product']")
        if prod_container is None:
            raise AttributeError
    except:
        logger.critical(f"Not recieving product list. Breaking.")
        return None,None
    for products in prod_container:
        attempts+=1
        
        grab_success,schema=item_grabber(products,"test",failed_links)
        if grab_success:
            success+=1
            schema["main_category"]=category
            schema["sub_category"]=sub_category
            our_list.append(schema)
        else:
            failed+=1
    logger.info(f'Attempted to scrape {attempts} items.')
    logger.info(f'{failed} failed, {success} succeded')
    return our_list,failed_links
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
def audit(combined_lists,combined_fails):
    total_products=len(combined_lists)
    total_fails=len(combined_fails)
    abnormal_name=0
    abnormal_price=0
    no_rating=0
    no_price=0
    category_count={}
    
    for product in combined_lists:
        if product["price"] is None:
            no_price+=1
        elif product["price"] >10000 or product["price"] <= 0:
            abnormal_price+=1
        if product["rating"] is None or product["rating"]>5 or product["rating"]<0 :
            no_rating+=1
        if product["name"] is None:
            abnormal_name+=1
        elif len(product["name"]) < 3:
            abnormal_name+=1
    combined_lists=[x for x in combined_lists if x.get("price") and x.get("price")>0]
    max_value=max(combined_lists, key= lambda prod:prod.get("price"))["price"]
    min_value=min(combined_lists, key= lambda prod:prod.get("price"))["price"]
    for product in combined_lists:
        if product["sub_category"]:
            if product["sub_category"] in category_count:
                category_count[product["sub_category"]]+=1
            else:
                category_count[product["sub_category"]]=1



    print(f'The number of products found was {total_products}')
    print(f'Unable to retrieve {total_fails} products')
    print(f'The highest product price was {max_value}')
    print(f'The lowest product price was {min_value}')
    print(f'The most popular category was {max(category_count, key=category_count.get)}')
    print(f'In this list, the number of products without a price is: {no_price} ')
    print(f'In this list, the number of products without a rating is: {no_rating} ')
    print(f'these number of products have odd names/descriptions: {abnormal_name}')
    print(f'Number of items with abnormal prices: {abnormal_price} ')


if __name__ == "__main__":
    combined_lists=[]
    combined_fails=[]
    search_list=["/test-sites/e-commerce/allinone/computers/laptops","/test-sites/e-commerce/allinone/computers/tablets","/test-sites/e-commerce/allinone/phones/touch"]
    for extension in search_list:
        url="https://webscraper.io"
        url=url+extension
        logger.info(f"attempting to request and parse {url}")
        response=request_url(url)
        converted=BeautifulSoup(response,'lxml')
        ourlist,ourfails=scraper(converted,extension)
        if ourlist:
            combined_lists.extend(ourlist)
        if ourfails:
            combined_fails.extend(ourfails)
    audit(combined_lists,combined_fails)
    
