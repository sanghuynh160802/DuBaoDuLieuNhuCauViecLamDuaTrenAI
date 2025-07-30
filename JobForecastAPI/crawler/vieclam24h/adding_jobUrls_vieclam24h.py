import os
import time
import logging
import re
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
OLD_FILE_PATH = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_urls_vieclam24h.txt"
NEW_FILE_PATH = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_urls_vieclam24h.txt"
# OLD_FILE_PATH = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_urls_vieclam24h_test_1.txt"
# NEW_FILE_PATH = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_urls_vieclam24h_test_2.txt"

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--user-agent=Mozilla/5.0")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def normalize_url(url):
    """Extract the canonical part of a job URL (remove tracking parameters and extra slugs)."""
    match = re.search(r"(https:\/\/vieclam24h\.vn\/[^\s?]+?id\d+\.html)", url)
    return match.group(1) if match else url

def read_existing_urls(file_path):
    """Read and normalize existing URLs."""
    normalized = set()
    original = dict()
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                url = line.strip()
                if url:
                    core = normalize_url(url)
                    normalized.add(core)
                    original[core] = url  # Keep one original version
    return normalized, original

def scrape_job_urls(n_pages, existing_cores):
    driver = setup_driver()
    new_urls = dict()  # key = normalized URL, value = full original URL

    for page in range(1, n_pages + 1):
        page_url = f"{BASE_URL}{page}"
        logging.info(f"Scraping page {page}: {page_url}")

        try:
            driver.get(page_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="flex flex-col gap-3 sm_cv:gap-2"]'))
            )
            job_links = driver.find_elements(By.XPATH, '//div[@class="flex flex-col gap-3 sm_cv:gap-2"]//a[@target="_blank"]')

            for link in job_links:
                job_url = link.get_attribute("href")
                if job_url and job_url.startswith("/"):
                    job_url = "https://vieclam24h.vn" + job_url
                core_url = normalize_url(job_url)
                if core_url and core_url not in existing_cores and core_url not in new_urls:
                    new_urls[core_url] = job_url  # Save original version

        except TimeoutException:
            logging.warning(f"Timeout on page {page}")
        except Exception as e:
            logging.error(f"Error on page {page}: {e}")
        time.sleep(2)

    driver.quit()
    return new_urls

def save_urls(file_path, url_dict):
    """Save full original URLs to file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        for url in url_dict.values():
            file.write(url + "\n")
    logging.info(f"Saved {len(url_dict)} URLs to {file_path}")

def main():
    existing_cores, original_urls = read_existing_urls(OLD_FILE_PATH)
    logging.info(f"Loaded {len(existing_cores)} normalized existing URLs.")

    n_pages = 15
    new_urls = scrape_job_urls(n_pages, existing_cores)
    logging.info(f"Found {len(new_urls)} new unique job URLs.")

    # Merge new with old
    all_urls = original_urls.copy()
    all_urls.update(new_urls)

    # Save merged URLs
    save_urls(NEW_FILE_PATH, all_urls)

if __name__ == "__main__":
    main()
