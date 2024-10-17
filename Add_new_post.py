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

def add_post_to_json(new_post):
    
    blob_name = 'postsdata/posts.json'  # The name of the JSON file in blob storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        # Download the current JSON file content
        download_stream = blob_client.download_blob()
        json_content = json.loads(download_stream.readall().decode('utf-8'))
        
        # Add new item to the JSON content
        json_content.insert(0, new_post)
        
        # Convert the updated JSON content back to a string
        updated_json = json.dumps(json_content)
        
        # Upload the updated JSON file back to Blob storage
        blob_client.upload_blob(updated_json, overwrite=True)
        
        return {'message': 'Item added successfully', 'new_item': new_post}
    
    except Exception as e:
        return {'error': str(e)}