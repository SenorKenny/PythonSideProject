import requests
from bs4 import BeautifulSoup
import json
import time
import random
import logging
import re

thislogger=logging.basicConfig()
def requester(url,theheader=None,timeoutval=5):
    i=0
    while i<5:
        i+=1
        print(f"info- attempt {i}")
        try:
            response=requests.get(url,headers=theheader,timeout=timeoutval)
            response.raise_for_status()
            print("Success, returning data")
            return response.text
        except requests.exceptions.ConnectTimeout:
            print("Took too long to connect to server")
        except requests.exceptions.ConnectionError:
            print("Could not connect to server")
        except requests.exceptions.HTTPError:
            print("4XX /5XX error ,aborting")
            print(f"total loop attempts {i}")
            return 
        except Exception as error:
            print(f"Error found: {error}")
        sometime=random.randint(1,99)/100
        time.sleep(float(random.randint(1,3))+sometime)
def all_urls(data):
    if data is None:
        return None
    these_links=[]
    toextract=BeautifulSoup(data,'lxml')
    chapter_container=toextract.select_one("table[id='chapters']")
    all_chapters=chapter_container.select("td a[href][data-content]")
    for links in all_chapters:
        these_links.append(links["href"])
    return these_links
def parser(these_links):
    default="https://www.royalroad.com"
    
    try:
        for links in these_links:
            chapter=str(default+links)
            print(chapter)
            the_data=requester(chapter)
            soup=BeautifulSoup(the_data,'lxml')
            title=soup.select_one("meta[property='og:title']")["content"]
            clean_tit = re.sub(r'<[^>]+>', '', title)
            clean_tit = re.sub(r'[\\/*?:"|<>. ]', '_', clean_tit)
            clean_tit = re.sub(r'_+', '_', clean_tit).strip('_')
            content=soup.select('div.chapter-inner p')
            content=[p.text for p in content]
            if not content:
                print("nothing available in this link")
                pass
            content="\n\n".join(content)
                
            filename=clean_tit+".txt"
            savefile(content,filename)
            sometime=random.randint(1,99)/100
            time.sleep(float(random.randint(1,3))+sometime)
            
    except TypeError:
        print("One of the links was not a string")
def savefile(content,filename="unknown"):
    
    try:
        with open(filename,'w', encoding='utf-8') as file:
            file.write(content)
    except FileNotFoundError:
        print("something is seriously wrong.")

if __name__ == "__main__":
    response=requester("https://www.royalroad.com/fiction/21220/mother-of-learning")
    these_links=all_urls(response)
    print(these_links)
    parser(these_links)