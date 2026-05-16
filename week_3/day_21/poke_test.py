from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)  # headed so you can see what happens
    page = browser.new_page()
    page.goto("https://www.pokemoncenter.com/category/trading-card-game")
    page.wait_for_load_state("networkidle")
    content = page.content()
    print(content[:2000])
    browser.close()