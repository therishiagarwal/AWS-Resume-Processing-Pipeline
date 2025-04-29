from fastapi import FastAPI, File, UploadFile
import boto3
import os
from mangum import Mangum

app = FastAPI()

# Initialize S3 client using environment variables from Lambda
# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_IDD"),
#     aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEYY"),
#     region_name=os.environ.get("AWS_DEFAULT_REGIONN", "us-east-1")
# )

s3 = boto3.client('s3')

# Bucket name also fetched from environment variable
BUCKET_NAME = os.environ.get("BUCKET_NAME")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not BUCKET_NAME:
        return {"status": "error", "detail": "Bucket name not configured in environment variables."}
    
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
@app.get("/upload")
def upload_get_test():
    return {
        "msg" : "hello from upload"
    }

# AWS Lambda-compatible handler
handler = Mangum(app)
