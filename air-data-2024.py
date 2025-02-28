import os
import subprocess
import gzip
import shutil
import pandas as pd

# Set parameters
location_id = "2178"  # Change this to the correct location ID
year = 2024
output_dir = f"data_location_{location_id}_{year}"

# Step 1: Ensure AWS CLI is installed
try:
    subprocess.run(["aws", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("✅ AWS CLI is installed.")
except subprocess.CalledProcessError:
    print("❌ AWS CLI is not installed. Please install it before running this script.")
    exit(1)

# Step 2: Create data directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Step 3: Download the data from OpenAQ S3 bucket
s3_path = f"s3://openaq-data-archive/records/csv.gz/locationid={location_id}/year={year}/"
print(f"📥 Downloading data from {s3_path}...")
download_cmd = ["aws", "s3", "cp", "--no-sign-request", "--recursive", s3_path, output_dir]

try:
    subprocess.run(download_cmd, check=True)
    print("✅ Data downloaded successfully.")
except subprocess.CalledProcessError:
    print("❌ Error downloading data. Please check your AWS CLI setup.")
    exit(1)

# Step 4: Extract all .csv.gz files
csv_files = []
for file in os.listdir(output_dir):
    if file.endswith(".csv.gz"):
        gz_file_path = os.path.join(output_dir, file)
        csv_file_path = gz_file_path[:-3]  # Remove .gz extension

        # Extract .gz file
        with gzip.open(gz_file_path, "rb") as f_in:
            with open(csv_file_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        csv_files.append(csv_file_path)
        os.remove(gz_file_path)  # Remove the compressed file

print(f"✅ Extracted {len(csv_files)} files.")

# Step 5: Combine extracted CSV files into one
if csv_files:
    combined_df = pd.concat([pd.read_csv(f) for f in csv_files])
    combined_csv_path = f"{output_dir}/combined_air_quality_{location_id}_{year}.csv"
    combined_df.to_csv(combined_csv_path, index=False)
    print(f"✅ Combined CSV saved: {combined_csv_path}")
else:
    print("⚠️ No CSV files found after extraction.")

print("🎉 Process completed successfully!")
