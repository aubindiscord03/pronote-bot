from playwright.sync_api import sync_playwright
import os

URL = os.getenv("PRONOTE_URL")
USERNAME = os.getenv("PRONOTE_USER")
PASSWORD = os.getenv("PRONOTE_PASS")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL)

    # attendre chargement
    page.wait_for_timeout(3000)

    # remplir identifiant
    page.fill('input[type="text"]', USERNAME)

    # remplir mot de passe
    page.fill('input[type="password"]', PASSWORD)

    # cliquer sur connexion
    page.click('button')

    page.wait_for_timeout(5000)

    print("Connecté à PRONOTE")

    browser.close()
