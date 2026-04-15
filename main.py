from playwright.sync_api import sync_playwright
import os
import json
import requests

URL = os.getenv("PRONOTE_URL")
USERNAME = os.getenv("PRONOTE_USER")
PASSWORD = os.getenv("PRONOTE_PASS")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

FILE = "last.json"

def load_last():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return ""

def save_last(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def send(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

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

        page.wait_for_timeout(8000)  # ⬅️ on augmente

        print("Page chargée")

        page.fill('input[type="text"]', USERNAME)
        page.fill('input[type="password"]', PASSWORD)

        page.click('button:has-text("Se connecter")')

        page.wait_for_timeout(5000)

        print("Connexion effectuée")

        # récupérer haut de page
        content = page.locator("body").inner_text()
        short = content[:500]

        print("===== DEBUG =====")
        print(short)

        # trouver première ligne utile
        lines = short.split("\n")

        last_homework = ""
        for line in lines:
            if len(line.strip()) > 15:
                last_homework = line.strip()
                break

        print("Dernier devoir détecté :", last_homework)

        old = load_last()

        if last_homework != old:
            print("NOUVEAU DEVOIR")
            save_last(last_homework)
            send(f"Nouveau devoir : {last_homework}")
        else:
            print("Aucun nouveau devoir")

        browser.close()

if __name__ == "__main__":
    main()
