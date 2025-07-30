import mysql.connector
import unicodedata
import re
import random

# Cấu hình DB
HOST = 'localhost'
USER = 'root'
PASSWORD = 'tansangdut'
PORT = 3306
DATABASE = 'railway'

def get_db_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
        database=DATABASE
    )

def normalize_text(text):
    if not text:
        return ""

    # 1. Chuyển unicode về dạng không dấu
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])

    # 2. Chuyển thành chữ thường
    text = text.lower()

    # 3. Loại bỏ ký tự đặc biệt, chỉ giữ chữ, số và khoảng trắng
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # 4. Bỏ khoảng trắng thừa 2 đầu và giữa
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def main():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Lấy toàn bộ users: id và name (chuẩn hóa name)
    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()

    # Tạo dict: key = normalized name, value = user id
    user_map = {}
    for u in users:
        norm_name = normalize_text(u['name'])
        user_map[norm_name] = u['id']

    # 2. Lấy danh sách job cần cập nhật user_id (user_id is NULL or empty)
    cursor.execute("SELECT id, Company_Name FROM job_data WHERE user_id IS NULL OR user_id = ''")
    jobs = cursor.fetchall()

    # 3. Lấy danh sách user_id random để gán nếu không tìm thấy
    user_ids = [u['id'] for u in users]
    if not user_ids:
        print("Bảng users trống, không thể gán user_id.")
        return

    updated_count = 0

    for job in jobs:
        norm_company = normalize_text(job['Company_Name'])
        matched_user_id = user_map.get(norm_company)

        if matched_user_id is None:
            # Không tìm thấy user, gán user_id random
            matched_user_id = random.choice(user_ids)
        else:
            updated_count += 1

        # Cập nhật user_id cho job
        cursor.execute(
            "UPDATE job_data SET user_id = %s WHERE id = %s",
            (matched_user_id, job['id'])
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Số lượng user_id được gán đúng theo tên công ty: {updated_count}")

if __name__ == "__main__":
    main()