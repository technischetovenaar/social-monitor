from datetime import datetime
import json
from pathlib import Path
import requests

# load settings 
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

# Function to make scrapers in 
def run_scraper():
    config = load_config()
    accounts = config.get("accounts", {})
    
    # collect data
    social_data = {
        "status": "success",
        "updated": datetime.utcnow().isoformat() + "Z",
        "platforms": {}
    }
    
    # Check Json platforms
    for platform, usernames in accounts.items():
        print(f"Scrapen starten voor platform: {platform}")
        social_data["platforms"][platform] = {}
        
        for username in usernames:
            print(f"  Gegevens ophalen voor: {username}")
            
            # TODO: building actual webhooks
            social_data["platforms"][platform][username] = {
                "followers": 1234,  # Testwaarde
                "posts": 42
            }

    # Saving local
    Path("data").mkdir(exist_ok=True)
    with open("data/output.json", "w") as f:
        json.dump(social_data, f, indent=4)
    print("Lokale output gegenereerd.")

    # Sending webhook to Home Assistant
    import os
    ha_webhook_url = os.environ.get("HA_WEBHOOK_URL")
    
    if ha_webhook_url:
        try:
            response = requests.post(ha_webhook_url, json=social_data)
            print(f"Webhook verstuurd naar Home Assistant. Status: {response.status_code}")
        except Exception as e:
            print(f"Fout bij het versturen van webhook: {e}")
    else:
        print("Geen HA_WEBHOOK_URL gevonden in de instellingen. Webhook overgeslagen.")

if __name__ == "__main__":
    run_scraper()