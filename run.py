#!/bin/python3
import os
import requests
from github import Github
import logging

import os
import requests
from github import Github

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

def upload_to_github(file_path, repo_name, github_token):
    github = Github(github_token)
    repo = github.get_repo(repo_name)
    filename = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        try:
            repo.create_file(filename, "Updated IP blocklist", content)
            print("File uploaded to GitHub successfully.")
        except Exception as e:
            print(f"Failed to upload file to GitHub: {e}")

def main():
    # File download settings
    url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
    download_dir = "/home/mraiham/abuse.ch"
    file_path = os.path.join(download_dir, "ipblocklist.csv")

    # GitHub settings
    repo_name = "wizard-projects/abuse.chC2Feeds"
    github_token = "*********"  # Make sure to replace this with your GitHub token

    # Create directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Download the file
    download_file(url, file_path)

    # Upload the file to GitHub
    upload_to_github(file_path, repo_name, github_token)

if __name__ == "__main__":
    main()
