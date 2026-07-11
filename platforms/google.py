import requests
import re

def scrape_google(place_id_or_query):
    """
    Haalt Google Reviews op via een stabiele Google Maps embedded URL.
    Werkt zowel met een Place ID (aanbevolen) als met de gewone bedrijfsnaam.
    """
    # Als de input een Google Place ID is (begint meestal met ChI), gebruiken we de specifieke kaart-URL
    if place_id_or_query.startswith("ChI"):
        url = f"https://maps.google.com/maps?ftid={place_id_or_query}&hl=nl"
    else:
        # Fallback naar de zoekopdracht als er nog geen Place ID in config.json staat
        url = f"https://www.google.com/search?q={place_id_or_query}&hl=nl"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        text = response.text
        
        # Verbeterde regex die zoekt naar het aantal reviews en de score in de Google Maps data
        # Dit zoekt naar patronen zoals "4,8" of "4.8" gevolgd door het aantal reviews
        match_reviews = re.search(r'(\d+)\s*(beoordelingen|reviews|reviews|Google-recensies)', text, re.IGNORECASE)
        match_rating = re.search(r'([3-5][,\.]\d)\s*(★|sterren|out of 5)', text, re.IGNORECASE)
        
        # Brede fallback mocht de specifieke Maps-layout afwijken
        if not match_reviews:
            match_reviews = re.search(r'\(?(\d+)\s*(beoordelingen|reviews)\)?', text, re.IGNORECASE)
        if not match_rating:
            match_rating = re.search(r'([3-5][,\.]\d)', text)

        if match_reviews and match_rating:
            return {
                "rating": float(match_rating.group(1).replace(',', '.')),
                "review_count": int(match_reviews.group(1))
            }
            
        return None
    except Exception:
        return None