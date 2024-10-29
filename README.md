# Project structure
linkedin_job_scraper/
├── README.md
├── setup.py
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   └── linkedin_job_scraper/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── scraper.py
│       └── utils.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_scraper.py
    └── test_utils.py

# README.md
# LinkedIn Job Scraper

A command-line tool to scrape job postings from LinkedIn based on job position and location filters.

## Features
- Scrape LinkedIn job postings based on position title
- Filter jobs by location (Australia)
- Filter by experience level (Entry level)
- Customizable number of posts to extract
- Outputs individual job posts as text files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/linkedin-job-scraper.git
cd linkedin-job-scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Install Chrome WebDriver:
Make sure you have Google Chrome installed and download the appropriate ChromeDriver version from:
https://sites.google.com/chromium.org/driver/

5. Copy .env.example to .env and set your LinkedIn credentials:
```bash
cp .env.example .env
```

## Usage

```bash
linkedin-scraper --position "Data Engineer" --num-posts 10 --output-dir ./job_posts
```

Arguments:
- `--position`: Job position to search for
- `--num-posts`: Number of job posts to extract (default: 10)
- `--output-dir`: Directory to save job posts (default: ./output)

## Running Tests

```bash
pytest tests/
```

## License

MIT License