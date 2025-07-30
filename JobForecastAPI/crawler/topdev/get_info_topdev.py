from venv import logger
import json
import re
import random

def get_company_name_topdev(source):
    # Check if the input is a dictionary and contains the expected keys
    if isinstance(source, dict) and 'hiringOrganization' in source:
        return source['hiringOrganization'].get('name', 'None')
    return 'None'
'''
def get_title_topdev(source):

    return source.find("h1", class_="text-2xl font-bold text-black").get_text(
        " ", strip=True
    )
'''
def get_title_topdev(source):
    # Check if the input is a dictionary and contains the expected keys
    if isinstance(source, dict) and 'title' in source:
        return source['title']
    return "None"

def get_company_nationality(source):
    """
    Extracts the 'Nationality' from the page source.

    Args:
        source (BeautifulSoup): Parsed HTML page source.

    Returns:
        str: The nationality information if found, otherwise "None".
    """
    try:
        # Locate the 'Nationality' section
        nationality_header = source.find("h3", string="Nationality")
        if nationality_header:
            # Find the <p> tag that contains the nationality information
            nationality_element = nationality_header.find_next("p", class_="text-base line-clamp-2 text-neutral-600 md:text-base")
            if nationality_element:
                return nationality_element.get_text(strip=True)  # Extract the text content
        
        # Log warning if not found
        logger.warning("'Nationality' not found in the source")
        return "None"
    except Exception as e:
        logger.error(f"Error extracting 'Nationality': {e}")
        return "None"
    
def get_industry_topdev(source):
    """
    Extracts the 'Ngành nghề' (Industry) from the page source.

    Args:
        source (BeautifulSoup): Parsed HTML page source.

    Returns:
        str: The industry if found, otherwise "None".
    """
    try:
        # Locate the 'Industry' section
        element = source.find("h3", class_="text-sm font-bold text-black md:text-base", string="Industry")
        
        if element:
            # Find the <p> tag following the <h3> with the relevant text
            industry_element = element.find_next("p", class_="text-base line-clamp-2 text-neutral-600 md:text-base")
            if industry_element:
                return industry_element.get_text(strip=True)  # Extract the text content
        
        # Log warning if not found
        logger.warning("'Industry' not found in the source")
        return "None"
    except Exception as e:
        logger.error(f"Error extracting 'Industry': {e}")
        return "None"
    
def get_technologies_used(source):
    """
    Extracts the 'Các công nghệ sử dụng' (Technologies Used) from the page source.

    Args:
        source (BeautifulSoup): Parsed HTML page source.

    Returns:
        list: A list of technologies used if found, otherwise an empty list.
    """
    try:
        # Find all <span> elements within <a> tags containing the relevant technologies
        tech_elements = source.find_all("span", class_="whitespace-nowrap rounded border border-solid font-normal transition-all inline-flex items-center justify-center border-blue-light text-blue-dark bg-blue-light hover:border-blue-dark h-[1.625rem] px-2 text-xs md:h-7 md:px-2 md:text-sm")
        
        # Extract the text of each technology
        technologies = [tech.get_text(strip=True) for tech in tech_elements]
        
        if technologies:
            return technologies
        
        # Log warning if not found
        logger.warning("'Các công nghệ sử dụng' not found in the source")
        return []
    except Exception as e:
        logger.error(f"Error extracting 'Các công nghệ sử dụng': {e}")
        return []
    
def get_jobs_topdev(source):

    return source.find("h1", class_="text-2xl font-bold text-black").get_text(
        " ", strip=True
    )


def get_headquater_topdev(source):

    return source.find("div", class_="w-11/12").get_text(" ", strip=True)


def get_city_from_headquater(source):
    """
    Extracts the city name from the job location address in the job posting data.

    Args:
        source (dict): Dictionary containing job posting data.

    Returns:
        str: The city name if found, otherwise "None".
    """
    try:
        # Check if the input is a dictionary and contains the expected keys
        if isinstance(source, dict) and 'jobLocation' in source:
            job_location = source['jobLocation']
            if isinstance(job_location, dict) and 'address' in job_location:
                address = job_location['address']
                if isinstance(address, dict) and 'addressRegion' in address:
                    return address['addressRegion']
        
        # Log a warning if the address element is not found
        logger.warning("City not found in the source")
        return "None"
    except Exception as e:
        # Log the error and return "None"
        logger.error(f"Error extracting 'Thành phố': {e}")
        return "None"

