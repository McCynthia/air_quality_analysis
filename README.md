# Air Quality Data Analysis (2024)

This project analyzes air quality data for a specific location in 2024. It consists of two main scripts: one for downloading and extracting the data from the OpenAQ S3 bucket and another for analyzing the air quality data. 

## Project Structure

The project consists of two Python files:
1. **air-data-2024.py**: Downloads and processes the air quality data from the OpenAQ S3 bucket.
2. **air_quality_analysis.py**: Analyzes the data, generates time-series plots for each pollutant, creates a correlation heatmap, and visualizes annual trends.

## Prerequisites

Before running these scripts, ensure you have the following installed:
- Python 3.x
- [AWS CLI](https://aws.amazon.com/cli/) (for `air-data-2024.py` to download data)
- Python libraries:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `gzip`
  - `subprocess`
  - `shutil`

You can install the required Python libraries using `pip`:

```bash
pip install pandas matplotlib seaborn
```

## Step 1: Download and Process Data

### Running `air-data-2024.py`

This script will:
1. Check if AWS CLI is installed and correctly configured.
2. Download air quality data from the OpenAQ S3 bucket for the specified location and year.
3. Extract the `.csv.gz` files.
4. Combine all the extracted CSV files into a single CSV.

### How to run:
```bash
python air-data-2024.py
```

**Parameters:**
- `location_id`: Change this to the location ID of your choice.
- `year`: Set this to 2024 or any year you want to analyze.

After running the script, the data will be stored in a folder named `data_location_{location_id}_{year}`.

## Step 2: Analyze the Air Quality Data

### Running `air_quality_analysis.py`

Once the data is downloaded and extracted, run the `air_quality_analysis.py` script to analyze the air quality.

This script will:
1. Load the combined CSV data.
2. Generate time-series plots for each pollutant (e.g., PM2.5, PM10, NO2).
3. Create a correlation heatmap to explore the relationships between pollutants.
4. Plot the annual trend of each pollutant, showing the overall yearly trend.

### How to run:
```bash
python air_quality_analysis.py
```

## Data Overview

The air quality data consists of the following columns:
- `datetime`: The timestamp for each air quality measurement.
- `parameter`: The type of pollutant (e.g., `PM2.5`, `PM10`, `NO2`).
- `value`: The concentration of the pollutant measured at that time.
- `location`: The geographic location where the data was recorded.

## Outputs

1. **Time-Series Plots**: For each pollutant, a plot showing its concentration over time in 2024.
2. **Annual Trend**: A plot showing the monthly average concentration of each pollutant over the year.
3. **Correlation Heatmap**: A heatmap showing the correlation between different pollutants.

## Notes
- Make sure AWS CLI is correctly set up with access to the OpenAQ S3 bucket. You can test the setup by running `aws s3 ls` from the command line.
- This project assumes the data is for a specific location in 2024. Update the `location_id` and `year` as needed.
- The data is processed in monthly chunks, so the output will contain one `.csv` file per month of data.
  
