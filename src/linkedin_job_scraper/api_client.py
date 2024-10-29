import requests
from urllib.parse import urlencode
import json
import os
from .config import Config
from .utils import setup_logger

logger = setup_logger()

class LinkedInAPIClient:
    """LinkedIn API client for job searching."""
    
    def __init__(self):
        """Initialize the API client."""
        self.access_token = None
        self.headers = None
    
    def get_auth_url(self):
        """Get the OAuth authorization URL."""
        params = {
            'response_type': 'code',
            'client_id': Config.CLIENT_ID,
            'redirect_uri': Config.REDIRECT_URI,
            'scope': 'r_liteprofile r_emailaddress jobs_jymbii'
        }
        return f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    
    def get_access_token(self, auth_code):
        """Exchange authorization code for access token."""
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
            'redirect_uri': Config.REDIRECT_URI
        }
        
        response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            return True
        return False
    
    def search_jobs(self, keywords, location="Australia", experience="ENTRY_LEVEL", limit=10):
        """Search for jobs using LinkedIn API."""
        if not self.headers:
            raise Exception("Not authenticated. Call get_access_token first.")
        
        params = {
            'keywords': keywords,
            'location': location,
            'experience': experience,
            'count': limit
        }
        
        response = requests.get(
            Config.JOBS_SEARCH_URL,
            headers=self.headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API request failed: {response.status_code}")
            return None
    
    def save_job_posts(self, jobs_data, output_dir):
        """Save job posts to output directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for job in jobs_data.get('elements', []):
            try:
                job_id = job['entityUrn'].split(':')[-1]
                filename = f"job_{job_id}.json"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(job, f, indent=2)
                
                logger.info(f"Saved job post: {filename}")
                
            except Exception as e:
                logger.error(f"Failed to save job post: {str(e)}")
                continue