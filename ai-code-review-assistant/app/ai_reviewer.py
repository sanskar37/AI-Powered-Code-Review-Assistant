"""
ai_reviewer.py - AI Code Reviewer

This file handles communication with the AI (OpenAI-compatible API).
It sends code to the AI and processes the response.
"""

import os
import json
from openai import OpenAI
from app.utils import log_message


def get_openai_client() -> OpenAI:
    """
    Create and return an OpenAI client.
    
    Uses environment variables for configuration:
    - OPENAI_API_KEY: Your API key (required)
    - OPENAI_BASE_URL: Custom API endpoint (optional, for compatible APIs)
    
    Returns:
        An OpenAI client instance
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")  # Optional: for using compatible APIs
    
    if not api_key:
        log_message("ERROR: OPENAI_API_KEY not found in environment variables")
        raise ValueError("OPENAI_API_KEY is required")
    
    # Create client with optional custom base URL
    if base_url:
        log_message(f"Using custom API base URL: {base_url}")
        return OpenAI(api_key=api_key, base_url=base_url)
    else:
        return OpenAI(api_key=api_key)


def create_review_prompt(code_diff: str) -> str:
    """
    Create the prompt that we send to the AI.
    
    This prompt tells the AI:
    - What role it should play (code reviewer)
    - What to look for (bugs, security, performance, quality)
    - How to format the response (JSON)
    - What severity levels to use
    
    Args:
        code_diff: The code changes to review
    
    Returns:
        The complete prompt string
    """
    prompt = f"""You are an expert code reviewer. Analyze the following code diff and provide feedback.

## Instructions:

1. Look for these types of issues:
   - **Bugs**: Logic errors, null pointer risks, off-by-one errors
   - **Security Issues**: SQL injection, XSS, hardcoded secrets, insecure practices
   - **Performance Concerns**: N+1 queries, inefficient loops, memory leaks
   - **Code Quality**: Poor naming, missing error handling, code duplication

2. Classify each issue by severity:
   - **Critical**: Security vulnerabilities, data loss risks, system crashes
   - **High**: Bugs that will cause incorrect behavior
   - **Medium**: Performance issues, maintainability problems
   - **Low**: Style issues, minor improvements

3. Respond with ONLY valid JSON in this exact format:
{{
  "summary": "A brief overall assessment of the code changes",
  "issues": [
    {{
      "severity": "High",
      "message": "Description of the issue",
      "suggestion": "How to fix it"
    }}
  ]
}}

If the code looks good with no issues, return:
{{
  "summary": "Code looks good! No significant issues found.",
  "issues": []
}}

## Code Diff to Review:

```
{code_diff}
```

Remember: Respond with ONLY the JSON object, no additional text or markdown.
"""
    return prompt


def parse_ai_response(response_text: str) -> dict:
    """
    Parse the AI's response into a structured dictionary.
    
    The AI should return JSON, but sometimes it adds extra text.
    This function tries to extract and parse the JSON.
    
    Args:
        response_text: The raw response from the AI
    
    Returns:
        A dictionary with 'summary' and 'issues' keys
    """
    log_message("Parsing AI response...")
    
    # Try to parse the response directly as JSON
    try:
        result = json.loads(response_text)
        log_message("Successfully parsed JSON response")
        return result
    except json.JSONDecodeError:
        pass  # Response isn't pure JSON, try to extract it
    
    # Try to find JSON within the response
    # Sometimes the AI wraps JSON in markdown code blocks
    try:
        # Look for JSON between ```json and ``` markers
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
            result = json.loads(json_str)
            log_message("Extracted JSON from markdown code block")
            return result
        
        # Look for JSON between ``` markers (without json label)
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
            result = json.loads(json_str)
            log_message("Extracted JSON from code block")
            return result
        
        # Look for JSON starting with { and ending with }
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start != -1 and end != 0:
            json_str = response_text[start:end]
            result = json.loads(json_str)
            log_message("Extracted JSON from response text")
            return result
            
    except (json.JSONDecodeError, ValueError) as e:
        log_message(f"Failed to extract JSON: {e}")
    
    # If all parsing fails, return a fallback response
    log_message("WARNING: Could not parse AI response, returning fallback")
    return {
        "summary": "Review completed but response parsing failed.",
        "issues": [
            {
                "severity": "Low",
                "message": "AI response could not be parsed",
                "suggestion": "Check the raw AI output for details"
            }
        ],
        "raw_response": response_text[:500]  # Include first 500 chars for debugging
    }


def review_code(code_diff: str) -> dict:
    """
    Main function to review code using AI.
    
    This function:
    1. Creates an OpenAI client
    2. Builds the review prompt
    3. Sends the request to the AI
    4. Parses and returns the response
    
    Args:
        code_diff: The code changes to review (diff format or raw code)
    
    Returns:
        A dictionary containing:
        - summary: Overall assessment
        - issues: List of found issues with severity, message, and suggestion
    """
    log_message("Starting AI code review...")
    
    # Limit the diff size to avoid token limits
    # Most models have a context limit; we keep it reasonable
    MAX_DIFF_LENGTH = 10000  # Characters
    if len(code_diff) > MAX_DIFF_LENGTH:
        log_message(f"Diff is too long ({len(code_diff)} chars), truncating...")
        code_diff = code_diff[:MAX_DIFF_LENGTH] + "\n\n[... diff truncated for length ...]"
    
    try:
        # Create the OpenAI client
        client = get_openai_client()
        
        # Create the prompt
        prompt = create_review_prompt(code_diff)
        
        log_message("Sending request to AI...")
        
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to gpt-4 for better results
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert code reviewer. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature = more focused/consistent responses
            max_tokens=2000   # Limit response length
        )
        
        # Extract the response text
        response_text = response.choices[0].message.content
        log_message(f"Received response: {len(response_text)} characters")
        
        # Parse and return the response
        return parse_ai_response(response_text)
        
    except ValueError as e:
        # Missing API key
        log_message(f"Configuration error: {e}")
        return {
            "summary": "Review failed due to configuration error.",
            "issues": [
                {
                    "severity": "Critical",
                    "message": str(e),
                    "suggestion": "Check your .env file and ensure OPENAI_API_KEY is set"
                }
            ]
        }
        
    except Exception as e:
        # Any other error
        log_message(f"AI review failed: {e}")
        return {
            "summary": "Review failed due to an error.",
            "issues": [
                {
                    "severity": "Critical",
                    "message": f"AI review error: {str(e)}",
                    "suggestion": "Check your API key and network connection"
                }
            ]
        }
