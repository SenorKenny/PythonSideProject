

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError 
from pathlib import Path
import json
def login(page,username,password):
    try:
        page.goto("https://www.saucedemo.com/", timeout=5000)
        page.wait_for_selector("[data-test='login-button']")
        print(f'attempting to login with {username}:{password}')
        page.fill("[data-test='username']",username) #in future, havee it so it reads from a .env or .config
        page.fill("[data-test='password']",password)
        page.click("[data-test='login-button']")
        page.locator("div[data-test='inventory-item']").first.wait_for()
        
        print("we logged in")
    except PlaywrightTimeoutError as e:
        raise RuntimeError("Failed to login, retry")
def load(AllUsers):

    for user in AllUsers:
        filepath=user["filepath"]
        if Path(filepath).exists():
            try:
                print(f"Looking for {filepath} at {Path(filepath).resolve()}")
                with open (filepath,'r',encoding='utf-8') as file:
                    user["token"]=json.load(file)
            except json.JSONDecodeError as e:
                print(f"File corrupted, setting cookie to none: {e}")
        else:
            pass
   
        
def objcreator(browser,session=None):
        context=browser.new_context(storage_state=session)
        page=context.new_page()
        return context,page
def saver(filename,storagestate):
     with open(filename,'w',encoding='utf-8') as file:
          json.dump(storagestate,file)
def idk(user): #Hold this thought
    print(f"Building context and page for {user["username"]} ")
    user["context"],user["page"]=objcreator(browser,session=user["token"])

    if user["token"] is None:
        login(user["page"],user["username"],user["password"])
        print(f"Saving cookies for {user["username"]}")
        saver(user["filepath"],user["context"].storage_state()) 
        print(f"Cookies Saved")
    else:
        user["page"].goto("https://www.saucedemo.com/inventory.html")
        try:
            user["page"].locator("div[data-test='inventory-item']").first.wait_for()
        except PlaywrightTimeoutError as e:
            print("Could not verify inventory page. Session page missing and/or expired")
            print("closing context")
            user["context"].close() 
            print(f"Making new context/page for {user["username"]} ")
            user["context"],user["page"]=objcreator(browser)
            print("context made")
            login(user["page"],user["username"],user["password"])
            print(f"Saving cookies for {user["username"]}")
            saver(user["filepath"],user["context"].storage_state())
            print(f"Cookies Saved")
if __name__=='__main__':        
    LoginData=[("standard_user","secret_sauce"),("problem_user","secret_sauce"),("performance_glitch_user","secret_sauce")]
    ourinfo=[]
    required_files = ["standard_user.json", "problem_user.json", "performance_glitch_user.json"]

    for user, password in LoginData:
        newdict={"username":user,
                "password":password,
                "token":None,
                "page":None,
                "context":None,
                "filepath":user+".json"}  
        ourinfo.append(newdict)
    load(ourinfo)
    print(ourinfo)

    with sync_playwright() as proc:
        browser=proc.chromium.launch(headless=False)
        for user in ourinfo:
            idk(user)
            
# how to detect the tokens are expire
# Try to direct to inventory
#if we geet redirected to the login, expireed
#not all the users havee to necessarily bee expired.
#Perhaps adding a true and false to it? Or just directly sending it in the same loop could do the trick.
#The point is to get it all the contexts ready with fresh session? will be important for keeping all bots activ
#objective: Have all contextes, regardless if the sesh token is missing/stale, be ready for thee next action with an active check.
