import os
import csv
import concurrent.futures
from google.cloud import storage
from tqdm import tqdm

os.environ["GCLOUD_PROJECT"] = "nimble-factor-422112-t6"

# Function to upload a file to Google Cloud Storage
def upload_to_gcs(bucket_name, local_file_path, gcs_file_path):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_file_path)
        blob.upload_from_filename(local_file_path)
        return f"gs://{bucket_name}/{gcs_file_path}"
    except Exception as e:
        print(f"Error uploading {local_file_path} to {gcs_file_path}: {e}")
        return None

# Function to list files in directory and subdirectories
def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# Function to extract subfolder name from path
def get_subfolder_name(file_path):
    return os.path.basename(os.path.dirname(file_path))

# Function to upload files from subfolders to Google Cloud Storage and log details to CSV
def upload_files_and_log(directory, bucket_name, csv_file):
    file_list = list_files(directory)
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = []
            progress_bar = tqdm(total=len(file_list), unit='file')
            for file_path in file_list:
                subfolder_name = get_subfolder_name(file_path)
                gcs_file_path = f"{subfolder_name}/{os.path.basename(file_path)}"
                future = executor.submit(upload_to_gcs, bucket_name, file_path, gcs_file_path)
                futures.append((future, file_path, gcs_file_path, subfolder_name))
                if len(futures) >= 100:
                    # Wait for all uploads in this batch to complete
                    for future, file_path, gcs_file_path, subfolder_name in futures:
                        gs_file_url = future.result()
                        if gs_file_url:
                            csv_writer.writerow([gs_file_url, subfolder_name])
                        else:
                            print(f"Failed to upload {file_path}")
                        progress_bar.update(1)
                    futures = []
                    csvfile.flush()  # Flush the CSV file to ensure data is written to disk
            # Write any remaining uploads to the CSV file
            for future, file_path, gcs_file_path, subfolder_name in futures:
                gs_file_url = future.result()
                if gs_file_url:
                    csv_writer.writerow([gs_file_url, subfolder_name])
                else:
                    print(f"Failed to upload {file_path}")
                progress_bar.update(1)
            progress_bar.close()
            csvfile.flush()  # Flush the CSV file to ensure data is written to disk

directory_path = r'C:\Users\Vishal Roy\Downloads\final'
bucket_name = 'plant_disease_images'
csv_file_path = r'C:\Users\Vishal Roy\Downloads\data.csv'

upload_files_and_log(directory_path, bucket_name, csv_file_path)