def get_num_employee_topdev(source):
    """
    Extracts the number of employees from TopDev HTML source.
    
    Args:
        source (str): HTML content of the job detail page.
    
    Returns:
        str: Company size (e.g., "25-99 Employees") or "None" if not found.
    """
    for block in source.find_all("div", class_="flex flex-col ml-2"):
        title = block.find("h3")
        if title and "Company size" in title.get_text(strip=True):
            size = block.find("p")
            return size.get_text(strip=True) if size else "None"
    return "None"

'''
def get_exp_topdev(source):

    div = source.find_all("div", class_="item-card-info")

    if len(div) > 0:

        return div[0].find("a", class_="hover:text-primary-300").get_text(strip=True)

    return "None"
'''
def get_exp_topdev(source):
    """
    Extracts the 'Year of experience' from the page source.

    Args:
        source (BeautifulSoup): Parsed HTML page source.

    Returns:
        str: The experience information if found, otherwise "None".
    """
    try:
        # Locate the 'Year of experience' section
        year_experience_header = source.find("h3", string="Year of experience")
        if year_experience_header:
            # Find the <div> that contains the <a> tag with the experience information
            experience_container = year_experience_header.find_next("div")
            if experience_container:
                experience_link = experience_container.find("a", class_="text-sm font-[600] leading-none text-[#292929] hover:text-primary-300 hover:underline md:text-base")
                if experience_link:
                    return experience_link.get_text(strip=True)  # Extract the text content
        
        # Log warning if not found
        logger.warning("'Year of experience' not found in the source")
        return "None"
    except Exception as e:
        logger.error(f"Error extracting 'Year of experience': {e}")
        return "None"
'''
def get_level_topdev(source):

    div = source.find_all("div", class_="item-card-info")

    if len(div) > 1:

        return div[1].find("a", class_="hover:text-primary-300").get_text(strip=True)

    return "None"
'''
def get_level_topdev(source):
    """
    Extracts the job levels from the page source.

    Args:
        source (BeautifulSoup): Parsed HTML page source.

    Returns:
        str: The job levels as a comma-separated string if found, otherwise "None".
    """
    try:
        # Locate the div containing the job levels
        level_div = source.find("h3", string="Job Level")
        if level_div:
            levels_container = level_div.find_next("div")  # Find the next div containing the links
            if levels_container:
                # Extract all the job level links
                level_links = levels_container.find_all("a", class_="text-sm font-[600] leading-none text-[#292929] hover:text-primary-300 hover:underline md:text-base")
                # Get the text from each link and join them with a comma
                levels = [link.get_text(strip=True) for link in level_links]
                return ", ".join(levels) if levels else "None"
        
        # Log warning if not found
        logger.warning("'Job Level' not found in the source")
        return "None"
    except Exception as e:
        logger.error(f"Error extracting job levels: {e}")
        return "None"

# def get_salary_topdev(source):
#     """
#     Extracts the salary from the job posting data.

#     Args:
#         source (dict): Dictionary containing job posting data.

#     Returns:
#         str: The salary information if found, otherwise "None".
#     """
#     try:
#         # Check if the input is a dictionary and contains the expected keys
#         if isinstance(source, dict) and 'baseSalary' in source:
#             salary_data = source['baseSalary']['value']
#             return salary_data.get('value', 'None')
        
#         # Log a warning if the salary information is not found
#         logger.warning("Salary information not found in the source")
#         return "None"
#     except Exception as e:
#         # Log the error and return "None"
#         logger.error(f"Error extracting salary: {e}")
#         return "None"

