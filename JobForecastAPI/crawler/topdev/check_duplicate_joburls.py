import os
from collections import Counter

# File path
file_path = r"D:\SANG\Do An Tot Nghiep\crawl-data\data\data_itviec\itviec_jobUrls_2.txt"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    # Read all URLs from the file
    with open(file_path, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file]

    # Count occurrences of each URL
    url_counts = Counter(urls)

    # Find duplicate URLs
    duplicates = {url: count for url, count in url_counts.items() if count > 1}

    # Print results
    if duplicates:
        print(f"Found {len(duplicates)} duplicate URLs:")
        for url, count in duplicates.items():
            print(f"{url} - Count: {count}")
    else:
        print("No duplicate URLs found.")

    # Print total duplicate count
    total_duplicates = sum(count - 1 for count in duplicates.values())
    print(f"Total duplicate entries: {total_duplicates}")
