import csv
import os

def main():
    # Define the output CSV file path
    output_file = 'exported_parameters.csv'
    
    # Get the selected components from Fusion 360
    try:
        from utils import get_fusion_components
        components = get_fusion_components()
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        return
    except Exception as e:
        print(f"Error retrieving components: {e}")
        return

    # Check if any components were found
    if not components:
        print("No components found to export.")
        return

    # Attempt to export selected parameters to CSV
    try:
        from export_parameters import export_selected_parameters
        export_selected_parameters(components, output_file)
        print(f"Parameters exported successfully to '{output_file}'")
    except ImportError as e:
        print(f"Error importing export module: {e}")
    except Exception as e:
        print(f"Error exporting parameters: {e}")

if __name__ == "__main__":
    main()
