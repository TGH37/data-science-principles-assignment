import pandas as pd
import os

working_dir = "app/raw-data"

def extract_csv_from_xlsx(xlsx_file):
    # Read the XLSX file
    xls = pd.ExcelFile(xlsx_file)

    # Get the sheet names
    sheet_names = xls.sheet_names

    # Iterate over each sheet and extract CSV data
    for sheet_name in sheet_names:
        # Read the sheet as a DataFrame
        df = pd.read_excel(xlsx_file, sheet_name=sheet_name)

        # Extract the CSV data
        csv_data = df.to_csv(index=False)

        # Save the CSV data to a file
        csv_file = f"{working_dir}/csvOutputs/{sheet_name}.csv"
        with open(csv_file, "w") as f:
            f.write(csv_data)

        print(f"CSV data extracted from sheet '{sheet_name}' and saved to '{csv_file}'")

# Usage example
xlsx_file = os.path.join(working_dir, "Superstore Dataset.xlsx")
extract_csv_from_xlsx(xlsx_file)