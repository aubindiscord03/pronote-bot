import os

URL = os.getenv("PRONOTE_URL")
USERNAME = os.getenv("PRONOTE_USER")
PASSWORD = os.getenv("PRONOTE_PASS")

print("===== DEBUG SECRETS =====")

print("URL:", URL if URL else "❌ NON DEFINI")
print("USERNAME:", USERNAME if USERNAME else "❌ NON DEFINI")
print("PASSWORD:", "✅ DEFINI" if PASSWORD else "❌ NON DEFINI")

print("=========================")
