import os
import pandas as pd

def merge_csv_files(directory, output_file):
    # Get all CSV files in the directory
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

    # Initialize an empty DataFrame to store the merged data
    merged_data = pd.DataFrame()

    # Iterate over each CSV file and merge its data into the DataFrame
    for file in csv_files:
        file_path = os.path.join(directory, file)
        data = pd.read_csv(file_path)
        merged_data = pd.concat([merged_data, data])

    # Write the merged data to the output file
    merged_data.to_csv(output_file, index=False)

# Usage example
directory = 'app/raw-data/csvOutputs'
output_file = 'app/processed_outputs/output.csv'
merge_csv_files(directory, output_file)