import mysql.connector
from config import HOST, USER, PASSWORD, PORT, DATABASE
import pandas as pd
import unicodedata
import re
import uuid
from datetime import datetime

def get_db_connection():
    """Create and return a connection to the MySQL database."""
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
        database=DATABASE
    )

def fetch_all_job_urls():
    """Fetch all Job_URLs from the job_data table."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Job_URL FROM job_data")
        job_urls = cursor.fetchall()
        cursor.close()
        connection.close()

        # # Print each Job_URL
        # for (url,) in job_urls:
        #     print(url)

        return job_urls

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    
def fetch_all_jobs():
    try:
        connection = get_db_connection()
        query = "SELECT * FROM job_data"
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối cơ sở dữ liệu: {err}")
        return pd.DataFrame()


def insert_jobs_from_csv(csv_file_path):
    """
    Read job info from a CSV and insert into job_data table, skipping 'Giới thiệu công ty'.
    Automatically handles missing values as NULLs in the database.
    """
    try:
        # Load CSV
        df = pd.read_csv(csv_file_path)

        # Drop the column not needed in the table
        if "Giới thiệu công ty" in df.columns:
            df = df.drop(columns=["Giới thiệu công ty"])

        # Rename columns to match database fields (if necessary)
        required_columns = [
            "Company_Name", "Job", "City", "Time", "Number_Recruitment", "Sexual",
            "Profession", "Title", "Level", "Salary", "Education", "Experience",
            "Description", "Requirement", "Right", "Place", "Number_Employee",
            "Work_Way", "Deadline", "Age", "Probation_Time", "Source_Picture", "Job_URL"
        ]

        # Check for missing columns
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            print(f"❌ Missing columns in CSV: {missing}")
            return

        # Establish DB connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Use backticks for all column names to be safe
        safe_columns = [f"`{col}`" for col in required_columns]
        query = f"""
        INSERT INTO job_data ({", ".join(safe_columns)})
        VALUES ({", ".join(["%s"] * len(required_columns))})
        """

        inserted_count = 0

        for _, row in df.iterrows():
            # Replace NaN with None for MySQL
            values = tuple(
                None if pd.isna(row[col]) else row[col]
                for col in required_columns
            )
            try:
                cursor.execute(query, values)
                connection.commit()  # Commit after each successful insert
                inserted_count += 1
            except mysql.connector.Error as e:
                connection.rollback()  # Rollback on error
                print(f"⚠️ Failed to insert row (Job_URL: {row.get('Job_URL', 'N/A')}): {e}")

        cursor.close()
        connection.close()
        print(f"✅ Inserted {inserted_count} job records from {csv_file_path}")

    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def insert_job(job_info):
    """
    Insert a single job entry into the job_data table.
    Automatically handles missing values as NULLs in the database.
    """
    try:
        reset_auto_increment_to_max_id()
        # Establish DB connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Include user_id in the columns
        safe_columns = [
            "`Company_Name`", "`Job`", "`City`", "`Time`", "`Number_Recruitment`", 
            "`Sexual`", "`Profession`", "`Title`", "`Level`", "`Salary`", 
            "`Education`", "`Experience`", "`Description`", "`Requirement`", 
            "`Right`", "`Place`", "`Number_Employee`", "`Work_Way`", 
            "`Deadline`", "`Age`", "`Probation_Time`", "`Skills`", 
            "`Source_Picture`", "`Job_URL`", "`user_id`"  # ✅ Add user_id here
        ]

        query = f"""
        INSERT INTO job_data ({", ".join(safe_columns)})
        VALUES ({", ".join(["%s"] * len(safe_columns))})
        """

        # Prepare values, replacing None with NULL for MySQL
        values = tuple(
            job_info.get(col[1:-1]) if job_info.get(col[1:-1]) is not None else None
            for col in safe_columns
        )

        cursor.execute(query, values)
        connection.commit()  # Commit after successful insert
        
        print(f"✅ Successfully inserted job record: {job_info['Job']}")
        
    except mysql.connector.Error as e:
        connection.rollback()  # Rollback on error
        print(f"⚠️ Failed to insert job record (Job_URL: {job_info.get('Job_URL', 'N/A')}): {e}")
    
    finally:
        cursor.close()
        connection.close()

def reset_auto_increment_to_max_id():
    """
    Automatically reset AUTO_INCREMENT on job_data table to follow the max existing ID.
    This ensures new inserts start immediately after the last existing record.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Get the next ID: MAX(id) + 1
        cursor.execute("SELECT IFNULL(MAX(id), 0) + 1 AS next_id FROM job_data")
        next_id = cursor.fetchone()[0]

        # Set AUTO_INCREMENT to this next ID
        cursor.execute(f"ALTER TABLE job_data AUTO_INCREMENT = {next_id}")
        connection.commit()

        # print(f"✅ AUTO_INCREMENT reset to {next_id}")

    except mysql.connector.Error as e:
        print(f"❌ Failed to reset AUTO_INCREMENT: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_or_create_user_id(company_name: str) -> str:
    """Tìm user_id theo company_name, nếu không có thì tạo mới user và trả về user_id."""
    norm_name = normalize_text(company_name)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Tìm user đã có với tên chuẩn hóa tương ứng
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
        user_map = {normalize_text(u['name']): u['id'] for u in users}

        if norm_name in user_map:
            return user_map[norm_name]

        # 2. Nếu không có, tạo user mới
        user_id = str(uuid.uuid4())
        name = company_name.strip()
        email = f"{normalize_text(company_name).replace(' ', '')}@company.com"
        password = normalize_text(company_name).replace(' ', '')
        salt = password
        role = "USER"
        avatar = "http://localhost:3009/public/user_icon.png"
        age = None
        is_verified = 1
        user_type = "EMPLOYER"
        created_at = now
        updated_at = now

        insert_sql = """
        INSERT INTO users
        (id, name, email, password, salt, role, avatar, age, isVerified, created_at, updated_at, user_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (
            user_id, name, email, password, salt, role, avatar,
            age, is_verified, created_at, updated_at, user_type
        ))
        conn.commit()
        return user_id

    except mysql.connector.Error as e:
        print(f"Database error in get_or_create_user_id: {e}")
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()