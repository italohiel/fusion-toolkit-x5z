import csv
import os

def export_to_csv(data, filename):
    """Export a list of dictionaries to a CSV file."""
    if not data:
        print("No data provided for CSV export.")
        return

    # Check if the first item is a dictionary to get the headers
    if not isinstance(data[0], dict):
        print("Data should be a list of dictionaries.")
        return

    # Ensure the directory exists
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully exported to {filename}")

    except Exception as e:
        print(f"Error exporting to CSV: {e}")

def import_from_csv(filename):
    """Import data from a CSV file into a list of dictionaries."""
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        return []

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
        print(f"Data successfully imported from {filename}")
        return data

    except Exception as e:
        print(f"Error importing from CSV: {e}")
        return []

# TODO: Add functions for handling specific data transformations if needed
# TODO: Consider adding support for different delimiters or file formats
