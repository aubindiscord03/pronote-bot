from playwright.sync_api import sync_playwright
import os

URL = os.getenv("PRONOTE_URL")
USERNAME = os.getenv("PRONOTE_USER")
PASSWORD = os.getenv("PRONOTE_PASS")

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
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            locale="fr-FR"
        )

        page = context.new_page()

        # anti-bot léger
        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        print("Ouverture PRONOTE...")
        page.goto(URL, wait_until="domcontentloaded")

        print("Connexion...")

        # =========================
        # 🔍 DETECTION iframe OU NON
        # =========================
        page.wait_for_timeout(3000)

        if page.locator("iframe").count() > 0:
            print("Mode iframe détecté")
            frame = page.frame_locator("iframe").first
        else:
            print("Mode sans iframe")
            frame = page

        # =========================
        # 🔑 LOGIN
        # =========================
        frame.locator('input[type="text"]').wait_for(timeout=15000)

        frame.locator('input[type="text"]').fill(USERNAME)
        frame.locator('input[type="password"]').fill(PASSWORD)

        frame.locator('button').click()

        page.wait_for_load_state("networkidle")

        print("Connecté")

        # =========================
        # 📚 DEBUG DEVOIRS
        # =========================
        print("\n===== DEBUG DEVOIRS =====")

        try:
            bloc = page.locator("text=Travail à faire pour les prochains jours").locator("xpath=..")
            elements = bloc.locator("div")

            for i in range(elements.count()):
                try:
                    text = elements.nth(i).inner_text()

                    if len(text) < 200 and len(text) > 10:
                        print("----")
                        print(text)

                except:
                    pass
        except:
            print("Bloc devoirs introuvable")

        # =========================
        # 📊 DEBUG NOTES
        # =========================
        print("\n===== DEBUG NOTES =====")

        try:
            bloc_notes = page.locator("text=Dernières notes").locator("xpath=..")
            elements_notes = bloc_notes.locator("div")

            for i in range(elements_notes.count()):
                try:
                    text = elements_notes.nth(i).inner_text()

                    if len(text) < 150 and len(text) > 10:
                        print("----")
                        print(text)

                except:
                    pass
        except:
            print("Bloc notes introuvable")

        browser.close()


if __name__ == "__main__":
    main()
