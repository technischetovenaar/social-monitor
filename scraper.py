from datetime import datetime, timezone
import json
from pathlib import Path
import requests
import os

# Importeer de scraper functionaliteiten
from platforms.tiktok import scrape_tiktok
from platforms.google import scrape_google
from platforms.instagram import scrape_instagram

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def run_scraper():
    config = load_config()
    accounts = config.get("accounts", {})
    
    social_data = {
        "status": "success",
        "updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "platforms": {}
    }
    
    for platform, usernames in accounts.items():
        print(f"Scrapen starten voor platform: {platform}")
        social_data["platforms"][platform] = {}
        
        for username in usernames:
            print(f"  Gegevens ophalen voor: {username}")
            
            if platform == "tiktok":
                data = scrape_tiktok(username)
                if data:
                    social_data["platforms"][platform][username] = data
                else:
                    social_data["platforms"][platform][username] = {"error": "Scrape mislukt"}
            
            elif platform == "google":
                data = scrape_google(username)
                if data:
                    social_data["platforms"][platform][username] = data
                else:
                    social_data["platforms"][platform][username] = {"error": "Scrape mislukt"}
                    
            elif platform == "instagram":
                data = scrape_instagram(username)
                if data:
                    social_data["platforms"][platform][username] = data
                else:
                    social_data["platforms"][platform][username] = {"error": "Scrape mislukt"}
            
            else:
                social_data["platforms"][platform][username] = {
                    "followers": 0,
                    "note": f"Scraper voor {platform} nog niet actief"
                }

    # Opslaan in de lokale data-map
    Path("data").mkdir(exist_ok=True)
    with open("data/output.json", "w") as f:
        json.dump(social_data, f, indent=4)
    print("Lokale output gegenereerd.")

    # Webhook versturen naar Home Assistant
    ha_webhook_url = os.environ.get("HA_WEBHOOK_URL")
    if ha_webhook_url:
        try:
            response = requests.post(ha_webhook_url, json=social_data)
            print(f"Webhook verstuurd naar Home Assistant. Status: {response.status_code}")
        except Exception as e:
            print(f"Fout bij het versturen of webhook: {e}")
    else:
        print("Geen HA_WEBHOOK_URL gevonden in de instellingen. Webhook overgeslagen.")

if __name__ == "__main__":
    run_scraper()