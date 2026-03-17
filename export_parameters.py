import adsk.core
import adsk.fusion
import adsk.cam
import csv
import os
import traceback

def export_parameters(design, output_file):
    """Export parameters of selected components to a CSV file."""
    try:
        # Ensure the output file has a .csv extension
        if not output_file.endswith('.csv'):
            output_file += '.csv'

        with open(output_file, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Component Name', 'Parameter Name', 'Value', 'Units'])

            # Loop through all components in the active design
            for component in design.allComponents:
                # Check if component has parameters
                if hasattr(component, 'parameters') and component.parameters.count > 0:
                    for param in component.parameters:
                        writer.writerow([component.name, param.name, param.expression, param.unit])

        print(f"Parameters exported successfully to {output_file}")

    except Exception as e:
        print(f"Failed to export parameters: {str(e)}")
        traceback.print_exc()  # Print the stack trace for debugging

def run(context):
    """Main entry point for the script."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Check if active document and design exist
        if not app.activeDocument or not app.activeDocument.design:
            ui.messageBox("No active design document found.")
            return
            
        design = app.activeDocument.design

        # Ask for output file path
        result, cancelled = ui.inputBox("Enter the output CSV file path:", "Export Parameters", "parameters.csv")

        if not cancelled and result:
            export_parameters(design, result)
        else:
            ui.messageBox("No file path provided. Export cancelled.")

    except Exception as e:
        if ui:
            ui.messageBox(f"Failed:\n{traceback.format_exc()}")
        else:
            print(f"Failed:\n{traceback.format_exc()}")

# TODO: Add functionality to select specific components before export
# TODO: Improve error handling and user feedback
# NOTE: This script exports parameters for all components in the design.
