from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# File path to save the data
output_file_path = r"D:\SANG\Do An Tot Nghiep\crawl-data\data\data_topdev\topdev_jobUrls_1.txt"

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open website
url = "https://topdev.vn/it-jobs"
driver.get(url)
time.sleep(3)  # Wait for the initial page load

# URL collection setup
all_urls = set()  # Tracks every URL detected across all scrolls
collected_urls = set()  # Tracks only URLs after `start_collecting_after`

# Scrolling parameters
scroll_limit = 33  # Maximum number of scrolls
start_collecting_after = 23  # Begin collecting URLs after this many scrolls
scroll_count = 0  # Scroll counter

while scroll_count < scroll_limit:
    # Scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for new data to load
    scroll_count += 1

    # Find all job links on the page
    jobs = driver.find_elements(By.CSS_SELECTOR, "ul.mt-4 li.mb-4.last\\:mb-0 a[target='_blank']")
    current_urls = {job.get_attribute("href") for job in jobs}

    # Track all URLs, and add to collected only after the threshold
    if scroll_count >= start_collecting_after:
        # Add only new URLs after threshold
        new_urls = current_urls - all_urls
        collected_urls.update(new_urls)

    # Update all URLs
    all_urls.update(current_urls)

    print(f"Scroll {scroll_count}: {len(current_urls)} URLs found, {len(collected_urls)} collected.")

    # Stop if no new URLs are loaded
    if scroll_count >= start_collecting_after and not new_urls:
        print("No new URLs loaded, stopping early.")
        break

# Load existing URLs from the file (if it exists)
existing_urls = set()
if os.path.exists(output_file_path):
    with open(output_file_path, "r", encoding="utf-8") as file:
        existing_urls = set(file.read().splitlines())

# Add new URLs to the file, avoiding duplicates
new_urls_to_save = collected_urls - existing_urls
with open(output_file_path, "a", encoding="utf-8") as file:  # Append new URLs
    for job_url in new_urls_to_save:
        file.write(job_url + "\n")
        print(f"Added: {job_url}")

# Close the browser
driver.quit()

print(f"Job data successfully saved to: {output_file_path}")
