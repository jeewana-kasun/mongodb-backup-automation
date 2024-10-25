import os
import time
import hashlib
from azure.storage.blob import BlobServiceClient

# Create connection to Azure Blog Storage

#Connection string can be copied from AzureStorageAccount --> Security + Networking --> Access Keys
connection_string = "DefaultEndpointsProtocol=https;AccountName=<STORAGE-ACCOUNT-NAME>;AccountKey=<STORAGE-ACCOUNT-KEY>;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#Specific container name in the storage account
container_name = "<AZURE-STORAGE-BLOB-CONTAINER_NAME"

# The Path to directory contains the MongoDB Dump file
#Sample | folder_path = "/home/vmo/Desktop/azure-blob/test"
folder_path = "<PATH-TO-BACKUP-FOLDER>"

def get_file_hash(file_path):
    # Open file in Binary mode
    with open(file_path, 'rb') as f:
        # Read file content
        file_data = f.read()
        # get sha256 of file
        file_hash = hashlib.sha256(file_data).hexdigest()
    return file_hash

#Define function to Delete all files in a directory
def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

# Upload file to Storage with the file that contains the hash of them.
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    print(file_path)
    blob_client = blob_service_client.get_blob_client(container_name, file)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    # Search for file names starts with a particular phrase
    if file.startswith('<FILE-NAME-SUFFIX>*'):
        print("Uploading file ", file_path)
        file_hash = get_file_hash(file_path)
        txt_file_path = os.path.join(folder_path, f'{os.path.splitext(file)[0]}.txt')
        with open(txt_file_path, 'w') as f:
            f.write(file_hash)
        # Upload .txt file to Storage
        blob_client = blob_service_client.get_blob_client(container_name, f'{os.path.splitext(file)[0]}.txt')
        with open(txt_file_path, "rb") as data:
            blob_client.upload_blob(data)

# Calling Delete function to clear the folder location
delete_files_in_directory(folder_path)