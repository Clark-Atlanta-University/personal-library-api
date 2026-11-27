from google.cloud import storage

def backup_to_gcs():
    client = storage.Client()
    bucket = client.get_bucket('library-db-backup')
    blob = bucket.blob('library.db')
    blob.upload_from_filename('library.db')
    print("Database backed up to GCS")

if __name__ == "__main__":
    backup_to_gcs()