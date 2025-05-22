import csv
import json

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as csvfile, open(json_file, 'w') as jsonfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ml_use, gcs_file_path, label = row
            json_line = {
                "imageGcsUri": gcs_file_path,
                "classificationAnnotation": {
                    "displayName": label,
                    "annotationResourceLabels": {
                        "aiplatform.googleapis.com/annotation_set_name": label,
                        "env": "prod"
                    }
                },
                "dataItemResourceLabels": {
                    "aiplatform.googleapis.com/ml_use": ml_use
                }
            }
            jsonfile.write(json.dumps(json_line) + '\n')

csv_file = "formatted_import_file.csv"  
json_file = "formatted_import_file.json" 

csv_to_json(csv_file, json_file)
