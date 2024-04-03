!#/bin/python3
import requests
from github import Github
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_csv(url):
    # Use streaming download to efficiently handle large files
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        return response.content

def upload_to_github(repo_name, file_name, file_content, github_token):
    try:
        g = Github(github_token)
        user = g.get_user()
        repo = user.get_repo(repo_name)
        
        # Check if the file exists
        existing_file = repo.get_contents(file_name)
        
        # Update the file
        repo.update_file(existing_file.path, f"Updating {file_name}", file_content, existing_file.sha)
        logger.info(f"File '{file_name}' updated in '{repo_name}' repository.")
    except Exception as e:
        # File does not exist, create a new one
        repo.create_file(file_name, f"Adding {file_name}", file_content)
        logger.info(f"File '{file_name}' uploaded to '{repo_name}' repository.")

if __name__ == "__main__":
    csv_url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
    github_repo = "YourGitHubUsername/YourRepository"
    github_token = "YourGitHubToken"
    file_name = "ipblocklist.csv"
    
    try:
        logger.info("Downloading CSV file...")
        csv_content = download_csv(csv_url)
        logger.info("Uploading CSV file to GitHub...")
        upload_to_github(github_repo, file_name, csv_content, github_token)
        logger.info("Process completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
