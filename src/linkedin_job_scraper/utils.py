import re
import os
import logging

def clean_filename(filename):
    """Clean filename by removing invalid characters."""
    # Remove invalid filename characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')
    return cleaned

def setup_logger():
    """Set up logging configuration."""
    logger = logging.getLogger('linkedin_scraper')
    logger.setLevel(logging.INFO)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

def ensure_output_dir(output_dir):
    """Ensure output directory exists, create if it doesn't."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")
