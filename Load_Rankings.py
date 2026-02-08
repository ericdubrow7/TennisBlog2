import requests
import os
import json
from flask import Flask, render_template, request, jsonify
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.identity import ClientSecretCredential
import os
import json
from datetime import datetime
import os

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

def load_rankings():
    try:
        blob_name = 'rankingsdata/rankings.json'  # Path to the rankings file in the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Download the blob's content as a string
        download_stream = blob_client.download_blob()
        rankings_data = json.loads(download_stream.readall().decode('utf-8'))

        # Get the last modified date of the blob
        blob_properties = blob_client.get_blob_properties()
        last_modified_date = blob_properties['last_modified'].strftime('%Y-%m-%d %H:%M:%S')

        return rankings_data, last_modified_date
    except Exception as e:
        print(f"Error loading rankings: {e}")
        return None, None

def load_WTArankings():
    try:
        blob_name = 'rankingsdata/WTArankings.json'  # Path to the WTA rankings file in the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Download the blob's content as a string
        download_stream = blob_client.download_blob()
        WTArankings_data = json.loads(download_stream.readall().decode('utf-8'))

        # Get the last modified date of the blob
        blob_properties = blob_client.get_blob_properties()
        last_modified_date = blob_properties['last_modified'].strftime('%Y-%m-%d %H:%M:%S')

        return WTArankings_data, last_modified_date
    except Exception as e:
        print(f"Error loading WTA rankings: {e}")
        return None, None