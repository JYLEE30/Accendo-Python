import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder

# Load the data
file_path = r'C:\Users\leeji\OneDrive\Desktop\Research\RHB KPI Data-KPI ALL.xlsx'
sheet_name = 'KPI-ALL'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Display the first few rows of the data
print("Original Data Sample:")
print(data.head())

# Check the class distribution
print("\nOriginal Class Distribution:")
print(data['KPI_rating'].value_counts())

# Encode the class labels
le = LabelEncoder()
data['KPI_rating'] = le.fit_transform(data['KPI_rating'])

# Separate features and target
X = data.drop('KPI_rating', axis=1)
y = data['KPI_rating']

# Identify the numeric representation of each class
class_mapping = {label: index for index, label in enumerate(le.classes_)}
print("\nClass Mapping:", class_mapping)

# Count the samples in each class
class_counts = y.value_counts()
print("\nSamples per class:", class_counts)

# Determine the number of samples for each class after SMOTE
target_samples = max(class_counts)  # We'll upsample all classes to the size of the largest class
print(f"\nTarget samples per class: {target_samples}")

# Set k_neighbors to 2 (minimum possible value) due to the small size of the 'BE' class
k_neighbors = 2

print(f"\nUsing k_neighbors = {k_neighbors}")

# Set sampling strategy to balance all classes to the target number of samples
sampling_strategy = {class_label: target_samples for class_label in class_mapping.values()}

# Apply SMOTE
smote = SMOTE(sampling_strategy=sampling_strategy, k_neighbors=k_neighbors, random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# Combine the resampled data into a new DataFrame
resampled_data = pd.DataFrame(X_res, columns=X.columns)
resampled_data['KPI_rating'] = y_res

# Decode the class labels back to original
resampled_data['KPI_rating'] = le.inverse_transform(resampled_data['KPI_rating'])

# Check the new class distribution
print("\nNew Class Distribution After SMOTE:")
print(resampled_data['KPI_rating'].value_counts())

# Save the resampled data to a new Excel file
output_file_path = r'C:\Users\leeji\OneDrive\Desktop\Research\RHB KPI Data-KPI ALL SMOTE.xlsx'
resampled_data.to_excel(output_file_path, index=False)
print(f"\nResampled data saved to: {output_file_path}")