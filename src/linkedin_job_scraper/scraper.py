from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from .config import Config
from .utils import clean_filename, setup_logger

logger = setup_logger()

class LinkedInScraper:
    """LinkedIn job posting scraper."""
    
    def __init__(self):
        """Initialize the scraper with Chrome WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    
    def login(self):
        """Login to LinkedIn using credentials from config."""
        try:
            self.driver.get(Config.LOGIN_URL)
            
            # Enter email
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(Config.LINKEDIN_EMAIL)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(Config.LINKEDIN_PASSWORD)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            logger.info("Successfully logged in to LinkedIn")
            
        except Exception as e:
            logger.error(f"Failed to login: {str(e)}")
            raise
    
    def search_jobs(self, position):
        """Search for jobs with given position and filters."""
        try:
            # Navigate to jobs page with filters
            search_url = (
                f"{Config.BASE_URL}/jobs/search/?"
                f"keywords={position}&"
                f"location={Config.LOCATION}&"
                f"f_E=2"  # Entry level filter
            )
            self.driver.get(search_url)
            time.sleep(3)  # Allow page to load
            logger.info(f"Searching for {position} positions in {Config.LOCATION}")
            
        except Exception as e:
            logger.error(f"Failed to search jobs: {str(e)}")
            raise
    
    def extract_job_posts(self, num_posts, output_dir):
        """Extract job posts and save to output directory."""
        try:
            job_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".job-card-container")
                )
            )
            
            extracted_count = 0
            for job_card in job_cards[:num_posts]:
                try:
                    # Click on job card to load details
                    job_card.click()
                    time.sleep(2)
                    
                    # Extract job details
                    title = self.driver.find_element(
                        By.CSS_SELECTOR, ".jobs-unified-top-card__job-title"
                    ).text
                    company = self.driver.find_element(
                        By.CSS_SELECTOR, ".jobs-unified-top-card__company-name"
                    ).text
                    description = self.driver.find_element(
                        By.CSS_SELECTOR, ".jobs-description"
                    ).text
                    
                    # Create output file
                    filename = clean_filename(f"{title}_{company}.txt")
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"Title: {title}\n")
                        f.write(f"Company: {company}\n")
                        f.write("\nDescription:\n")
                        f.write(description)
                    
                    extracted_count += 1
                    logger.info(f"Extracted job post {extracted_count}: {title}")
                    
                except Exception as e:
                    logger.error(f"Failed to extract job post: {str(e)}")
                    continue
                
            logger.info(f"Successfully extracted {extracted_count} job posts")
            
        except Exception as e:
            logger.error(f"Failed to extract job posts: {str(e)}")
            raise
        
        finally:
            self.driver.quit()