import requests
import os
import json

def get_rankings():
    rankings_key = os.getenv("TENNIS_DATA_API_KEY_UPDATED")
    base_url = "https://tennisapi1.p.rapidapi.com/api/tennis/rankings/atp"
    url = f"{base_url}"
    headers = {
        "x-rapidapi-key": rankings_key,
        "x-rapidapi-host": "tennisapi1.p.rapidapi.com"
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

def get_WTArankings():
    rankings_key = os.getenv("TENNIS_DATA_API_KEY_UPDATED")
    base_url = "https://tennisapi1.p.rapidapi.com/api/tennis/rankings/wta"
    url = f"{base_url}"
    headers = {
        "x-rapidapi-key": rankings_key,
        "x-rapidapi-host": "tennisapi1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        rankings_data = response.json()
        
        # Save the response to a file
        with open("WTArankings.json", "w") as file:
            json.dump(rankings_data, file)
        
        return rankings_data
    else:
        print(f"Error: {response.status_code}")
        return None
get_WTArankings()
get_rankings()