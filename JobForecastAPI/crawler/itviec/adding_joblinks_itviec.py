import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import os
import random

# === File paths ===
existing_file_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\itviec\itviec_jobUrls.txt"
new_file_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\itviec\itviec_jobUrls.txt"

# === Number of pages to scrape ===
start_page = 1
end_page = 50

# === Base URL template ===
base_url = "https://itviec.com/it-jobs?page={}"

# === Load existing URLs ===
all_urls = set()
if os.path.exists(existing_file_path):
    with open(existing_file_path, "r", encoding="utf-8") as file:
        all_urls = set(line.strip() for line in file)
    print(f"✅ Loaded {len(all_urls)} existing URLs from {existing_file_path}")

# === Random user-agent ===
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
]
user_agent = random.choice(user_agents)

# === Setup undetected Chrome options ===
options = uc.ChromeOptions()
options.headless = True
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument(f'--user-agent={user_agent}')

# === Initialize browser ===
driver = uc.Chrome(options=options)

try:
    for page in range(start_page, end_page + 1):
        url = base_url.format(page)
        print(f"\n🌐 Processing page: {page} -> {url}")

        driver.get(url)
        time.sleep(5)  # Wait for page to load

        # Grab job URLs
        job_elements = driver.find_elements(By.CSS_SELECTOR, "h3.imt-3[data-url]")

        new_urls_this_page = 0
        for job in job_elements:
            job_url = job.get_attribute("data-url")
            if job_url:
                if job_url not in all_urls:
                    all_urls.add(job_url)
                    new_urls_this_page += 1
                    print(f"[+] New job URL: {job_url}")
                else:
                    print(f"[-] Duplicate: {job_url}")

        print(f"✅ Page {page} - Collected: {new_urls_this_page} new job URLs")

        # Optional: Save after each page to reduce risk of data loss
        with open(new_file_path, "w", encoding="utf-8") as file:
            for url in sorted(all_urls):
                file.write(url + "\n")
        print(f"💾 Intermediate save after page {page} -> Total: {len(all_urls)} URLs")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    driver.quit()
    print("🧹 Driver closed.")

# === Final save (just in case) ===
os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
with open(new_file_path, "w", encoding="utf-8") as file:
    for url in sorted(all_urls):
        file.write(url + "\n")
print(f"\n✅ Final save completed: {len(all_urls)} total job URLs saved to {new_file_path}")
