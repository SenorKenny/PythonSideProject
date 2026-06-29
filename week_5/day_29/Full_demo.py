

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError 
import playwright


with sync_playwright() as proc:
    browser=proc.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    try:
        page.goto("https://www.saucedemo.com/")
        page.wait_for_selector("[data-test='login-button']")
        page.fill("[data-test='username']","standard_user") #in future, havee it so it reads from a .env or .config
        page.fill("[data-test='password']","secret_sauce")
        page.click("[data-test='login-button']")
        page.locator("div[data-test='inventory-item']").first.wait_for()
        print("we logged in")
    except PlaywrightTimeoutError as e:
        raise RuntimeError("Failed to login, retry")
    try:
        page.click("button[id='add-to-cart-sauce-labs-backpack']")
        page.locator("span[data-test='shopping-cart-badge']").wait_for()
        backpack_price=page.locator("div[data-test='inventory-item-price']").first.inner_text()
        if page.locator("span[data-test='shopping-cart-badge']").inner_text() == "1":
            print("Successfully Added to Cart")
        else:
            print(f' Cart value shows as {page.locator("span[data-test='shopping-cart-badge']").inner_text()} when we expected 1')
    except PlaywrightTimeoutError as e:
        raise RuntimeError(f"Could not add to cart. Error {e}")
    try:
        page.click("a[data-test='shopping-cart-link']")
        checkout=page.locator("button[data-test='checkoutXXX']")
        checkout.wait_for()
        if page.locator("div[data-test='item-quantity']").inner_text() != "1":
            raise RuntimeError("Value is expected to be one. Aborting.")
    except PlaywrightTimeoutError as e:
        raise RuntimeError(f"Failure with Cart page: {e}")
    # in future tests, wee do both quantity and name of item. This will be derived from schema.Today is simple
   
        #Would return nothing in real script, and skip to next item
    print("Item is there")
    try:
        checkout.click()
        continue_button=page.locator("input[data-test='continue']")
        continue_button.wait_for()
        print("in Checkout page")
    except PlaywrightTimeoutError as e:
        raise RuntimeError (f"Could not load checkout page: {e}")
    try:
        page.locator("input[data-test='firstName']").fill("Edward")
        page.locator("input[data-test='lastName']").fill("Elric")
        page.locator("input[data-test='postalCode']").fill("12345")
    except PlaywrightTimeoutError as e:
        raise RuntimeError(f'Could not fill out information.  {e}')
    print("Proceeding to overview")
    try:
        continue_button.click()
        finish_button=page.locator("button[data-test='finish']")
        finish_button.wait_for()
        
        
    except PlaywrightTimeoutError as e:
        raise RuntimeError(f'Could not load overview page. Exiting: {e}.')
    try:
        sub_total=page.locator("div[data-test='subtotal-label']").inner_text()
        sub_total=sub_total.replace("Item total: ","")
        if sub_total == backpack_price:
            finish_button.click()
            confirmation=page.locator("h2[data-test='complete-header']")
            if confirmation.inner_text() == "Thank you for your order!":
                print("Backpack successfully purchased")
            else:
                raise RuntimeError("Didn't see expected meessage")
        else:
            raise RuntimeError("Configured set price does not match final price. Aborting")

    except PlaywrightTimeoutError as e:
            print(f"Could not load the confirmation page {e}")