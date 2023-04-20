import boto3
import requests

# Obtém o ID da conta a partir dos metadados da EC2
response = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
instance_identity = response.json()
source_account_id = instance_identity["accountId"]

# Cria os clients do S3 na conta de origem e destino
source_s3 = boto3.client("s3")
destination_s3 = boto3.client("s3",
                    aws_access_key_id=["$DESTINATION_ACCESS_KEY"],
                    aws_secret_access_key=["$DESTINATION_SECRET_KEY"])

# Lista os buckets S3 com a tag "BackupSchedule" com o valor "S3-Sync" na conta de origem
buckets = [bucket["Name"] for bucket in source_s3.list_buckets()["Buckets"]
           if "BackupSchedule" in [tag["Key"] for tag in source_s3.get_bucket_tagging(Bucket=bucket["Name"])["TagSet"]]
           and [tag["Value"] for tag in source_s3.get_bucket_tagging(Bucket=bucket["Name"])["TagSet"]][
               [tag["Key"] for tag in source_s3.get_bucket_tagging(Bucket=bucket["Name"])["TagSet"]].index("BackupSchedule")
           ] == "S3-Sync"]

# Sincroniza cada bucket com o mesmo nome na conta de destino
for bucket in buckets:
    # Cria o bucket na conta de destino caso não exista
    if not [b["Name"] for b in destination_s3.list_buckets()["Buckets"]].__contains__(bucket):
        destination_s3.create_bucket(Bucket=bucket)

    source_s3_objects = source_s3.list_objects_v2(Bucket=bucket)
    for obj in source_s3_objects["Contents"]:
        source_s3.download_file(Bucket=bucket, Key=obj["Key"], Filename=obj["Key"])
        destination_s3.upload_file(Bucket=bucket, Key=obj["Key"], Filename=obj["Key"])
        print(f"Arquivo {obj['Key']} sincronizado com sucesso.")

