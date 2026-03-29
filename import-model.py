import boto3

s3 = boto3.client("s3")

bucket = "your-bucket"
prefix = "path/to/model/"

# List and download all files
response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

for obj in response.get("Contents", []):
    key = obj["Key"]
    filename = key.split("/")[-1]
    
    s3.download_file(bucket, key, f"./model/{filename}")