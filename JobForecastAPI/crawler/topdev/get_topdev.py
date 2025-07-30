from bs4 import BeautifulSoup
import requests
import logging
from time import sleep
import csv
import json
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from unidecode import unidecode
import os
import sys

# Fix import path for db_handler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db_handler import insert_job, get_or_create_user_id
from get_info_topdev import (
    get_company_name_topdev,
    get_title_topdev,
    get_deadline_topdev,
    get_num_employee_topdev,
    get_exp_topdev,
    get_level_topdev,
    get_salary_topdev,
    get_edu_topdev,
    get_requirement_topdev,
    get_description_topdev,
    get_date_topdev,
    get_src_pic_topdev,
    get_place_topdev,
    get_probation_topdev,
    get_sex_topdev,
    get_way_topdev,
    get_age_topdev,
    get_right_topdev,
    get_company_nationality,
    get_industry_topdev,
    get_city_from_headquater,
    get_topdev_skills,
)

job_urls_file = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\topdev\topdev_jobUrls.txt"
output_file_path = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\topdev\info_topdev.csv"

csv_headers = [
    "Company_Name", "Job", "City", "Time", "Number_Recruitment", "Profession",
    "Title", "Level", "Salary", "Education", "Experience", "Company Nationality",
    "Sexual", "Description", "Requirement", "Right", "Place", "Number_Employee",
    "Work_Way", "Deadline", "Age", "Probation_Time", "Source_Picture", "Job_URL"
]

API_URL = "http://localhost:5000/api/job-urls"

def fetch_existing_urls():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        job_urls = response.json()
        logging.info(f"Fetched {len(job_urls)} existing job URLs.")
        return {url.strip() for url in job_urls}
    except requests.RequestException as e:
        logging.error(f"Error fetching job URLs from API: {e}")
        return set()

def init_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    return uc.Chrome(options=options)

def remove_accents_and_non_ascii(text):
    if isinstance(text, str):
        text = unidecode(text)
        return ''.join(c for c in text if ord(c) < 128)
    return text

def extract_jobposting_json_ld(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//script[@type='application/ld+json']"))
        )
        script_elements = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")

        for idx, script in enumerate(script_elements):
            content = script.get_attribute('innerHTML').strip()
            try:
                data = json.loads(content)
                if isinstance(data, dict) and data.get('@type') == 'JobPosting':
                    return data
            except json.JSONDecodeError as je:
                print(f"⚠️ JSON decode error in script {idx + 1}: {je}")
    except Exception as e:
        print(f"❌ JSON-LD Extraction Error: {e}")
    return None

def get_profile_info_topdev(driver, url):
    try:
        driver.get(url)
        sleep(2)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        jobposting_data = extract_jobposting_json_ld(driver)
        if not jobposting_data:
            print("⚠️ No JobPosting data found, fallback to BS4 parsing.")
            return []

        company_name = get_company_name_topdev(jobposting_data)
        job = get_title_topdev(jobposting_data)
        city = get_city_from_headquater(jobposting_data)
        date = get_date_topdev(jobposting_data)
        deadline = get_deadline_topdev(jobposting_data)
        industry = get_industry_topdev(page_source)
        num_of_recruitment = 1
        title = get_title_topdev(jobposting_data)
        level = get_level_topdev(page_source)
        salary = get_salary_topdev()
        src_pic = get_src_pic_topdev(jobposting_data)
        exp_year = get_exp_topdev(page_source)
        nationality = get_company_nationality(page_source)
        sex = get_sex_topdev()
        description = get_description_topdev(page_source)
        requirement = get_requirement_topdev(page_source)
        right = get_right_topdev(page_source)
        place = get_place_topdev(jobposting_data)
        way = get_way_topdev(page_source)
        age = get_age_topdev()
        probation = get_probation_topdev()
        num_of_employee = get_num_employee_topdev(page_source)
        edu = get_edu_topdev(page_source)
        skills = get_topdev_skills(jobposting_data, page_source)

        raw_data = [
            company_name, job, city, date, num_of_recruitment, industry, title, level, salary, edu, exp_year,
            nationality, sex, description, requirement, right, place, num_of_employee, way, deadline,
            age, probation, skills, src_pic, url,
        ]

        cleaned_data = [remove_accents_and_non_ascii(field) for field in raw_data]
        return cleaned_data

    except Exception as e:
        print(f"Error occurred while scraping data from {url}: {e}")
        return []

def get_job_topdev(driver):
    try:
        existing_urls = fetch_existing_urls()

        with open(job_urls_file, "r", encoding="utf-8") as f:
            job_urls = [line.strip() for line in f.readlines()]

        data = []

        with open(output_file_path, "w", newline='', encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers)

            for url in job_urls:
                if url in existing_urls:
                    print(f"⏩ Skipped (already exists): {url}")
                    continue

                info = get_profile_info_topdev(driver, url)
                if info:
                    writer.writerow(info)
                    data.append(info)

                    company_name = info[0]
                    user_id = get_or_create_user_id(company_name)

                    job_info = {
                        "Company_Name": info[0],
                        "Job": info[1],
                        "City": info[2],
                        "Time": info[3],
                        "Number_Recruitment": info[4],
                        "Profession": info[5],
                        "Title": info[6],
                        "Level": info[7],
                        "Salary": info[8],
                        "Education": info[9],
                        "Experience": info[10],
                        "Company Nationality": info[11],
                        "Sexual": info[12],
                        "Description": info[13],
                        "Requirement": info[14],
                        "Right": info[15],
                        "Place": info[16],
                        "Number_Employee": info[17],
                        "Work_Way": info[18],
                        "Deadline": info[19],
                        "Age": info[20],
                        "Probation_Time": info[21],
                        "Skills": info[22],
                        "Source_Picture": info[23],
                        "Job_URL": url,
                        "user_id": user_id  # ✅ Add user_id here
                    }

                    insert_job(job_info)
                    print(f"✅ Saved job info to Database: {job_info}")

        return data

    except Exception as e:
        print(f"❌ Error occurred while getting data from Topdev: {e}")
        return []

if __name__ == "__main__":
    driver = None
    try:
        driver = init_driver()
        get_job_topdev(driver)
    finally:
        if driver:
            driver.quit()
            print("Driver closed.")
