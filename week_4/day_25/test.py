from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup


## test---


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://quotes.toscrape.com/")
    page.pause()
    context.storage_state(path="auth_state.json")