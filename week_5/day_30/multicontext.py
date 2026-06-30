

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError 
import playwright


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
    
def objcreator(browser):
        context=browser.new_context()
        page=context.new_page()
        return context,page
with sync_playwright() as proc:
    browser=proc.chromium.launch(headless=False)
    context1,page1=objcreator(browser)
    context2,page2=objcreator(browser)
    context3,page3=objcreator(browser)


    login(page1,"standard_user","secret_sauce")
    print(context1.storage_state())
    login(page2,"problem_user","secret_sauce")
    print(context2.storage_state())
    login(page3,"performance_glitch_user","secret_sauce")
    print(context3.storage_state())
    page1.pause()
  