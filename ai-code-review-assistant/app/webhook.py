"""
webhook.py - GitHub Webhook Handler

This file handles incoming webhook events from GitHub.
When someone opens or updates a Pull Request, GitHub sends us a notification here.
"""

# Import required modules
import os
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import our custom modules
from app.github_client import get_pull_request_diff
from app.ai_reviewer import review_code
from app.utils import log_message

# Create a router for webhook endpoints
# This groups related endpoints together
router = APIRouter()


# Define a simple model for manual code review requests
class CodeReviewRequest(BaseModel):
    """
    Model for manual code review requests.
    Users can submit code directly for review without GitHub.
    """
    code: str  # The code to review


def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify that the webhook request actually came from GitHub.
    
    GitHub signs each webhook payload with a secret key.
    We verify this signature to ensure the request is authentic.
    
    Args:
        payload: The raw request body
        signature: The signature from GitHub (X-Hub-Signature-256 header)
        secret: Our webhook secret (must match what we set in GitHub)
    
    Returns:
        True if signature is valid, False otherwise
    """
    # If no secret is configured, skip verification (not recommended for production!)
    if not secret:
        log_message("WARNING: No webhook secret configured. Skipping verification.")
        return True
    
    # Calculate the expected signature
    expected_signature = "sha256=" + hmac.new(
        secret.encode(),      # Convert secret to bytes
        payload,              # The raw payload
        hashlib.sha256        # Use SHA-256 algorithm
    ).hexdigest()
    
    # Compare signatures securely (prevents timing attacks)
    return hmac.compare_digest(expected_signature, signature)


@router.post("/webhook")
async def handle_webhook(request: Request):
    """
    Handle incoming GitHub webhook events.
    
    This endpoint receives notifications when:
    - A Pull Request is opened
    - A Pull Request is updated (new commits pushed)
    - A Pull Request is synchronized
    
    We only process 'opened' and 'synchronize' actions.
    """
    log_message("Received webhook request")
    
    # Get the raw request body (needed for signature verification)
    payload = await request.body()
    
    # Get the signature from headers
    signature = request.headers.get("X-Hub-Signature-256", "")
    
    # Get our secret from environment variables
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    
    # Verify the signature
    if not verify_github_signature(payload, signature, secret):
        log_message("ERROR: Invalid webhook signature")
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse the JSON payload
    try:
        data = await request.json()
    except Exception as e:
        log_message(f"ERROR: Failed to parse JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Check if this is a Pull Request event
    if "pull_request" not in data:
        log_message("Not a pull request event, ignoring")
        return {"status": "ignored", "reason": "Not a pull request event"}
    
    # Get the action (opened, synchronize, closed, etc.)
    action = data.get("action", "")
    log_message(f"Pull request action: {action}")
    
    # Only process 'opened' and 'synchronize' actions
    # - opened: A new PR was created
    # - synchronize: New commits were pushed to an existing PR
    if action not in ["opened", "synchronize"]:
        log_message(f"Ignoring action: {action}")
        return {"status": "ignored", "reason": f"Action '{action}' not processed"}
    
    # Extract repository and PR information
    repo_full_name = data["repository"]["full_name"]  # e.g., "owner/repo"
    pr_number = data["pull_request"]["number"]        # e.g., 42
    pr_title = data["pull_request"]["title"]          # The PR title
    
    log_message(f"Processing PR #{pr_number} in {repo_full_name}")
    log_message(f"PR Title: {pr_title}")
    
    # Step 1: Fetch the PR diff from GitHub
    log_message("Fetching PR diff from GitHub...")
    diff = get_pull_request_diff(repo_full_name, pr_number)
    
    if not diff:
        log_message("ERROR: Could not fetch PR diff")
        return {"status": "error", "message": "Could not fetch PR diff"}
    
    log_message(f"Fetched diff: {len(diff)} characters")
    
    # Step 2: Send the diff to AI for review
    log_message("Sending diff to AI for review...")
    review_result = review_code(diff)
    
    log_message("Review complete!")
    log_message(f"Summary: {review_result.get('summary', 'No summary')}")
    log_message(f"Issues found: {len(review_result.get('issues', []))}")
    
    # Return the review result
    return {
        "status": "success",
        "repository": repo_full_name,
        "pull_request": pr_number,
        "review": review_result
    }


@router.post("/review")
async def manual_review(request: CodeReviewRequest):
    """
    Manually submit code for AI review.
    
    This endpoint allows testing without GitHub integration.
    Just send code directly and get a review back.
    
    Example request:
    {
        "code": "def hello():\n    print('world')"
    }
    """
    log_message("Received manual review request")
    
    # Check if code was provided
    if not request.code or not request.code.strip():
        raise HTTPException(status_code=400, detail="No code provided")
    
    log_message(f"Code to review: {len(request.code)} characters")
    
    # Send to AI for review
    review_result = review_code(request.code)
    
    log_message("Manual review complete!")
    
    return review_result
