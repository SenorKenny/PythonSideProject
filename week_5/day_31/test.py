from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # headed — you want to SEE it
    page = browser.new_page()
    page.goto("https://bot.sannysoft.com")
    page.wait_for_timeout(30000)                   # 30s to read the grid
    browser.close()