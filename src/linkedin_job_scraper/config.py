class Config:
    """Configuration for LinkedIn API access."""
    
    # LinkedIn API endpoints
    API_BASE_URL = "https://api.linkedin.com/v2"
    JOBS_SEARCH_URL = f"{API_BASE_URL}/jobs-search"
    
    # OAuth 2.0 settings
    CLIENT_ID = "your_client_id"  # Get from LinkedIn Developer Portal
    CLIENT_SECRET = "your_client_secret"  # Get from LinkedIn Developer Portal
    REDIRECT_URI = "http://localhost:8000/callback"