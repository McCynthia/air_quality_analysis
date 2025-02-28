import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gzip

# Define the path where data is stored
DATA_DIR = '/Users/CynthiaMC/data-analysis/data_location_2178_2024'

# Function to read and combine all CSV files
def load_air_quality_data():
    all_files = []
    
    # Iterate over months
    for month in sorted(os.listdir(DATA_DIR)):
        month_path = os.path.join(DATA_DIR, month)
        
        # Skip non-directory files (like .DS_Store)
        if not os.path.isdir(month_path):
            continue
        
        # Iterate over daily compressed CSV files
        for file in sorted(os.listdir(month_path)):
            if file.endswith(".csv.gz"):
                file_path = os.path.join(month_path, file)
                
                # Read compressed CSV
                with gzip.open(file_path, 'rt') as f:
                    df = pd.read_csv(f)
                    all_files.append(df)
    
    # Combine all data into a single DataFrame
    if all_files:
        return pd.concat(all_files, ignore_index=True)
    else:
        print("No data files found.")
        return None

# Load the data
df = load_air_quality_data()

if df is not None:
    # Display basic info
    print("Data Loaded Successfully!")
    print(df.info())
    print(df.head())

    # Check available columns
    print("Columns in the dataset:", df.columns)

    # Convert 'datetime' column to datetime if available
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')  # Ensure it's a datetime object
        df.dropna(subset=['datetime'], inplace=True)  # Drop any rows where datetime is invalid
        df.set_index('datetime', inplace=True)  # Set 'datetime' as the index

    # Check unique values in 'parameter' to identify available pollutants
    pollutants = df['parameter'].unique()
    print("Unique pollutants in 'parameter' column:", pollutants)

    # Loop through each unique pollutant to create graphs
    for pollutant in pollutants:
        print(f"\nGenerating graphs for pollutant: {pollutant}")

        # Filter for the chosen pollutant
        df_pollutant = df[df['parameter'] == pollutant]

        # Visualization 1: Time-Series of the Pollutant
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_pollutant, x=df_pollutant.index, y='value')
        plt.title(f"Time-Series of {pollutant.upper()} Levels in 2024")
        plt.xlabel("Date")
        plt.ylabel(f"{pollutant.upper()} Concentration")
        plt.grid()

        # Show the time-series plot
        print(f"Displaying the {pollutant} timeseries plot...")
        plt.show()  # This will display the plot on the screen

    # Create a correlation heatmap for all pollutants
    print("\nGenerating Pollutant Correlation Heatmap...")

    # Pivot table for pollutants: We want a table where each column is a pollutant and the rows are datetime indices
    pivot_data = df.pivot_table(index=df.index, columns='parameter', values='value', aggfunc='mean')

    # Compute the correlation matrix between pollutants
    correlation_matrix = pivot_data.corr()

    # Plotting the correlation heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Correlation Between Pollutants")
    plt.show()

    print("✅ Analysis complete. Graphs displayed.")

else:
    print("❌ No data loaded. Check your file paths.")
