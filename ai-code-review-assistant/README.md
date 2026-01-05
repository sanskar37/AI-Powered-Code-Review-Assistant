# AI-Powered Code Review Assistant

A beginner-friendly Python application that automatically reviews GitHub Pull Requests using AI.

## What This Does

1. Receives GitHub Pull Request events via webhook
2. Fetches the code changes (diff) from the PR
3. Sends the diff to an AI (OpenAI-compatible) for analysis
4. Returns structured feedback with severity levels

## Project Structure

```
ai-code-review-assistant/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── webhook.py           # GitHub webhook handler
│   ├── github_client.py     # Fetch PR diffs
│   ├── ai_reviewer.py       # Call LLM and process response
│   └── utils.py             # Helper functions
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### Step 1: Clone and Install Dependencies

```bash
# Navigate to the project folder
cd ai-code-review-assistant

# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys:
# - GITHUB_TOKEN: Your GitHub Personal Access Token
# - OPENAI_API_KEY: Your OpenAI API key
# - GITHUB_WEBHOOK_SECRET: A secret string for webhook verification
```

### Step 3: Create a GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token and add it to your `.env` file

### Step 4: Run the Application

```bash
# Start the server
uvicorn app.main:app --reload --port 8000
```

The API will be available at: http://localhost:8000

### Step 5: Expose Your Local Server (for GitHub Webhooks)

To receive GitHub webhooks locally, use ngrok:

```bash
# Install ngrok (https://ngrok.com/)
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Step 6: Configure GitHub Webhook

1. Go to your GitHub repository → Settings → Webhooks
2. Click "Add webhook"
3. Set:
   - **Payload URL**: `https://your-ngrok-url.ngrok.io/webhook`
   - **Content type**: `application/json`
   - **Secret**: Same value as `GITHUB_WEBHOOK_SECRET` in your `.env`
   - **Events**: Select "Pull requests"
4. Click "Add webhook"

## API Endpoints

### Health Check
```
GET /
```
Returns a simple status message.

### Webhook Endpoint
```
POST /webhook
```
Receives GitHub Pull Request events.

### Manual Review
```
POST /review
```
Manually submit code for review.

**Request Body:**
```json
{
  "code": "def hello():\n    print('world')"
}
```

**Response:**
```json
{
  "summary": "Overall review summary",
  "issues": [
    {
      "severity": "Medium",
      "message": "Missing docstring",
      "suggestion": "Add a docstring explaining what this function does"
    }
  ]
}
```

## How It Works

1. **GitHub sends a webhook** when a PR is opened or updated
2. **FastAPI receives the event** and extracts the PR details
3. **GitHub Client fetches the diff** using the GitHub API
4. **AI Reviewer analyzes the code** and returns structured feedback
5. **Response is logged** and sent back as JSON

## Troubleshooting

### "401 Unauthorized" from GitHub
- Check that your `GITHUB_TOKEN` is valid and has the `repo` scope

### "Invalid signature" webhook error
- Make sure `GITHUB_WEBHOOK_SECRET` matches exactly in both your `.env` and GitHub webhook settings

### AI not responding
- Verify your `OPENAI_API_KEY` is valid
- Check you have API credits available

## License

MIT License - Feel free to use and modify!
