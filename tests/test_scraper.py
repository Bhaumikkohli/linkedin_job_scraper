import pytest
from selenium.common.exceptions import TimeoutException
from linkedin_job_scraper.scraper import LinkedInScraper
from linkedin_job_scraper.config import Config

def test_login(chrome_driver):
    """Test LinkedIn login functionality."""
    scraper = LinkedInScraper()
    
    try:
        scraper.login()
        # Check if login was successful by verifying navigation bar presence
        nav_element = chrome_driver.find_element_by_id("global-nav")
        assert nav_element is not None
        
    except TimeoutException:
        pytest.fail("Login timeout - check credentials or LinkedIn availability")
    except Exception as e:
        pytest.fail(f"Login failed: {str(e)}")

def test_search_jobs(chrome_driver):
    """Test job search functionality."""
    scraper = LinkedInScraper()
    position = "Software Engineer"
    
    try:
        scraper.login()
        scraper.search_jobs(position)
        
        # Verify search results
        job_cards = chrome_driver.find_elements_by_css_selector(".job-card-container")
        assert len(job_cards) > 0
        
    except Exception as e:
        pytest.fail(f"Job search failed: {str(e)}")

def test_extract_job_posts(chrome_driver, test_output_dir):
    """Test job post extraction functionality."""
    scraper = LinkedInScraper()
    position = "Data Analyst"
    num_posts = 3
    
    try:
        scraper.login()
        scraper.search_jobs(position)
        scraper.extract_job_posts(num_posts, test_output_dir)
        
        # Verify output files
        output_files = list(test_output_dir.glob("*.txt"))
        assert len(output_files) == num_posts
        
        # Verify file contents
        for file_path in output_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Title:" in content
                assert "Company:" in content
                assert "Description:" in content
                
    except Exception as e:
        pytest.fail(f"Job post extraction failed: {str(e)}")
