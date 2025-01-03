# -*- coding: utf-8 -*-
"""Final script.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1N2qseYYEnHjrXLHdNVokTj_1UnKXRpND
"""

import os
import requests
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build

#scopes for Google Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

service_account_file=os.environ['SERVICE_ACCOUNT_FILE']
print (type(service_account_file))
# Authenticate using the service account for Google Drive
credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

url = os.environ['URL'] 
token = os.environ['TOKEN']
username = os.environ['USERNAME'] 
org_name = os.environ['ORG_NAME'] 
# Build the Google Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

# Define the folder ID for the "Repos" folder in Google Drive

# Function to check if the folder exists
def ensure_folder_exists(folder_id):
    try:
        folder = drive_service.files().get(fileId=folder_id, fields="id, name").execute()
        print(f"Using folder: {folder['name']} (ID: {folder['id']})")
    except HttpError as error:
#        print(f"An error occurred: {error}")
#        print("Ensure the folder ID is correct and the service account has access.")
        exit()

# Function to upload a file to Google Drive
def upload_to_drive(file_path, file_name, folder_id):
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='application/zip')

    try:
        request = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id', supportsAllDrives=True)
        file = request.execute()
        print(f"Uploaded {file_name} with ID: {file['id']}")
        return file['id']
    except HttpError as error:
        print(f"An error occurred while uploading {file_name}: {error}")
        return None

headers = {'Authorization': f'token {token}'}

def get_default_branch(repo_name):
    repo_url = f'https://api.github.com/repos/{org_name}/{repo_name}'
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get('default_branch', 'main')
    else:
        print(f"Failed to get default branch for {repo_name}. Status code: {response.status_code}")
        return None

def download_repo_zip(repo_name):
    default_branch = get_default_branch(repo_name)
    if not default_branch:
        # print(f"Skipping {repo_name}. No default branch found.")
        return None

    zip_url = f'https://github.com/{org_name}/{repo_name}/archive/refs/heads/{default_branch}.zip'
    zip_path = f"/tmp/{repo_name}.zip"

    # print(f"Downloading {repo_name} from {zip_url}...")
    response = requests.get(zip_url, headers=headers)

    if response.status_code == 200:
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        # print(f"Saved {repo_name} to {zip_path}")
        return zip_path
    else:
        # print(f"Failed to download {repo_name}. Status code: {response.status_code}")
        return None

def download_all_repos(folder_id):
    page = 1
    repo_count = 0

    while True:
        response = requests.get(url.replace("page=1", f"page={page}"), headers=headers)

        if response.status_code == 200:
            repos = response.json()
            if not repos:
                print("No more repositories to download.")
                break

            for repo in repos:
                repo_name = repo['name']
                try:
                    zip_path = download_repo_zip(repo_name)
                    if zip_path:
                        upload_to_drive(zip_path, f"{repo_name}.zip", folder_id)
                        os.remove(zip_path)
                        repo_count += 1
                except Exception as e:
                    print(f"Error processing {repo_name}: {e}")

            page += 1
        else:
            print(f"Error fetching repositories: {response.status_code}")
            break

    return repo_count

# Main execution
ensure_folder_exists(FOLDER_ID)

repo_count = download_all_repos(FOLDER_ID)

print(f"\n--- Backup Complete ---")
print(f"Total Repositories Uploaded: {repo_count}")
print(f"Google Drive Folder Path: https://drive.google.com/drive/folders/{FOLDER_ID}")
