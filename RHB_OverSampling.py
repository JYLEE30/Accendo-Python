import tkinter as tk
from tkinter import filedialog
import pandas as pd
from imblearn.over_sampling import SMOTE
from collections import Counter

# Open a file dialog to select an Excel file
def select_excel_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", "*.xlsx;*.xls")])
    return file_path

# Open a file dialog to save the Excel file
def save_excel_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(title="Save Excel File", defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    return file_path

# Main function to run the process
def main():
    file_path = select_excel_file()

    if file_path:
        try:
            # Load the Excel file into a pandas DataFrame
            data = pd.read_excel(file_path, header=0)
            print("Data loaded successfully!")
            print(data.head())  # Print the first few rows of the data

            # Separate features and target variable
            X = data.drop('is_hired', axis=1)
            y = data['is_hired']

            # Apply SMOTE
            smote = SMOTE()
            X_resampled, y_resampled = smote.fit_resample(X, y)

            # Check class balance
            print('\nOriginal dataset shape:', Counter(y))
            print('Resampled dataset shape:', Counter(y_resampled))

            # Create a DataFrame for the resampled data
            resampled_data = pd.DataFrame(X_resampled, columns=X.columns)
            resampled_data['is_hired'] = y_resampled

            # Save the resampled data to a new Excel file
            save_path = save_excel_file()
            if save_path:
                resampled_data.to_excel(save_path, index=False)
                print(f"Resampled data saved to {save_path}")
            else:
                print("No file selected for saving.")

        except Exception as e:
            print(f"Error loading file: {e}")
            return None, None
    else:
        print("No file selected.")
        return None, None

if __name__ == "__main__":
    main()