def get_salary_topdev(_=None):  # Accepts optional parameter for compatibility
    try:
        # Step 1: Choose min_salary_million based on custom probabilities
        range_choice = random.choices(
            population=["low", "mid", "high"],
            weights=[70, 20, 10],  # Probabilities: low <30M, mid 30–50M, high >50M
            k=1
        )[0]

        if range_choice == "low":
            min_salary_million = random.randint(13, 29)
        elif range_choice == "mid":
            min_salary_million = random.randint(30, 49)
        else:
            min_salary_million = random.randint(50, 100)

        # Step 2: Random percentage increase (50%, 60%, or 70%)
        percent = random.choice([0.5, 0.6, 0.7])
        max_salary_million = int(min_salary_million * (1 + percent))

        # Step 3: Convert to VND
        min_salary_vnd = min_salary_million * 1_000_000
        max_salary_vnd = max_salary_million * 1_000_000

        return f"{min_salary_vnd} - {max_salary_vnd}"

    except Exception as e:
        print(f"Error generating salary: {e}")
        return "Unknown"
    
def get_edu_topdev(source):
    """
    Extracts education level from job requirement text.
    
    Args:
        source (str): HTML content of the job detail page.
    
    Returns:
        str: Education level (e.g., "University Graduate", "No degree required", or a default).
    """
    try:
        # Get job requirements text using get_requirement_topdev function
        requirement = get_requirement_topdev(source)

        # Initialize the default education level
        edu = "No degree required"  # Default value, meaning "No degree required"

        # Check for education keywords in the requirement text
        if edu == "No degree required":  # Only update if it's still the default value
            education_keywords = r"(degree|bachelor|bằng cấp|certification|tốt nghiệp|đại học|master|phd|doctoral|education)"
            if re.search(education_keywords, requirement, re.IGNORECASE):
                edu = "University Graduate"  # Update education to "University Graduate"

        return edu
    except Exception as e:
        logger.error(f"Error extracting education level: {e}")
        return "None"

'''
def get_requirement_topdev(source):

    div = source.find_all("div", class_="rounded bg-white p-4 md:px-6 md:py-4")

    res = ""

    if div:

        second_div = div[0]

        lis = second_div.find_all("ul")[1].find_all("li")

        for li in lis:

            res += li.get_text(strip=True) + "\n"

        return res

    else:

        return "None"
'''
def get_requirement_topdev(source):
    try:
        # Find the <h2> heading with the text 'Requirements'
        req_heading = source.find("h2", string="Requirements")
        if req_heading:
            # Find the next <div> that contains the requirement list
            content_div = req_heading.find_next("div", class_="prose")
            if content_div:
                # Extract all <li> tags inside this block
                lis = content_div.find_all("li")
                return "\n".join(li.get_text(strip=True) for li in lis) if lis else "None"
        return "None"
    except Exception as e:
        logger.error(f"Error extracting requirements: {e}")
        return "None"
'''
def get_description_topdev(source):

    div = source.find(
        "div",
        class_="prose mb-4 max-w-full border-b border-gray-200 pb-2 text-sm last:mb-0 last:border-0 last:pb-0 lg:text-base",
    )

    return div.get_text(strip=True)
'''
def get_description_topdev(source):
    try:
        # Find the <h2> heading with text 'Responsibilities'
        responsibilities_heading = source.find("h2", string="Responsibilities")
        if responsibilities_heading:
            # The next sibling div contains the description content
            content_div = responsibilities_heading.find_next("div", class_="prose")
            if content_div:
                return content_div.get_text(separator="\n", strip=True)
        return "None"
    except Exception as e:
        logger.error(f"Error extracting description: {e}")
        return "None"

def get_date_topdev(jobposting_data):
    """
    Extracts the 'Ngày đăng' (datePosted) from the JobPosting JSON-LD.

    Args:
        jobposting_data (dict): The JobPosting JSON-LD dictionary.

    Returns:
        str: The datePosted value if found, otherwise "None".
    """
    try:
        date = jobposting_data.get("datePosted", "").strip()
        return date if date else "None"
    except Exception as e:
        print(f"❌ Error extracting 'datePosted': {e}")
        return "None"

