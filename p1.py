import requests
import os
import shutil

backup_folder = 'Repos'

if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

# List the contents of the backup folder to confirm access
print("Current files in GitHub backup folder before downloading:", os.listdir(backup_folder))


# Define GitHub API URL for repositories within the organization
org_name = 'activeviam'  # Organization name
url = f'https://api.github.com/orgs/activeviam/repos?per_page=100&page=1'  # Start with page 1


# Function to get the default branch of a repository
def get_default_branch(repo_name):
    repo_url = f'https://api.github.com/repos/{org_name}/{repo_name}'
    response = requests.get(repo_url)

    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get('default_branch', 'main')  # Return 'main' if no default branch is found
    else:
        print(f"Failed to get default branch for {repo_name}. Status code: {response.status_code}")
        return None

# Function to download the zip file for each repository
def download_repo_zip(repo_name):
    # Get the default branch name
    default_branch = get_default_branch(repo_name)

    if not default_branch:
        print(f"Skipping {repo_name} as no default branch was found.")
        return

    # Correct URL format for downloading ZIP from GitHub
    zip_url = f'https://github.com/{org_name}/{repo_name}/archive/refs/heads/{default_branch}.zip'
    zip_path = os.path.join(backup_folder, f"{repo_name}.zip")

    # Check if the zip file already exists and remove it if so
    if os.path.exists(zip_path):
        print(f"Zip file for {repo_name} already exists. Overwriting...")
        os.remove(zip_path)

    # Download the zip file from GitHub
    print(f"Downloading {repo_name} from {zip_url}...")
    response = requests.get(zip_url)

    if response.status_code == 200:
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved {repo_name} as {zip_path}")
    else:
        print(f"Failed to download {repo_name}. Status code: {response.status_code}, URL: {zip_url}")

# Function to fetch and download all repositories
def download_all_repos():
    page = 1  # Start with page 1

    while True:
        # Request for repositories via GitHub API
        response = requests.get(url.replace("page=1", f"page={page}"))

        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            repos = response.json()  # List of repositories on this page

            if not repos:  # If no repositories are left to download, break the loop
                print("All repositories have been downloaded.")
                break

            # Loop through each repository and download its ZIP file
            for repo in repos:
                repo_name = repo['name']
                try:
                    download_repo_zip(repo_name)
                except Exception as e:
                    print(f"Error downloading {repo_name}: {e}")

            page += 1  # Move to the next page of repositories
        else:
            print(f'Error fetching repositories: {response.status_code}')
            print(response.text)  # Print error message from GitHub
            break

# Start the downloading process
download_all_repos()

# Final check of the folder contents after all repositories have been downloaded
print("Final files in GitHub backup folder:", os.listdir(backup_folder))

