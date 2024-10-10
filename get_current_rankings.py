import requests
import os
import json

def get_rankings():
    rankings_key = os.getenv("TENNIS_DATA_API_KEY")
    base_url = "https://tennis-live-data.p.rapidapi.com/rankings/"
    tour_code = "ATP"
    url = f"{base_url}{tour_code}"
    headers = {
        "x-rapidapi-key": rankings_key,
        "x-rapidapi-host": "tennis-live-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        rankings_data = response.json()
        
        # Save the response to a file
        with open("rankings.json", "w") as file:
            json.dump(rankings_data, file)
        
        return rankings_data
    else:
        print(f"Error: {response.status_code}")
        return None
get_rankings()