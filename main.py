from playwright.sync_api import sync_playwright
import os

URL = os.getenv("PRONOTE_URL")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL)

    # screenshot pour debug
    page.screenshot(path="debug.png")

    print("Screenshot pris")

    browser.close()
    page.wait_for_timeout(5000)

    print("Connecté à PRONOTE")

    browser.close()
