"""
utils.py - Helper Functions

This file contains utility functions used across the application.
Keeping these in one place makes the code cleaner and easier to maintain.
"""

from datetime import datetime


def log_message(message: str) -> None:
    """
    Print a log message with a timestamp.
    
    This is a simple logging function that adds timestamps to messages.
    In a production app, you might use Python's logging module instead.
    
    Args:
        message: The message to log
    
    Example:
        log_message("Server started")
        # Output: [2024-01-15 10:30:45] Server started
    """
    # Get current time formatted nicely
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Print the message with timestamp
    print(f"[{timestamp}] {message}")


def truncate_string(text: str, max_length: int = 100) -> str:
    """
    Truncate a string if it's longer than max_length.
    
    Useful for logging long strings without flooding the console.
    
    Args:
        text: The string to truncate
        max_length: Maximum length before truncating (default: 100)
    
    Returns:
        The truncated string with "..." if it was shortened
    
    Example:
        truncate_string("Hello World", 5)  # Returns "Hello..."
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_issue_count(issues: list) -> str:
    """
    Create a human-readable summary of issue counts by severity.
    
    Args:
        issues: List of issue dictionaries with 'severity' key
    
    Returns:
        A formatted string like "2 Critical, 3 High, 1 Medium"
    
    Example:
        issues = [
            {"severity": "High", "message": "..."},
            {"severity": "High", "message": "..."},
            {"severity": "Low", "message": "..."}
        ]
        format_issue_count(issues)  # Returns "2 High, 1 Low"
    """
    if not issues:
        return "No issues found"
    
    # Count issues by severity
    counts = {}
    for issue in issues:
        severity = issue.get("severity", "Unknown")
        counts[severity] = counts.get(severity, 0) + 1
    
    # Format the counts
    # Order by severity (Critical first, then High, Medium, Low)
    severity_order = ["Critical", "High", "Medium", "Low"]
    parts = []
    
    for severity in severity_order:
        if severity in counts:
            parts.append(f"{counts[severity]} {severity}")
    
    # Add any unknown severities at the end
    for severity, count in counts.items():
        if severity not in severity_order:
            parts.append(f"{count} {severity}")
    
    return ", ".join(parts)


def is_valid_pr_event(payload: dict) -> bool:
    """
    Check if a webhook payload is a valid Pull Request event.
    
    Args:
        payload: The webhook payload dictionary
    
    Returns:
        True if this is a valid PR event we should process
    """
    # Must have pull_request key
    if "pull_request" not in payload:
        return False
    
    # Must have repository info
    if "repository" not in payload:
        return False
    
    # Action must be one we care about
    action = payload.get("action", "")
    valid_actions = ["opened", "synchronize", "reopened"]
    
    return action in valid_actions


def sanitize_for_logging(text: str) -> str:
    """
    Remove or mask sensitive information from text before logging.
    
    This helps prevent accidentally logging secrets, tokens, or passwords.
    
    Args:
        text: The text to sanitize
    
    Returns:
        The sanitized text with sensitive info masked
    """
    import re
    
    # Patterns to look for (simplified examples)
    patterns = [
        # GitHub tokens
        (r'ghp_[a-zA-Z0-9]{36}', 'ghp_***REDACTED***'),
        # OpenAI API keys
        (r'sk-[a-zA-Z0-9]{48}', 'sk-***REDACTED***'),
        # Generic "token" or "key" in key=value format
        (r'(token|key|secret|password)=\S+', r'\1=***REDACTED***'),
    ]
    
    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result
