"""
github_client.py - GitHub API Client

This file contains functions to interact with the GitHub API.
We use it to fetch Pull Request diffs (the code changes).
"""

import os
import requests
from app.utils import log_message


def get_github_token() -> str:
    """
    Get the GitHub Personal Access Token from environment variables.
    
    Returns:
        The GitHub token, or empty string if not found
    """
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        log_message("WARNING: GITHUB_TOKEN not found in environment variables")
    return token


def get_pull_request_diff(repo_full_name: str, pr_number: int) -> str:
    """
    Fetch the diff (code changes) for a Pull Request.
    
    The diff shows what lines were added (+) and removed (-) in the PR.
    
    Args:
        repo_full_name: The repository in "owner/repo" format (e.g., "octocat/hello-world")
        pr_number: The Pull Request number (e.g., 42)
    
    Returns:
        The diff as a string, or empty string if failed
    
    Example:
        diff = get_pull_request_diff("octocat/hello-world", 42)
    """
    log_message(f"Fetching diff for {repo_full_name} PR #{pr_number}")
    
    # Get our GitHub token
    token = get_github_token()
    
    # Build the API URL
    # GitHub API endpoint for getting a PR's diff
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
    
    # Set up the request headers
    headers = {
        # Request the diff format (not JSON)
        "Accept": "application/vnd.github.v3.diff",
        # User-Agent is required by GitHub API
        "User-Agent": "AI-Code-Review-Assistant"
    }
    
    # Add authorization if we have a token
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        # Make the API request
        log_message(f"Making request to: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Check if the request was successful
        if response.status_code == 200:
            log_message("Successfully fetched diff")
            return response.text
        
        # Handle common errors
        elif response.status_code == 401:
            log_message("ERROR: Unauthorized. Check your GITHUB_TOKEN.")
            return ""
        
        elif response.status_code == 404:
            log_message("ERROR: PR not found. Check the repo name and PR number.")
            return ""
        
        else:
            log_message(f"ERROR: GitHub API returned status {response.status_code}")
            log_message(f"Response: {response.text[:200]}")  # First 200 chars
            return ""
            
    except requests.exceptions.Timeout:
        log_message("ERROR: Request timed out")
        return ""
        
    except requests.exceptions.RequestException as e:
        log_message(f"ERROR: Request failed: {e}")
        return ""


def get_pull_request_files(repo_full_name: str, pr_number: int) -> list:
    """
    Get the list of files changed in a Pull Request.
    
    This is an alternative to getting the full diff.
    It returns information about each changed file.
    
    Args:
        repo_full_name: The repository in "owner/repo" format
        pr_number: The Pull Request number
    
    Returns:
        A list of file objects, each containing:
        - filename: The path to the file
        - status: 'added', 'removed', 'modified', etc.
        - additions: Number of lines added
        - deletions: Number of lines deleted
        - patch: The diff for this specific file
    """
    log_message(f"Fetching file list for {repo_full_name} PR #{pr_number}")
    
    token = get_github_token()
    
    # API endpoint for PR files
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Code-Review-Assistant"
    }
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            files = response.json()
            log_message(f"Found {len(files)} changed files")
            return files
        else:
            log_message(f"ERROR: Failed to fetch files: {response.status_code}")
            return []
            
    except Exception as e:
        log_message(f"ERROR: Failed to fetch files: {e}")
        return []
