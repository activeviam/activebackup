# -*- coding: utf-8 -*-
"""Final script.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1N2qseYYEnHjrXLHdNVokTj_1UnKXRpND
"""

import os
import json
import requests
import base64
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build

#scopes for Google Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

SERVICE_ACCOUNT_JSON = '{"type": "service_account", "project_id": "github-project-445314", "private_key_id": "4e50e71dd60ea90d2ca60ee316e3c5469a0453df", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDKT1ZDG272si3h\\nWnvxdPIizyc7guZZItMSsjLRjWJvXZrz7dKO8cIhDX8WF2J4RJwCar2e2O9/7zv9\\nzGKXVCYRSwrv/6sK3aDceznDR2md9y9ssflGDgidd+i/TVHavT6rTpk5E7r0roAz\\nvuBGL0eEPbqQYluBCw4L65bNcy9f3ZkEV18R1WrePEDGvsc+8FREVFq2cUHYujZv\\nUDJZ3U8/0bqqiCMbeQY6CW8Pt9qa+4cs5gW9K7iBzqFHVCIosznwvTc4/pn8igWB\\n57FZ8ne+TQRaBy8H2qfO31z2waW0rbu8uoyKCuGHy1TJ9pdMFBs6gdG4YmURvjyn\\n18eOmykrAgMBAAECggEAAx++gULHL+AIfVZcW5omswrn3C9lRzMWd09xIXNBdd7I\\nKcQeYD6zdLc0oy6xQpIspoznaLCI4jzbfEvPqe6Ot+2kuZgFGCHb/guZFL7hjqLm\\nhJMq+j31PBlB6tJS1UHe2d5Y11zKokSfji0AYZURUaVyYBBkwVVeXijBJ2MD9EL8\\ns4z+0A9EDao+M+Dluukf1+RWikHvm1XJGfh0qNzvgAG/EuiDmRzpyqjIublSl4nF\\nq7s6rbH+/w/HTSD7J6NIyntQMsADNaIKDFCIOfGXIyUSSVLSA7aFeOxGDUMKgimE\\nhIU1UE6fD89FkRJ6eNsHflk0pT0gOsPCWNSOH+xBwQKBgQDxR1bndYBYNDKyeglu\\n622yG8v9ZEc2Oze+44e9WF+O3B9nlBwAi/bDv6qyBCmgRE8a4xI/72Z1zUBIED3R\\n8VgrioESUPorW2Q2+Er+YqZRFYEAGL6Qmr0+T2VAcrivpAEko0r9lcErpPycvP6c\\nFVd9oAO2VfGQPmDlbsMud8WcGQKBgQDWp1LXeGQ44RvNgpCC32+5LIjC3KsXb5+z\\nTq17wVc1hsvagsugoZfJKcgglal32Bll1j9ujNdMjmpV8zilDkOs0HQhWUrEOJxG\\nWmn4KGs+wgpjxpGj20WWKQcE2sc/oFnzrLr72f7+H/DGITHFwPtDMxszDP8hwSdu\\nWLnLj6eX4wKBgBZMmpqPwInmYR0frEmFFsFUUlkb8HzxoihRTRVR2psQexKOnLvs\\nM6VJzJPhUJuQVKNOgzxHeve+PYergJsrrBNyHJW9yDFDpBJ0hjHWmjp6O07v+oTQ\\n2Fau7dO0Bp+tD7H8KY0gTxcii3pM+VchndFtfYpXjRjguwHZZ86eoTPZAoGBAMv8\\nZrVtK5ECG7HJChvUyg9nSvAjVFQJN/LmKecZbQ7o8oDNG0WjSuNYWV7d2xaQvlIQ\\nsGcWYOPX0yWq5YG1dIqd7j5i5LJkOd6BvYKepowVSlpXMcBNeGuiwZDTd9X3RIRU\\n+bytBa3qHJ2snegX5K+PuaFiEHK7ZAVxO98+vT2RAoGBAKkXa1UvfYHdL4/fDadK\\nj94dxYvnGQOGWEahNdYZQaCFRBeww44eiEYYZWIWDfVVOwnaRqki42255u0MFB2I\\nqbZoHfyYBSTNYydMMUhQ+Hwt5o7F1YDCKVQFckK3tQAm/K6rl7BjwsNggYKgFP2p\\n7Juk+/NQ9j4JXNtnWv7aY2vN\\n-----END PRIVATE KEY-----\\n", "client_email": "git-google-600@github-project-445314.iam.gserviceaccount.com", "client_id": "100131960802612611294", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/git-google-600%40github-project-445314.iam.gserviceaccount.com", "universe_domain": "googleapis.com"}'

# Convert the JSON string to a Python dictionary
service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
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
