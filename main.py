print("Page chargée")

# 🔍 vérifier si déjà connecté
content = page.locator("body").inner_text()

if "Espace Élèves" in content:
    print("Déjà connecté")
else:
    print("Connexion requise")

    # chercher le bon frame
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

browser.close()

if __name__ == "__main__":
    main()
