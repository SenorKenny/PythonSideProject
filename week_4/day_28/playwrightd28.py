from playwright.sync_api import sync_playwright

"""
with sync_playwright() as sesh:
    browser=sesh.chromium.launch(headless=False)
    context=browser.new_context()
    page=browser.new_page()
    page.goto("https://quotes.toscrape.com/js/")
    page.locator("div.quote").first.wait_for()
    total_quotes=page.locator("div.quote")
    fake=page.get_by_text("bogusbogusbogusss")
    text=fake.inner_text()
    print(fake.count())
"""
"""
with sync_playwright() as sesh:
    browser=sesh.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.goto("https://quotes.toscrape.com/js/")

    try:
        page.click("p a[href='/login']")
        page.fill("input[id='username']","jojojo")
        page.fill("input[id='password']","testing123")
        page.click("input.btn")
        page.wait_for_url("https://quotes.toscrape.com/")
        print("true, we waited. Logged in")
    except:
        print("error testing.")"""
with sync_playwright() as sesh:
    browser=sesh.chromium.launch(headless=False)
    context=browser.new_context()
    page=browser.new_page()
    page.goto("https://quotes.toscrape.com/js/")
    page.wait_for_function("document.querySelectorAll('div.quote').length >= 10")
    total_quotes=page.locator("div.quote")
    for x in total_quotes.all():
        print(x.inner_text())