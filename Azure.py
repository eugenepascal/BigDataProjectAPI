import os
from fastapi import FastAPI, File, UploadFile
from azure.storage.blob import BlobServiceClient, ContentSettings
import re

app = FastAPI()

# Set your Azure Storage Account connection string as an environment variable
# Replace <your_connection_string> with your actual connection string
os.environ['AZURE_STORAGE_CONNECTION_STRING'] = "DefaultEndpointsProtocol=https;AccountName=projetbigdata;AccountKey=xRU9prUEDrJe+/CgehnOezt1DWdL2bNRqwurYYZuNPPw3N2ugKLQRrKkKfRv1DN13ySkl04iBQGA+AStI/bnFA==;EndpointSuffix=core.windows.net"

# Replace <your_container_name> with your actual container name
CONTAINER_NAME = "projetbigdata"

def upload_to_azure_storage(file: UploadFile):
    sanitized_filename = sanitize_filename(file.filename)

    blob_service_client = BlobServiceClient.from_connection_string(os.environ['AZURE_STORAGE_CONNECTION_STRING'])
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    content_settings = ContentSettings(content_type=file.content_type)
    blob_client = container_client.get_blob_client(sanitized_filename)

    blob_client.upload_blob(file.file, content_settings=content_settings)

def sanitize_filename(filename: str) -> str:
    # Remove any invalid characters from the filename
    sanitized_filename = re.sub(r'[<>:"\\/|?*]', '', filename)

    # Truncate the filename if it exceeds the maximum allowed length
    max_length = 1024
    if len(sanitized_filename) > max_length:
        sanitized_filename = sanitized_filename[:max_length]

    return sanitized_filename
