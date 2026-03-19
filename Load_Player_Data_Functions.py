import io
import os
import json
from typing import Any, Optional

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

load_dotenv()

AZURE_TENANT_ID = os.getenv("YOUR_AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("YOUR_AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("YOUR_AZURE_CLIENT_SECRET")
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("YOUR_STORAGE_ACCOUNT_NAME")
AZURE_CONTAINER_NAME = "tennis-data"
AZURE_PATH_PREFIX = os.getenv("AZURE_PATH_PREFIX", "").strip()
if AZURE_PATH_PREFIX and not AZURE_PATH_PREFIX.endswith("/"):
    AZURE_PATH_PREFIX = AZURE_PATH_PREFIX.rstrip("/") + "/"


def get_blob_service_client() -> BlobServiceClient:
    credential = ClientSecretCredential(
        tenant_id=AZURE_TENANT_ID,
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET,
    )
    account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    return BlobServiceClient(account_url=account_url, credential=credential)


def _blob_path(rel_path: str) -> str:
    return f"{AZURE_PATH_PREFIX}{rel_path}"


def read_parquet_from_blob(rel_path: str) -> pd.DataFrame:
    svc = get_blob_service_client()
    blob = svc.get_container_client(AZURE_CONTAINER_NAME).get_blob_client(_blob_path(rel_path))
    data = blob.download_blob().readall()
    return pd.read_parquet(io.BytesIO(data))


def read_csv_from_blob(rel_path: str, **kwargs) -> pd.DataFrame:
    svc = get_blob_service_client()
    blob = svc.get_container_client(AZURE_CONTAINER_NAME).get_blob_client(_blob_path(rel_path))
    data = blob.download_blob().readall()

    # Rankings CSVs are uploaded as UTF-8.
    kwargs.setdefault("encoding", "utf-8")
    kwargs.setdefault("low_memory", False)
    return pd.read_csv(io.BytesIO(data), **kwargs)


def read_json_from_blob():
    """
    Download `Outputs/player_info.json` from Azure Blob Storage, parse it,
    save it to the project root, and return (parsed_json, last_modified_date).
    """
    blob_name = "Outputs/player_info.json"
    save_to = "player_info.json"  # saved into the project root folder
    encoding = "utf-8"

    try:
        blob_client = get_blob_service_client().get_blob_client(
            container=AZURE_CONTAINER_NAME, blob=blob_name
        )

        raw_bytes = blob_client.download_blob().readall()
        player_data_matches = json.loads(raw_bytes.decode(encoding))

        blob_properties = blob_client.get_blob_properties()
        last_modified_date = blob_properties["last_modified"].strftime("%Y-%m-%d %H:%M:%S")

        # Project root is the directory containing this file (TennisBlog2/).
        project_root = os.path.abspath(os.path.dirname(__file__))
        abs_save_to = os.path.join(project_root, save_to)

        with open(abs_save_to, "w", encoding="utf-8") as f:
            json.dump(player_data_matches, f, ensure_ascii=False, indent=2)

        return player_data_matches, last_modified_date
    except Exception as e:
        print(f"Error loading player_data_matches: {e}")
        return None, None



if __name__ == "__main__":
    read_json_from_blob()