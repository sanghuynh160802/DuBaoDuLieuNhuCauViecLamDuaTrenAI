import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from unidecode import unidecode
import csv
import random
import time
import os
from datetime import datetime, timedelta
import requests
import logging
import sys
import json
# Fix import path for db_handler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db_handler import insert_job, get_or_create_user_id

# File paths
input_file = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\itviec\itviec_jobUrls.txt"
output_file = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\itviec\itviec_jobInfo.csv"

# Levels of developers
developer_levels = ["Intern", "Fresher", "Junior", "Middle", "Senior", "Lead", "Manager"]

API_URL = "http://localhost:5000/api/job-urls"

def fetch_existing_urls():
    """Fetch existing job URLs from the MySQL database."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad responses
        job_urls = response.json()
        
        # Log the response content for debugging
        logging.info(f"Response from API: {job_urls}")

        return {url for url in job_urls}  # Focus on base URLs
    except requests.RequestException as e:
        logging.error(f"Error fetching job URLs: {e}")
        return set()

def remove_accents_and_non_ascii(text):
    """Remove accents and non-ASCII characters from text."""
    if isinstance(text, str):
        # Remove accents
        text = unidecode(text)
        # Remove non-ASCII characters
        return ''.join(c for c in text if ord(c) < 128)
    return text

# Helper function to extract text or return default
def get_element_text(driver, by, value, default=None):
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        return element.text.strip()
    except Exception as e:
        print(f"Error extracting element {value}: {e}")
        return default
    
def generate_random_salary():
    try:
        # Step 1: Choose min salary range based on weighted probability
        band_choice = random.choices(
            population=["low", "mid", "high"],
            weights=[70, 20, 10],  # 70% for low, 20% for mid, 10% for high
            k=1
        )[0]

        # Step 2: Define actual min salary based on band
        if band_choice == "low":
            min_salary_million = random.randint(13, 29)
        elif band_choice == "mid":
            min_salary_million = random.randint(30, 50)
        else:  # high
            min_salary_million = random.randint(51, 100)

        # Step 3: Randomly choose a percentage multiplier
        percentage = random.choice([0.5, 0.6, 0.7])

        # Step 4: Calculate max salary
        max_salary_million = int(min_salary_million * (1 + percentage))

        # Step 5: Convert to VND
        min_salary_vnd = min_salary_million * 1_000_000
        max_salary_vnd = max_salary_million * 1_000_000

        # Step 6: Format the salary string
        salary_range = f"{min_salary_vnd} - {max_salary_vnd}"
        return salary_range

    except Exception as e:
        print(f"Error generating salary: {e}")
        return "Unknown"

def extract_skills(driver):
    """Extract skills from JSON-LD script or fallback HTML using Selenium."""
    skills = []

    # === 1. Try extracting from JSON-LD ===
    try:
        scripts = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')
        for script in scripts:
            json_ld_content = script.get_attribute('innerHTML').strip()
            if not json_ld_content:
                continue

            try:
                json_data = json.loads(json_ld_content)
            except Exception:
                continue

            # Case 1: Direct object
            if isinstance(json_data, dict) and json_data.get("@type") == "JobPosting":
                skills_raw = json_data.get("skills") or json_data.get("skillRequirements")
                if skills_raw:
                    if isinstance(skills_raw, str):
                        skills = [s.strip() for s in skills_raw.split(",")]
                    elif isinstance(skills_raw, list):
                        skills = [s.strip() for s in skills_raw if isinstance(s, str)]
                    if skills:
                        # print(f"✅ Skills from JSON-LD: {skills}")
                        return ", ".join(skills)

            # Case 2: JSON array
            elif isinstance(json_data, list):
                for item in json_data:
                    if isinstance(item, dict) and item.get("@type") == "JobPosting":
                        skills_raw = item.get("skills") or item.get("skillRequirements")
                        if skills_raw:
                            if isinstance(skills_raw, str):
                                skills = [s.strip() for s in skills_raw.split(",")]
                            elif isinstance(skills_raw, list):
                                skills = [s.strip() for s in skills_raw if isinstance(s, str)]
                            if skills:
                                print(f"✅ Skills from JSON-LD list: {skills}")
                                return ", ".join(skills)
    except Exception as e:
        print(f"⚠️ Error extracting skills from JSON-LD: {e}")

    # === 2. Fallback to HTML parsing ===
    try:
        # Locate the wrapper div that contains the skill tags (based on "Kỹ năng:" label)
        wrapper = driver.find_element(By.XPATH, "//div[contains(@class, 'imt-2') and .//span[contains(text(), 'Kỹ năng') or contains(text(), 'Skills')]]")
        tag_elements = wrapper.find_elements(By.XPATH, ".//a/div[contains(@class, 'itag')]")
        
        for tag in tag_elements:
            skill = tag.text.strip()
            if skill:
                skills.append(skill)

        if skills:
            # print(f"✅ Skills from HTML: {skills}")
            return ", ".join(skills)

    except Exception as e:
        # print(f"⚠️ Error extracting skills from HTML: {e}")
        pass

    # Final fallback
    return "Unknown"

# Function to extract job details from a URL
def extract_job_details(driver, url):
    driver.get(url)
    time.sleep(random.uniform(5, 10))  # Random delay to mimic human behavior

    # Extract skills using the new function
    skills = extract_skills(driver)

    # Extract fields
    company_name = get_element_text(driver, By.CLASS_NAME, "employer-name", default="Unknown")
    company_name = remove_accents_and_non_ascii(company_name)

    title = get_element_text(driver, By.CSS_SELECTOR, "h1.ipt-xl-6.text-it-black", default="Unknown")
    title = remove_accents_and_non_ascii(title)

    # Debug: Log the extracted title
    if title == "Unknown":
        print(f"Debug: Title extraction failed. Default value used: {title}")
    else:
        print(f"Debug: Extracted Title: '{title}'")
    # Extract company nationality
    company_nationality = None
    try:
        nationality_element = driver.find_element(By.CSS_SELECTOR, "div.d-inline-block svg.feather-icon.align-middle + span.align-middle")
        company_nationality = nationality_element.text.strip()  # Extract text, e.g., "Japan"
        company_nationality = remove_accents_and_non_ascii(company_nationality)
    except Exception as e:
        print(f"Error extracting company nationality: {e}")
        company_nationality = "Unknown"

    # Extract company industry
    company_industry = None
    try:
        industry_element = driver.find_element(By.CSS_SELECTOR, "div.col.text-end.text-it-black.text-wrap-desktop div.d-inline-flex")
        company_industry = industry_element.text.strip()  # Extract text, e.g., "Financial Services"
        company_industry = remove_accents_and_non_ascii(company_industry)
    except Exception as e:
        print(f"Error extracting company industry: {e}")
        company_industry = "Unknown"

    # Determine level from title
    level = next((lvl for lvl in developer_levels if lvl.lower() in title.lower()), "Senior")

    # List of possible date formats
    date_formats = ["%m/%d/%Y", "%Y-%m-%d"]  # Add more formats if needed

    # Initialize variables for new fields
    deadline = None
    source_picture = None
    place = None
    right = None
    date_posted = None

    # --------------------------------------------------------------------------------------------------------------------
    # Extract additional data fields

    # Sexual
    sexual = random.choices(["Male", "Female"], weights=[80, 20], k=1)[0]

    # Description
    description = None
    try:
        description_element = driver.find_element(By.XPATH, "//div[@class='imy-5 paragraph']/h2[text()='Job description']/parent::div")
        description = description_element.text.replace("Job description", "").strip()
        description = remove_accents_and_non_ascii(description)
    except Exception as e:
        print(f"Error extracting description: {e}")
        description = "Unknown"

    # Requirement
    requirement = None
    try:
        requirement_element = driver.find_element(By.XPATH, "//div[@class='imy-5 paragraph']/h2[text()='Your skills and experience']/parent::div")
        requirement = requirement_element.text.replace("Your skills and experience", "").strip()
        requirement = remove_accents_and_non_ascii(requirement)
    except Exception as e:
        print(f"Error extracting requirement: {e}")
        requirement = "Unknown"

    # Number_Employee
    number_employee = "Unknown"
    try:
        # Using WebDriverWait for more reliable element location
        number_employee_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, 
                "//div[contains(@class, 'row') and contains(@class, 'ipy-2') and contains(@class, 'border-bottom-dashed')]"
                "/div[contains(text(), 'Company size')]/following-sibling::div[contains(@class, 'text-end')]"
            ))
        )
        
        # Get the full text including "employees" and clean up whitespace
        number_employee = number_employee_element.text.strip()
        number_employee = remove_accents_and_non_ascii(number_employee)
        
    except Exception as e:
        print(f"Error extracting number of employees: {e}")

    # Work_Way
    work_way = None
    try:
        work_way_element = driver.find_element(By.XPATH, "//div[@class='d-flex align-items-center']/span[@class='normal-text text-rich-grey ms-1']")
        work_way = work_way_element.text.strip()
        work_way = remove_accents_and_non_ascii(work_way)
    except Exception as e:
        print(f"Error extracting work way: {e}")
        work_way = "Unknown"

    # Age
    age_range = None
    start_age = random.randint(19, 32)  # Ensure start age is > 18 and allows for a range < 35
    age_range = f"{start_age}-{start_age + 3}"

    # Probation_Time
    probation_time = random.choices(["12 months", "6 months"], weights=[70, 30], k=1)[0]

    # Extract Right, Place, Deadline, Source_Picture from JSON-LD
    # --------------------------------------------------------------------------------------------------------------------
    # Extract additional data fields
    try:
        # Extract Right
        try:
            right_element = driver.find_element(
                By.XPATH,
                "//div[@class='imy-5 paragraph'][h2[text()=\"Why you'll love working here\"]]"
            )
            header = right_element.find_element(By.TAG_NAME, "h2").text.strip()
            right = right_element.text.replace(header, "").strip()
            right = remove_accents_and_non_ascii(right)
        except Exception as e:
            print(f"Error extracting Right: {e}")
            right = "Unknown"

        # Extract Place
        try:
            place_element = driver.find_element(By.XPATH, "//div[@class='d-inline-block text-dark-grey']/span[@class='normal-text text-rich-grey']")
            place = place_element.text.strip()
            place = remove_accents_and_non_ascii(place)
        except Exception as e:
            print(f"Error extracting Place: {e}")
            place = "Unknown"

        # Extract Date_posted
        try:
            time_element = driver.find_element(By.CSS_SELECTOR, "div.job-details i.far.fa-clock + span")
            date_posted = time_element.text.strip()
        except:
            date_posted = datetime.now().strftime("%d/%m/%Y")
        # Generate Deadline
        try:
            start_date = datetime.strptime(date_posted, "%d/%m/%Y")
            days_to_add = random.randint(7, 30)
            deadline_date = start_date + timedelta(days=days_to_add)
            deadline = deadline_date.strftime("%d/%m/%Y")
        except:
            deadline = None

        # Extract Source_Picture
        try:
            source_picture_element = driver.find_element(By.CSS_SELECTOR, "img.employer-logo")
            source_picture = source_picture_element.get_attribute("data-src")
        except Exception as e:
            print(f"Error extracting Source_Picture: {e}")
            source_picture = "Unknown"

    except Exception as e:
        print(f"Error in additional data fields extraction: {e}")

    # Extract years of experience and education
    exp_year = None
    edu = "Không yêu cầu bằng cấp"  # Default value for education

    try:
        # Locate all div elements with the class 'imy-5 paragraph'
        skills_sections = driver.find_elements(By.CLASS_NAME, "imy-5.paragraph")
        # print("Debug: Found", len(skills_sections), "div elements with class 'imy-5 paragraph'")

        # Filter for divs containing <h2>Your skills and experience</h2>
        target_divs = []
        for section in skills_sections:
            try:
                # Check if <h2>Your skills and experience</h2> exists inside the div
                header = section.find_element(By.TAG_NAME, "h2")
                if header.text.strip().lower() == "your skills and experience":
                    target_divs.append(section)
            except Exception:
                continue  # Skip if <h2> is not found in this div

        # print("Debug: Found", len(target_divs), "div elements containing '<h2>Your skills and experience</h2>'")

        # Process each target div
        for div_index, skills_section in enumerate(target_divs):
            # print(f"Debug: Processing div {div_index + 1}...")

            # Collect text from all <p> and <li> tags
            list_items = skills_section.find_elements(By.TAG_NAME, "li")
            paragraphs = skills_section.find_elements(By.TAG_NAME, "p")

            # Combine all text elements into a single list
            elements = list_items + paragraphs

            # Process each element
            for index, element in enumerate(elements):
                text = element.text.strip()  # Extract and clean the text
                # print(f"Debug: Processing element {index + 1}: '{text}'")

                # Check for years of experience
                if exp_year is None:  # Only extract if it hasn't been found yet
                    exp_matches = re.findall(r"(\d+)\+?\s?(?:năm|year|years)", text, re.IGNORECASE)
                    if exp_matches:
                        exp_year = int(exp_matches[0])  # Use the first match for experience years
                        # print(f"Debug: Found years of experience: {exp_year}")

                # Check for education keywords
                if edu == "Không yêu cầu bằng cấp":  # Only update if it's still the default value
                    education_keywords = r"(degree|bachelor|bằng cấp|certification|tốt nghiệp|đại học|master|phd|doctoral|education)"
                    if re.search(education_keywords, text, re.IGNORECASE):
                        edu = "University Graduate"  # Update education to "Đại học" (University-level)
                        # print(f"Debug: Found education keyword in text: '{text}'. Updated edu to '{edu}'")

                # Exit loop if both exp_year and edu are found
                if exp_year is not None and edu != "No degree required":
                    # print(f"Debug: Both exp_year and edu found. Stopping further processing for div {div_index + 1}.")
                    break

            # print(f"Debug: Final extracted values for div {div_index + 1} - exp_year: {exp_year}, edu: {edu}")

        # If no exp_year or edu was found by the end of all divs, leave as None/default
        # print(f"Final extracted values - exp_year: {exp_year}, edu: {edu}")

    except Exception as e:
        print(f"Error extracting experience or education: {e}")

    # Extract and process salary values
    salary = None
    try:
        salary = generate_random_salary()

    except Exception as e:
        # print(f"Error extracting or processing salary: {e}")
        salary = "Unknown"

    # Extract city (after the last comma)
    city = None
    try:
        city_element = driver.find_element(By.CSS_SELECTOR, "div.d-inline-block.text-dark-grey span.normal-text.text-rich-grey")
        full_address = city_element.text.strip()  # Get the full address, e.g., "24th-25th Floor, ..., Ho Chi Minh"
        if full_address and ',' in full_address:
            city = full_address.split(',')[-1].strip()  # Extract the city after the last comma
        city = remove_accents_and_non_ascii(city)
    except Exception as e:
        print(f"Error extracting city: {e}")
        city = "Unknown"

    # Return extracted data as a dictionary
    return {
        "Company_Name": company_name,
        "Job": title,
        "City": city,
        "Time": date_posted,
        "Number_Recruitment": 1,
        "Profession": company_industry,
        "Title": title,
        "Level": level,
        "Salary": salary,
        "Education": edu,
        "Experience": exp_year,
        "Company Nationality": company_nationality,
        "Job_URL": url,
        "Sexual": sexual,
        "Description": description,
        "Requirement": requirement,
        "Right": right,
        "Place": place,
        "Number_Employee": number_employee,
        "Work_Way": work_way,
        "Deadline": deadline,
        "Age": age_range,
        "Probation_Time": probation_time,
        "Skills": skills, # ADD SKILLS
        "Source_Picture": source_picture,
        "Job_URL": url,
    }

# Initialize undetected Selenium WebDriver with user profile
options = uc.ChromeOptions()
# options.add_argument('--user-data-dir=C:/Users/tansa/AppData/Local/Google/Chrome/User Data/ScrapingProfile')
options.add_argument('--headless=new')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

try:
    driver = uc.Chrome(options=options)

    # Fetch existing job URLs from the database
    existing_urls = fetch_existing_urls()
    print(f"Total existing URLs in the database: {len(existing_urls)}")

    # Specify the number of URLs to read
    n = 50  # Replace with the desired number of URLs to process

    # Read job URLs from the input file
    with open(input_file, "r", encoding="utf-8") as file:
        job_urls = [line.strip() for line in file]

    # Ensure n is less than the total number of URLs
    if n > len(job_urls):
        raise ValueError("n must be less than or equal to the total number of URLs.")

    # Select a random starting position (ensuring enough URLs remain for n)
    start_pos = random.randint(0, len(job_urls) - n)
    selected_urls = job_urls[start_pos:start_pos + n]

    print(f"Selected starting position: {start_pos}")
    print(f"Processing URLs from {start_pos} to {start_pos + n - 1}")

    # driver = uc.Chrome(options=options)

    # # Fetch existing job URLs from the database
    # existing_urls = fetch_existing_urls()
    # print(f"Total existing URLs in the database: {len(existing_urls)}")

    # # Read all job URLs from the input file
    # with open(input_file, "r", encoding="utf-8") as file:
    #     job_urls = [line.strip() for line in file]

    # selected_urls = job_urls  # Select all URLs

    # print(f"Processing all {len(selected_urls)} URLs")

    # Extract job details for each selected URL
    job_data = []
    duplicate_urls = set()
    for job_url in selected_urls:
        if job_url in existing_urls:
            duplicate_urls.add(job_url)
            print(f"Skipping already processed URL: {job_url}")
            continue
        
        print(f"Processing: {job_url}")
        try:
            job_info = extract_job_details(driver, job_url)
            user_id = get_or_create_user_id(job_info["Company_Name"])
            job_info["user_id"] = user_id
            # Insert into database
            insert_job(job_info)
            print("Debug: Insert into database", job_info)
            # Optional: Also store in memory if you still want to write to CSV later
            job_data.append(job_info)
        except Exception as e:
            print(f"Error processing {job_url}: {e}")

    # Log duplicates if any were found
    if duplicate_urls:
        print(f"Duplicate URLs found: {len(duplicate_urls)}")
        for url in duplicate_urls:
            print(f"Duplicate URL: {url}")

    # Save data to CSV if there is any new job data
    if job_data:
        with open(output_file, "w", encoding="utf-8-sig", newline="") as csvfile:
            fieldnames = [
                "Company_Name", "Job", "City", "Time", "Number_Recruitment", "Profession",
                "Title", "Level", "Salary", "Education", "Experience", "Company Nationality",
                "Sexual", "Description", "Requirement", "Right", "Place", "Number_Employee",
                "Work_Way", "Deadline", "Age", "Probation_Time", "Skills", "Source_Picture", "Job_URL", "user_id"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(job_data)

        print(f"Job information extracted and saved to {output_file}")
    else:
        print("No new job data to save.")

finally:
    # Ensure the driver quits even if an error occurs
    if 'driver' in locals():
        driver.quit()
        print("Browser session closed successfully")