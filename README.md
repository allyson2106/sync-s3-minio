# sync-s3-minio
## S3 Buckets Synchronization
This Python script synchronizes S3 buckets from a source AWS account to a destination AWS account using the boto3 and requests libraries. The script searches for S3 buckets in the source account that have a specific tag named BackupSchedule with a value of S3-Sync. It then creates the same bucket in the destination account (if it doesn't already exist) and copies all the objects from the source bucket to the destination bucket.

## Prerequisites
To use this script, you need:

Python 3.x
The boto3 and requests libraries installed
AWS credentials with sufficient permissions to access the source and destination accounts
Usage
Set your AWS credentials as environment variables or in the`~/.aws/credentials` file.
Replace `$DESTINATION_ACCESS_KEY` and `$DESTINATION_SECRET_KEY` with the appropriate values for the destination account.
Run the script.


The script starts by obtaining the account ID of the source AWS account using the EC2 metadata service. It then creates S3 client objects for both the source and destination accounts.

The script then uses the `list_buckets()` method of the source S3 client to obtain a list of all buckets in the account. It filters this list to only include buckets that have the BackupSchedule tag with a value of S3-Sync. The script then creates a list of bucket names from the filtered list.

Finally, the script iterates over the list of bucket names and creates each bucket in the destination account (if it doesn't already exist)