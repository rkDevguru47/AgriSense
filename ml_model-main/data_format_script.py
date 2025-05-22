import csv
import random

# Define the file paths
input_file = 'raw_data.csv'
output_file = 'formatted_import_file.csv'

# Read data from input CSV file
data = []
with open(input_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# Assign labels to rows
labels = ['training'] * len(data)
test_indices = random.sample(range(len(data)), 300)
for idx in test_indices:
    labels[idx] = 'test'
validation_indices = random.sample(list(set(range(len(data))) - set(test_indices)), int(len(data) * 0.1))
for idx in validation_indices:
    labels[idx] = 'validation'

# Write data to output CSV file with added labels and double quotes around second column
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    for label, row in zip(labels, data):
        writer.writerow([label] + row)
