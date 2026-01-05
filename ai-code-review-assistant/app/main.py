"""
main.py - FastAPI Entry Point

This is the main file that starts our application.
It sets up the FastAPI app and includes all our routes.
"""

# Import FastAPI framework
from fastapi import FastAPI

# Import our webhook router (contains the webhook endpoint)
from app.webhook import router as webhook_router

# Import dotenv to load environment variables from .env file
from dotenv import load_dotenv

# Load environment variables at startup
# This reads the .env file and makes variables available via os.getenv()
load_dotenv()

# Create the FastAPI application instance
# title and description appear in the auto-generated API docs
app = FastAPI(
    title="AI Code Review Assistant",
    description="Automatically review GitHub Pull Requests using AI",
    version="1.0.0"
)

# Include the webhook router
# This adds all routes defined in webhook.py to our app
app.include_router(webhook_router)


# Health check endpoint
# This is a simple endpoint to verify the server is running
@app.get("/")
def health_check():
    """
    Simple health check endpoint.
    Returns a message confirming the server is running.
    """
    return {
        "status": "running",
        "message": "AI Code Review Assistant is ready!",
        "docs": "Visit /docs for API documentation"
    }


# This runs when you execute: python app/main.py
# But normally we use: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
