import pandas as pd
import random

# Load the CSV file into a pandas DataFrame without header
df = pd.read_csv('raw_data.csv', header=None)

# Add column names
df.columns = ['GCS_FILE_PATH', 'LABEL']

# Define the number of rows for each category
test_rows = 7
training_rows = 200
validation_rows = 20

# Get unique labels from the LABEL column
labels = df['LABEL'].unique()

# Initialize a new column to store the parameter
df.insert(0, 'PARAMETER', '')

# Assign TEST to 7 random rows for each label
for label in labels:
    test_indices = df[df['LABEL'] == label].sample(n=min(test_rows, len(df[df['LABEL'] == label])), replace=False).index
    df.loc[test_indices, 'PARAMETER'] = 'TEST'

# Assign TRAINING to 200 random rows for each label
for label in labels:
    remaining_indices = df[(df['LABEL'] == label) & (df['PARAMETER'] == '')].index
    training_indices = df.loc[remaining_indices].sample(n=min(training_rows, len(remaining_indices)), replace=False).index
    df.loc[training_indices, 'PARAMETER'] = 'TRAINING'

# Assign VALIDATION to 20 random rows for each label
for label in labels:
    remaining_indices = df[(df['LABEL'] == label) & (df['PARAMETER'] == '')].index
    validation_indices = df.loc[remaining_indices].sample(n=min(validation_rows, len(remaining_indices)), replace=False).index
    df.loc[validation_indices, 'PARAMETER'] = 'VALIDATION'

# Remove rows where PARAMETER is not defined
df = df[df['PARAMETER'] != '']

# Save the modified DataFrame to a new CSV file
df.to_csv('formatted_import_file_limited.csv', index=False, header=False)