import requests
import os
import json
from flask import Flask, render_template, request, jsonify
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.identity import ClientSecretCredential
import os
import json



# Your Azure details
tenant_id = os.getenv("YOUR_AZURE_TENANT_ID")
client_id = os.getenv("YOUR_AZURE_CLIENT_ID")
client_secret = os.getenv("YOUR_AZURE_CLIENT_SECRET")
storage_account_name = os.getenv("YOUR_STORAGE_ACCOUNT_NAME")
container_name = os.getenv("YOUR_CONTAINER_NAME")

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=credential
)


def get_rankings():
    rankings_key = os.getenv("TENNIS_DATA_API_KEY_UPDATED")
    base_url = "https://tennisapi1.p.rapidapi.com/api/tennis/rankings/atp"
    url = f"{base_url}"
    headers = {
        "x-rapidapi-key": rankings_key,
        "x-rapidapi-host": "tennisapi1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    
    blob_name = 'rankingsdata/rankings.json'  # The name of the JSON file in blob storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    if response.status_code == 200:
        rankings_data = response.json()
        
        # Save the response to a file
        rankings_data = json.dumps(rankings_data)
        blob_client.upload_blob(rankings_data, overwrite=True)
        
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

    blob_name = 'rankingsdata/WTArankings.json'  # The name of the JSON file in blob storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)    
    
    if response.status_code == 200:
        rankings_data = response.json()
          
        # Save the response to a file
        rankings_data = json.dumps(rankings_data)
        blob_client.upload_blob(rankings_data, overwrite=True)
        
        return rankings_data
    else:
        print(f"Error: {response.status_code}")
        return None
get_WTArankings()
get_rankings()