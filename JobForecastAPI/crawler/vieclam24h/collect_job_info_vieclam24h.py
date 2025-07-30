import os
import csv
import time
import logging
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from unidecode import unidecode 
import sys
# Fix import path for db_handler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db_handler import insert_job

# Constants
JOB_URLS_FILE = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_urls_vieclam24h.txt"
# JOB_URLS_FILE = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/random_job_urls_vieclam24h.txt"
OUTPUT_CSV = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_info_vieclam24h.csv"
# OUTPUT_CSV = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/job_info_vieclam24h_testing.csv"
FAILED_URLS_FILE = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/job-urls/vieclam24h/failed_urls.txt"
API_URL = "http://localhost:5000/api/job-urls"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import random
import time

def setup_driver():
    options = Options()

    # Common stealthy arguments
    options.add_argument("--headless=new")  # use the new headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Random user-agent from a list
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    ]
    options.add_argument(f"--user-agent={random.choice(user_agents)}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Stealth injection for Chrome
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
        """
    })

    return driver

def extract_text(element, default=""):
    """Helper function to extract text from a Selenium element."""
    try:
        return element.text.strip()
    except (AttributeError, NoSuchElementException):
        return default

def generate_random_age_range():
    """Generate a random age range between 20 and 35."""
    start_age = random.randint(20, 33)  # Ensure there's room for a range
    end_age = start_age + 2  # Add 2 to create a range (e.g., 20-22)
    return f"{start_age} - {end_age}"

def generate_random_probation_period():
    """Generate a random probation period between 1 and 12 months."""
    return f"{random.randint(1, 12)} tháng"

def remove_accents_and_non_ascii(text):
    """Remove accents and non-ASCII characters from text."""
    if isinstance(text, str):
        # Remove accents
        text = unidecode(text)
        # Remove non-ASCII characters
        return ''.join(c for c in text if ord(c) < 128)
    return text

def scrape_job_info(driver, url):
    """Scrape job information from a single job URL."""
    driver.get(url)
    time.sleep(3)  # Allow more time for the page to load

    job_info = {
        "Company_Name": "",
        "Job": "",
        "City": "",
        "Time": "",
        "Number_Recruitment": "",
        "Sexual": "",
        "Profession": "",
        "Title": "",
        "Level": "",
        "Salary": "",
        "Education": "",
        "Experience": "",
        "Description": "",
        "Requirement": "",
        "Right": "",
        "Place": "",
        "Number_Employee": "",
        "Giới thiệu công ty": "",
        "Work_Way": "",
        "Deadline": "",
        "Age": "",
        "Probation_Time": "",  # New field
        "Source_Picture": "",
        "Job_URL": url,
    }

    try:
        job_info["Company_Name"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(@class, "text-se-neutral-64")]'))
    except NoSuchElementException:
        pass

    try:
        job_info["City"] = extract_text(driver.find_element(By.XPATH, '//a[@class="hover:text-se-accent"]/span'))
    except NoSuchElementException:
        pass

    try:
        job_info["Time"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Ngày đăng")]/p[@class="text-14"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Number_Recruitment"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Số lượng tuyển")]/p[@class="text-14"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Sexual"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Yêu cầu giới tính")]/p[@class="text-14"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Profession"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Ngành nghề")]//a[contains(text(), "IT")]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Title"] = extract_text(driver.find_element(By.XPATH, '//h1[@class="font-semibold text-18 md:text-24 leading-snug"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Job"] = extract_text(driver.find_element(By.XPATH, '//h1[@class="font-semibold text-18 md:text-24 leading-snug"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Level"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Cấp bậc")]/p[@class="text-14"]'))
    except NoSuchElementException:
        pass

    # Extract "Mức lương"
    try:
        job_info["Salary"] = extract_text(driver.find_element(By.XPATH, '//h2[contains(., "Mức lương")]//p[@class="font-semibold text-14 text-[#8B5CF6]"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Education"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Yêu cầu bằng cấp")]/p[@class="text-14"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Experience"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Yêu cầu kinh nghiệm")]/p[@class="text-14"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Description"] = "; ".join([
            li.text.strip()
            for li in driver.find_elements(
                By.XPATH,
                '//h2[contains(text(), "Mô tả công việc") or contains(text(), "Job description")]/following-sibling::div[contains(@class, "text-description")]//li'
            )
        ])
    except NoSuchElementException:
        pass

    try:
        job_info["Requirement"] = "; ".join([
            li.text.strip()
            for li in driver.find_elements(
                By.XPATH,
                '//h2[contains(text(), "Yêu cầu công việc") or contains(text(), "Job requirements")]/following-sibling::div[contains(@class, "text-description")]//li'
            )
        ])
    except NoSuchElementException:
        pass

    try:
        job_info["Right"] = "; ".join([
            li.text.strip()
            for li in driver.find_elements(
                By.XPATH,
                '//h2[contains(text(), "Quyền lợi") or contains(text(), "Benefits")]/following-sibling::div[contains(@class, "text-description")]//li'
            )
        ])
    except NoSuchElementException:
        pass

    try:
        job_info["Place"] = extract_text(driver.find_element(By.XPATH, '//h4[contains(., "Địa chỉ")]//div[@class="text-14 text-se-grey-48 font-semibold"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Number_Employee"] = extract_text(driver.find_element(By.XPATH, '//h4[contains(., "Quy mô")]//div[@class="text-14 text-se-grey-48 font-semibold"]'))
    except NoSuchElementException:
        pass

    try:
        job_info["Giới thiệu công ty"] = extract_text(driver.find_element(By.XPATH, '//div[@class="max-h-[84px] overflow-hidden mt-4 text-14 text-se-neutral-84 mb-2"]'))
    except NoSuchElementException:
        pass

    # Extract "Hình thức làm việc"
    try:
        job_info["Work_Way"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Hình thức làm việc")]/p[@class="text-14"]'))
    except NoSuchElementException:
        pass

    # Extract "Hạn nộp hồ sơ"
    try:
        job_info["Deadline"] = extract_text(driver.find_element(By.XPATH, '//h2[contains(., "Hạn nộp hồ sơ")]//p[@class="text-14 text-[#414045]"]'))
    except NoSuchElementException:
        pass

    # Extract "Độ tuổi"
    try:
        job_info["Age"] = extract_text(driver.find_element(By.XPATH, '//h3[contains(., "Độ tuổi")]/p[@class="text-14"]'))
    except NoSuchElementException:
        # If "Độ tuổi" is not found, generate a random age range
        job_info["Age"] = generate_random_age_range()

    # Extract "Source_Picture"
    try:
        job_info["Source_Picture"] = driver.find_element(By.XPATH, '//img[contains(@class, "rounded")]').get_attribute("src")
    except NoSuchElementException:
        pass

    # Extract "Thời gian thử việc"
    try:
        probation_element = driver.find_element(By.XPATH, '//h3[contains(., "Thời gian thử việc")]/p[@class="text-14"]')
        job_info["Probation_Time"] = extract_text(probation_element)
    except NoSuchElementException:
        # If "Thời gian thử việc" is not found, generate a random probation period
        job_info["Probation_Time"] = generate_random_probation_period()

        # Process the scraped data
    for key in job_info:
        job_info[key] = remove_accents_and_non_ascii(job_info[key])

    return job_info

def fetch_existing_urls():
    """Fetch existing job URLs from the MySQL database."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad responses
        job_urls = response.json()
        
        # Log the response content for debugging
        logging.info(f"Response from API: {job_urls}")

        return {url.split('?')[0] for url in job_urls}  # Focus on base URLs
    except requests.RequestException as e:
        logging.error(f"Error fetching job URLs: {e}")
        return set()
    
def insert_jobs_from_scraped_data(job_info):
    """Insert scraped job information into the database."""
    # Assuming insert_jobs_from_csv is a function that takes a single job_info dict
    # Adjust this function as needed based on your database handler implementation
    try:
        # Call the function to insert into the database
        insert_job(job_info)  # Modify this based on your actual function
        logging.info(f"Debug - Inserted Job Info: {job_info}")
        logging.info(f"Inserted job info into the database: {job_info['Job']}")
        # Debug print out job info after successful insertion
        # print("Debug - Inserted Job Info:", job_info)  # Print job info to console
    except Exception as e:
        logging.error(f"Error inserting job info into the database: {e}")

def scrape_all_jobs(job_urls, existing_urls):
    driver = setup_driver()
    job_data = []
    failed_urls = []

    for i, url in enumerate(job_urls):
        base_url = url.split('?')[0]  # Get the base URL
        if base_url in existing_urls:
            logging.info(f"Duplicate URL found, skipping: {url}")
            continue  # Skip if the base URL is found in the existing URLs

        logging.info(f"Scraping job URL {i + 1}/{len(job_urls)}: {url}")
        try:
            job_info = scrape_job_info(driver, url)
            insert_jobs_from_scraped_data(job_info)
            job_data.append(job_info)

            # Save progress incrementally (e.g., every 10 URLs)
            if (i + 1) % 10 == 0:
                save_to_csv(job_data, OUTPUT_CSV)
                logging.info(f"Saved progress after {i + 1} URLs.")

        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")
            failed_urls.append(url)

    driver.quit()

    # Save final results to CSV
    save_to_csv(job_data, OUTPUT_CSV)
    logging.info(f"Scraped {len(job_data)} jobs and saved to {OUTPUT_CSV}")

    # Save failed URLs to a file
    if failed_urls:
        with open(FAILED_URLS_FILE, "w", encoding="utf-8") as file:
            for failed_url in failed_urls:
                file.write(failed_url + "\n")
        logging.info(f"Saved {len(failed_urls)} failed URLs to {FAILED_URLS_FILE}")

def save_to_csv(job_data, file_path):
    """Save job data to a CSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = job_data[0].keys() if job_data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(job_data)

def main():
    # Read job URLs from file
    with open(JOB_URLS_FILE, "r", encoding="utf-8") as file:
        job_urls = [line.strip() for line in file.readlines()]

    # Fetch existing URLs from the database
    existing_urls = fetch_existing_urls()
    logging.info(f"Fetched {len(existing_urls)} existing URLs from the database.")

    # Scrape all URLs
    scrape_all_jobs(job_urls, existing_urls)

# Run the main function
if __name__ == "__main__":
    main()