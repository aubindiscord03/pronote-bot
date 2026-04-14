from pronotepy import Client
import requests
import json
import os

# CONFIG
URL = "https://2470002k.index-education.net/pronote/"
USERNAME = "aubin.gonzalez@mylfigp.org"
PASSWORD = "Katell1980!!"

TOKEN = "8749087089:AAE8hkO3HHx8nMyolwwd7YekeAZ_OU-jo48"
CHAT_ID = "6391025631"

DATA_FILE = "data.json"

def send(msg):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": msg})

def load_old():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def main():
    client = Client(URL, username=USERNAME, password=PASSWORD)

    homeworks = client.homework()
    new_list = [hw.description for hw in homeworks]

    old_list = load_old()

    for hw in new_list:
        if hw not in old_list:
            send(f"Nouveau devoir : {hw}")

    save(new_list)

if __name__ == "__main__":
    main()