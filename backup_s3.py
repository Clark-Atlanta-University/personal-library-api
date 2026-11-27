import boto3

def backup_to_s3():
    s3 = boto3.client('s3')
    s3.upload_file('library.db', 'library-db-backup', 'library.db')
    print("Database backed up to S3")

if __name__ == "__main__":
    backup_to_s3()