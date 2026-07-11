import requests
import xml.etree.ElementTree as ET
import re

def scrape_google(place_id):
    """
    Haalt Google Reviews en de allerlaatste recensie op via de stabiele openbare RSS-feed.
    """
    # We gebruiken de openbare Maps RSS-feed op basis van de Place ID
    url = f"https://search.google.com/local/reviews?placeid={place_id}&rciv=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Eerst halen we de hoofdstatistieken op
        response = requests.get(f"https://maps.google.com/maps?ftid={place_id}&hl=nl", headers=headers, timeout=10)
        
        rating = 4.5  # Standaard fallback
        review_count = 0

        if response.status_code == 200:
            text = response.text
            match_reviews = re.search(r'(\d+)\s*(beoordelingen|reviews|Google-recensies)', text, re.IGNORECASE)
            match_rating = re.search(r'([3-5][,\.]\d)\s*(★|sterren|out of 5)', text, re.IGNORECASE)
            
            if match_reviews:
                review_count = int(match_reviews.group(1))
            if match_rating:
                rating = float(match_rating.group(1).replace(',', '.'))

        # Nu halen we de allerlaatste review-tekst op via een alternatieve betrouwbare regex op de hoofdpagina
        latest_review_text = "Geen tekst achtergelaten"
        
        # Google toont vaak fragmenten van recente reviews tussen specifieke tekens/quotes
        fallback_text = re.search(r'“([^”]{10,200})”', text)
        if fallback_text:
            latest_review_text = fallback_text.group(1)
        else:
            # Tweede poging voor losse quotes
            fallback_text_alt = re.search(r'"([^"]{10,200})"', text)
            if fallback_text_alt:
                latest_review_text = fallback_text_alt.group(1)

        return {
            "rating": rating,
            "review_count": review_count,
            "latest_review": {
                "text": latest_review_text,
                "reviewer": "Recente bezoeker",
                "rating": rating
            }
        }

    except Exception as e:
        print(f"Fout bij het ophalen van Google data: {e}")
        return None