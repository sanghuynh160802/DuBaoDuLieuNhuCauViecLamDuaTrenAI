# import pandas as pd
# import random

# # Input and output file paths
# input_csv = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\vieclam24h\job_info_vieclam24h.csv"
# output_csv = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\vieclam24h\random_sampled_jobs_vieclam24h.csv"

# # Read the original CSV
# df = pd.read_csv(input_csv)

# # Pick 10 random samples
# sampled_df = df.sample(n=10, random_state=42)

# # Save the sampled data to a new CSV
# sampled_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

# print(f"Exported 10 random job samples to: {output_csv}")


import pandas as pd

# Input and output file paths
input_txt = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\vieclam24h\job_urls_vieclam24h.txt"
output_txt = r"D:\SANG\Do An Tot Nghiep\WEB-THAMKHAO\JOBINFOR\JobForecastAPI\job-urls\vieclam24h\random_job_urls_vieclam24h.txt"

# Read the original TXT file (assuming one URL per line)
with open(input_txt, 'r', encoding='utf-8') as f:
    urls = f.read().splitlines()

# Pick 10 random URLs
import random
sampled_urls = random.sample(urls, 10)

# Save to a new TXT file
with open(output_txt, 'w', encoding='utf-8') as f:
    for url in sampled_urls:
        f.write(url + '\n')

print(f"Exported 10 random job URLs to: {output_txt}")
