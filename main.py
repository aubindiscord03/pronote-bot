from playwright.sync_api import sync_playwright
import os

# 🔐 Récupération des variables (GitHub Secrets)
URL = os.getenv("PRONOTE_URL")
USERNAME = os.getenv("PRONOTE_USERNAME")
PASSWORD = os.getenv("PRONOTE_PASSWORD")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        page = context.new_page()

        # 🔥 Anti-détection
        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """)

        print("Ouverture de PRONOTE...")
        page.goto(URL)

        # ⏳ laisse charger
        page.wait_for_timeout(5000)

        print("Page chargée")

        # 🔑 Remplissage login
        page.fill('input[type="text"]', USERNAME)
        page.fill('input[type="password"]', PASSWORD)

        print("Identifiants remplis")

        # 🔘 Bouton connexion
        page.click('button[type="submit"]')

        page.wait_for_timeout(5000)

        print("Connexion réussie (si pas bloqué)")

        browser.close()

if __name__ == "__main__":
    main()
