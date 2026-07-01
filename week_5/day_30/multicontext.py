

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError 
from pathlib import Path
import json
def login(page,username,password):
    try:
        page.goto("https://www.saucedemo.com/")
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
            with open (filepath,'r',encoding='utf-8') as file:
                user["token"]=json.load(file)
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
    
    user["context"],user["page"]=objcreator(browser,session=user["token"])

    if user["token"] is None:
        login(user["page"],user["username"],user["password"])
        saver(user["filepath"],user["context"].storage_state()) 
    
    else:
        user["page"].goto("https://www.saucedemo.com/inventory.html")
        try:
            user["page"].locator("div[data-test='inventory-item']").first.wait_for()
        except PlaywrightTimeoutError as e:
            print("Could not verify inventory page. Session page missing and/or expired")# a log instead in future, error
            login(user["page"],user["username"],user["password"])
            saver(user["filepath"],user["context"].storage_state())

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
            user["page"].pause()
# how to detect the tokens are expire
# Try to direct to inventory
#if we geet redirected to the login, expireed
#not all the users havee to necessarily bee expired.
#Perhaps adding a true and false to it? Or just directly sending it in the same loop could do the trick.
#The point is to get it all the contexts ready with fresh session? will be important for keeping all bots activ
#objective: Have all contextes, regardless if the sesh token is missing/stale, be ready for thee next action with an active check.