'''
def get_src_pic_topdev(source):

    div = source.find(
        "div", class_="flex w-[21%] flex-initial items-center justify-center bg-white"
    )

    return div.find("img").get("src")
'''
def get_src_pic_topdev(source):
    """
    Extracts the logo URL from the job posting data.

    Args:
        source (dict): Dictionary containing job posting data.

    Returns:
        str: The logo URL if found, otherwise "None".
    """
    try:
        # Check if the input is a dictionary and contains the expected keys
        if isinstance(source, dict) and 'hiringOrganization' in source:
            hiring_organization = source['hiringOrganization']
            if isinstance(hiring_organization, dict) and 'logo' in hiring_organization:
                return hiring_organization['logo']
        
        # Log a warning if the logo is not found
        logger.warning("Logo not found in the source")
        return "None"
    except Exception as e:
        logger.error(f"Error extracting logo: {e}")
        return "None"

def get_deadline_topdev(source):
    """
    Args:
        source (dict): Dictionary containing job posting data.
    Returns:
        str: The application deadline if available, otherwise "None"
    """
    return source.get('validThrough', "None")


def get_place_topdev(source):
    """
    Extracts the street address from the job location data.

    Args:
        source (dict): Dictionary containing job posting data.

    Returns:
        str: The street address if found, otherwise "None".
    """
    try:
        # Check if the input is a dictionary and contains the expected keys
        if isinstance(source, dict) and 'jobLocation' in source:
            job_location = source['jobLocation']
            if isinstance(job_location, dict) and 'address' in job_location:
                address = job_location['address']
                if isinstance(address, dict) and 'streetAddress' in address:
                    return address['streetAddress']
        
        # Log a warning if the street address is not found
        logger.warning("Street address not found in the source")
        return "None"
    except Exception as e:
        logger.error(f"Error extracting street address: {e}")
        return "None"


def get_probation_topdev():
    # Generate a random number between 0 and 1
    probability = random.random()
    
    # Return "12 months" for 70% probability, "6 months" for 30% probability
    if probability < 0.7:
        return "12 months"
    else:
        return "6 months"


def get_sex_topdev():
    return "Male" if random.random() < 0.8 else "Female"


def get_way_topdev(source):
    try:
        for div in source.find_all("div", class_="flex items-center gap-2"):
            heading = div.find("h3")
            if heading and "Job Type" in heading.get_text(strip=True):
                job_type_tag = div.find("a")
                if job_type_tag:
                    return job_type_tag.get_text(strip=True)
    except Exception as e:
        print(f"Error in get_way_topdev: {e}")
    return "None"


def get_age_topdev():
    """
    Returns a random age range of 3 consecutive numbers between 18 and 35.
    Example: '20-23', '26-29'
    """
    start = random.randint(18, 32)  # 32 + 3 = 35 max
    end = start + 3
    return f"{start}-{end}"


def get_right_topdev(source):
    try:
        # Find the <h2> heading with the text 'Benefits'
        right_heading = source.find("h2", string="Benefits")
        if right_heading:
            # Look for the closest following <ul> element that contains the benefits list
            ul = right_heading.find_next("ul")
            if ul:
                lis = ul.find_all("li")
                return "\n".join(li.get_text(strip=True) for li in lis) if lis else "None"
        return "None"
    except Exception as e:
        logger.error(f"Error extracting benefits: {e}")
        return "None"


def get_topdev_skills(jobposting_data, page_source):
    """
    Extract skills from the JobPosting JSON-LD script or, if not found, from the HTML.
    """
    try:
        if jobposting_data and 'skills' in jobposting_data:
            skills = jobposting_data['skills']
            if isinstance(skills, str):
                return skills  # If skills is a string, return it directly
            elif isinstance(skills, list):
                return ', '.join(skills)  # If skills is a list, join them with a comma
        
        # If skills are not found in the script, extract from HTML
        skill_elements = page_source.find_all('a', class_='mr-2 inline-block')
        if skill_elements:
            skills = [skill.text.strip() for skill in skill_elements]
            return ', '.join(skills)
        
        return None  # Return None if no skills are found in either script or HTML
    except Exception as e:
        print(f"Error extracting skills: {e}")
        return None