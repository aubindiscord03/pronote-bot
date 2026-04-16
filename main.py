from playwright.sync_api import sync_playwright
import os

URL = os.getenv("PRONOTE_URL")
USERNAME = os.getenv("PRONOTE_USER")
PASSWORD = os.getenv("PRONOTE_PASS")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page = context.new_page()

        # anti-bot
        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """)

        print("Ouverture PRONOTE...")
        page.goto(URL)

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        print("Page chargée")

        # 🔍 vérifier si déjà connecté
        content = page.locator("body").inner_text()

        if "Espace Élèves" in content:
            print("Déjà connecté")

        else:
            print("Connexion requise")

            frame = None

            for f in page.frames:
                try:
                    if f.locator('input[type="text"]').count() > 0:
                        frame = f
                        break
                except:
                    pass

            if frame is None:
                raise Exception("Impossible de trouver le login")

            frame.fill('input[type="text"]', USERNAME)
            frame.fill('input[type="password"]', PASSWORD)
            frame.click('button:has-text("Se connecter")')

            page.wait_for_timeout(5000)

            print("Connexion effectuée")

        # 📄 récupérer contenu haut de page
        content = page.locator("body").inner_text()
        short = content[:500]

        print("===== DEBUG =====")
        print(short)

if __name__ == "__main__":
    main()
