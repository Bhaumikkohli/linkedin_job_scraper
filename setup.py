from setuptools import setup, find_packages

setup(
    name="linkedin-job-scraper",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "selenium>=4.1.0",
        "python-dotenv>=0.19.0",
        "click>=8.0.0",
        "webdriver-manager>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "linkedin-scraper=linkedin_job_scraper.cli:main",
        ],
    },
    python_requires=">=3.8",
)