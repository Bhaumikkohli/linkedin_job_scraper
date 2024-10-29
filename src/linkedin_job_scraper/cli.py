import click
from .api_client import LinkedInAPIClient
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback."""
    
    def do_GET(self):
        """Process the callback request."""
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            self.server.auth_code = params['code'][0]
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Authentication successful! You can close this window.")

@click.command()
@click.option('--position', required=True, help='Job position to search for')
@click.option('--num-posts', default=10, help='Number of job posts to extract')
@click.option('--output-dir', default='./output', help='Directory to save job posts')
def main(position, num_posts, output_dir):
    """LinkedIn job search CLI using official API."""
    client = LinkedInAPIClient()
    
    # Start local server for OAuth callback
    server = HTTPServer(('localhost', 8000), OAuthCallbackHandler)
    server.auth_code = None
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser for authentication
    auth_url = client.get_auth_url()
    webbrowser.open(auth_url)
    
    click.echo("Please authenticate in your browser...")
    
    # Wait for callback
    while server.auth_code is None:
        pass
    
    # Stop server
    server.shutdown()
    server.server_close()
    
    # Get access token
    if client.get_access_token(server.auth_code):
        # Search for jobs
        jobs_data = client.search_jobs(position, limit=num_posts)
        if jobs_data:
            client.save_job_posts(jobs_data, output_dir)
            click.echo(f"Successfully extracted {num_posts} job posts to {output_dir}")
        else:
            click.echo("Failed to retrieve job posts")
    else:
        click.echo("Authentication failed")

if __name__ == '__main__':
    main()