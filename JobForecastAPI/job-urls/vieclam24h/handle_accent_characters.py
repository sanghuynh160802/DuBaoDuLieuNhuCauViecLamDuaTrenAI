import sys
import os
import pandas as pd
from unidecode import unidecode

# Fix import path for db_handler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db_handler import insert_jobs_from_csv

# File paths
input_file = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\vieclam24h\random_sampled_jobs_vieclam24h.csv"
output_file = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\vieclam24h\random_sampled_jobs_vieclam24h_Version1.csv"

# Load CSV
df = pd.read_csv(input_file, encoding="utf-8-sig", dtype=str)

# Function to remove accents
def remove_accents(text):
    if isinstance(text, str):
        return unidecode(text)
    return text

# Apply function to all text columns
df = df.applymap(remove_accents)

# Remove non-ASCII characters
df = df.apply(lambda x: ''.join(c for c in str(x) if ord(c) < 128) if isinstance(x, str) else x)

# Save the cleaned file
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"✅ File saved successfully: {output_file}")

# Insert into MySQL
insert_jobs_from_csv(output_file)