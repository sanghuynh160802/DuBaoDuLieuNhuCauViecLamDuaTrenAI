import requests
import mysql.connector
import uuid
from datetime import datetime

# Database configuration
HOST = 'localhost'
USER = 'root'
PASSWORD = 'tansangdut'
PORT = 3306
DATABASE = 'railway'

API_URL = "http://localhost:5000/api/all-jobs"

def get_db_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
        database=DATABASE
    )

def fetch_all_jobs():
    resp = requests.get(API_URL)
    resp.raise_for_status()
    return resp.json()

def normalize_company_name(name):
    # Basic normalization: lowercase, remove spaces for email and password fields
    if not name:
        return ""
    return name.strip().lower().replace(" ", "")

def create_employer_users(company_names):
    users = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for company_name in company_names:
        user_id = str(uuid.uuid4())
        name = company_name.strip()
        # Email replaced with company name + domain to form valid email
        email = f"{normalize_company_name(company_name)}@company.com"
        # Password and salt replaced with normalized company name string per your instruction
        password = normalize_company_name(company_name)
        salt = normalize_company_name(company_name)
        role = "USER"
        avatar = "http://localhost:3009/public/user_icon.png"
        age = None
        is_verified = 1
        user_type = "EMPLOYER"
        created_at = now
        updated_at = now

        users.append((
            user_id, name, email, password, salt, role, avatar,
            age, is_verified, created_at, updated_at, user_type
        ))
    return users

def insert_users_to_db(users):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO users
    (id, name, email, password, salt, role, avatar, age, isVerified, created_at, updated_at, user_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(insert_sql, users)
        conn.commit()
        print(f"✅ Inserted {cursor.rowcount} employer users into the database.")
    except Exception as e:
        print("❌ Error inserting users:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def main():
    data = fetch_all_jobs()
    # data expected to be list of job dicts
    company_names = set()
    for job in data:
        company_name = job.get("Company_Name")
        if company_name:
            company_names.add(company_name.strip())

    print(f"ℹ️ Found {len(company_names)} unique company names.")

    users = create_employer_users(company_names)
    insert_users_to_db(users)

if __name__ == "__main__":
    main()