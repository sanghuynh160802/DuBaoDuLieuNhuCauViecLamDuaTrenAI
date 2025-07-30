import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import os
import time
import random

# === Load existing URLs ===
old_file_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\topdev\topdev_jobUrls.txt"
new_file_path = old_file_path

existing_urls = set()
if os.path.exists(old_file_path):
    with open(old_file_path, "r", encoding="utf-8") as file:
        existing_urls = set(line.strip() for line in file if line.strip())
    print(f"✅ Loaded {len(existing_urls)} existing URLs from {old_file_path}")
else:
    print(f"⚠️ File not found: {old_file_path}")

# === Random user-agent ===
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
]
user_agent = random.choice(user_agents)
print(f"🧠 Selected User-Agent: {user_agent}")

# === Setup browser options ===
options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument(f'--user-agent={user_agent}')

def append_new_urls(new_urls, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for url in sorted(new_urls):
            f.write(url + "\n")
    print(f"📝 Appended {len(new_urls)} new URLs to {path}")

try:
    start_collect_after = 0
    scroll_limit = 100

    print("🚀 Launching undetected Chrome browser...")
    driver = uc.Chrome(options=options)
    print("✅ Chrome initialized successfully")

    url = "https://topdev.vn/it-jobs"
    print(f"🌐 Navigating to {url}")
    driver.get(url)
    time.sleep(3)

    new_job_urls = set()
    new_found_urls_batch = set()
    scroll_count = 0

    while scroll_count < scroll_limit:
        print(f"\n🔄 Scroll {scroll_count + 1}/{scroll_limit}")

        jobs = driver.find_elements(By.CSS_SELECTOR, "ul.mt-4 li.mb-4.last\\:mb-0 a[target='_blank']")
        if not jobs:
            print("❌ No job elements found. Retrying...")
            time.sleep(5)
            jobs = driver.find_elements(By.CSS_SELECTOR, "ul.mt-4 li.mb-4.last\\:mb-0 a[target='_blank']")
            if not jobs:
                print("🛑 Still no jobs found. Exiting scroll loop.")
                break

        seen_urls_this_scroll = set()
        new_urls_this_round = 0

        if scroll_count < start_collect_after:
            print(f"⏳ Waiting to start collecting URLs. Current scroll: {scroll_count + 1}/{start_collect_after}")
        else:
            for job in jobs:
                job_url = job.get_attribute("href")
                if not job_url or job_url in seen_urls_this_scroll:
                    continue

                seen_urls_this_scroll.add(job_url)

                if job_url not in existing_urls and job_url not in new_job_urls:
                    print(f"[+] New URL: {job_url}")
                    new_job_urls.add(job_url)
                    new_found_urls_batch.add(job_url)
                    new_urls_this_round += 1

                    if len(new_found_urls_batch) >= 10:
                        append_new_urls(new_found_urls_batch, new_file_path)
                        existing_urls.update(new_found_urls_batch)
                        new_found_urls_batch.clear()
                else:
                    # Print this only once per scroll
                    print(f"[-] Duplicate URL: {job_url}")

            if new_urls_this_round == 0:
                print(f"ℹ️ No new URLs found in this scroll ({len(seen_urls_this_scroll)} unique URLs scanned).")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        scroll_count += 1

    if new_found_urls_batch:
        append_new_urls(new_found_urls_batch, new_file_path)
        existing_urls.update(new_found_urls_batch)

    driver.quit()
    print("🧹 Browser closed.")
    print(f"✅ Final save completed.")
    print(f"🆕 New URLs collected: {len(new_job_urls)}")
    print(f"📁 Total URLs saved in file: {len(existing_urls)}")

except Exception as e:
    print(f"❌ Error initializing or running browser: {e}")
