import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Constants
BASE_URL = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?occupation_ids%5B%5D=7&occupation_ids%5B%5D=8&page="
SAVE_PATH = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_urls_vieclam24h.txt"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_job_urls(n_pages):
    driver = setup_driver()
    job_urls = set()  # Use a set to store unique URLs

    for page in range(1, n_pages + 1):
        url = f"{BASE_URL}{page}"
        logging.info(f"Scraping page {page}: {url}")
        
        try:
            driver.get(url)
            # Wait for the job listings container to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="flex flex-col gap-3 sm_cv:gap-2"]'))
            )

            # Find all job links within the specified div
            job_links = driver.find_elements(By.XPATH, '//div[@class="flex flex-col gap-3 sm_cv:gap-2"]//a[@target="_blank"]')
            page_urls = set()

            for link in job_links:
                job_url = link.get_attribute("href")
                if job_url and job_url.startswith("/"):
                    job_url = "https://vieclam24h.vn" + job_url
                if job_url:
                    page_urls.add(job_url)

            logging.info(f"Page {page}: Found {len(page_urls)} job URLs")
            if len(page_urls) < 30:  # Debug when job count is low
                logging.warning(f"Fewer than 30 job URLs found on page {page}! Possible issue with page loading.")

            job_urls.update(page_urls)

        except TimeoutException:
            logging.warning(f"Timeout on page {page}. Skipping to the next page.")
        except Exception as e:
            logging.error(f"Error on page {page}: {e}")

        # Add a small delay between pages to avoid overwhelming the server
        time.sleep(2)

    driver.quit()

    # Save results
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as file:
        for url in job_urls:
            file.write(url + "\n")

    logging.info(f"Scraped a total of {len(job_urls)} job URLs and saved to {SAVE_PATH}")

# Example usage
n = 15  # Number of pages to scrape
scrape_job_urls(n)