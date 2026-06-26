from playwright.sync_api import sync_playwright
import json
from pathlib import Path
## test---


"""with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth_state.json")
    page = context.new_page()
    page.goto("https://quotes.toscrape.com/")
    page.pause()
    context.storage_state(path="auth_state.json")"""

###### 
"""with open("auth_state.json",'r') as file:
    cookie_info=json.load(file)
ourinfo=cookie_info['cookies']

for x,y in ourinfo[0].items():
    print(f'{x} : {y}')
"""

def verifier():
    if Path("auth_state.json").is_file():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state="auth_state.json")
            page = context.new_page()
            page.goto("https://quotes.toscrape.com/",
            logged_in=page.get_by_role("link",name="Logout")
            if logged_in.count() >0:
                print("You're logged in succesfully")
            else:
                print("Please log in manually")
    else:
        print("Please log in manually")

verifier()