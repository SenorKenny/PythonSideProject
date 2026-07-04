from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
def parser(response):
      if response is None:
            print("Stopping script, no response found")
            return
      quoteslist=response["quotes"]
      for info in quoteslist:
            author=info["author"]["name"]
            text=info["text"]
            print(f'{author} once said {text}')

def resp_printer(response):
        #if "page=" in response.request.url:
                print(response)
                
def simpreq(url):
        try:
              response=requests.get()
              response.raise_for_status()
              return response.json()
        except TimeoutError:
              print("Could not recieve a response")
              return None
        except requests.exceptions.ConnectionError:
              print("could not establish connection with server")
              return None
        except requests.exceptions.HTTPError:
              print("404/not found")
              return None
        except Exception as e: 
              print(f"unknown : {e}")
              return None
def pgrouter(route):
       print(route)
       route.continue_()
       return
#exercise 1-3
"""with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.on('response',resp_printer)
    page.goto("https://quotes.toscrape.com/scroll")"""


#exercise 4
"""
i=0
hasnext=True
while  hasnext:
        i+=1
        url ="https://quotes.toscrape.com/api/quotes?page="
        url=url+str(i)
        response=simpreq(url)
        print(f'\n \n Here are the quotes for page {i} \n ')
        parser(response)
        hasnext=response["has_next"]
"""

#exercise 5
with sync_playwright() as pw:
       browser=pw.chromium.launch(headless=False)
       context=browser.new_context()
       page=context.new_page()
       page.route("**",pgrouter)
       page.goto("https://quotes.toscrape.com/scroll")
       page.pause()