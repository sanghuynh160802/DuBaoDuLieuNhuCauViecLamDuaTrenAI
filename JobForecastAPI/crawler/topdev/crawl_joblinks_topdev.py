from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Đường dẫn lưu dữ liệu
output_file_path = r"D:\SANG\Do An Tot Nghiep\crawl-data\data\data_topdev\topdev_jobUrls.txt"

# Khởi tạo Selenium WebDriver (chạy trình duyệt không ở chế độ headless)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Mở website
url = "https://topdev.vn/it-jobs"
driver.get(url)
time.sleep(3)  # Đợi trang load lần đầu

# Tập hợp các URL công việc
job_urls = set()  # Sử dụng set để loại bỏ trùng lặp

# Đặt giới hạn số lần cuộn
scroll_limit = 30  # Số lần cuộn tối đa
scroll_count = 0   # Đếm số lần đã cuộn

while scroll_count < scroll_limit:
    # Tìm tất cả các công việc trên trang
    jobs = driver.find_elements(By.CSS_SELECTOR, "ul.mt-4 li.mb-4.last\\:mb-0 a[target='_blank']")
    for job in jobs:
        job_url = job.get_attribute("href")
        job_urls.add(job_url)
    
    # Cuộn xuống cuối trang
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Đợi thêm 3 giây để tải dữ liệu mới
    
    # Cập nhật bộ đếm cuộn
    scroll_count += 1

    # Kiểm tra nếu không có công việc mới được tải
    new_jobs = driver.find_elements(By.CSS_SELECTOR, "ul.mt-4 li.mb-4.last\\:mb-0 a[target='_blank']")
    if len(new_jobs) == len(jobs):
        print("Không có công việc mới, dừng cuộn.")
        break  # Dừng nếu không có công việc mới

# Lưu các URL vào file
with open(output_file_path, "w", encoding="utf-8") as file:
    for job_url in job_urls:
        file.write(job_url + "\n")
        print(f"Đã lưu: {job_url}")  # Ghi log URL đã lưu

# Đóng trình duyệt
driver.quit()

print(f"Dữ liệu công việc đã được lưu thành công tại: {output_file_path}")
