### 📄 Example S3 Event to Test the Lambda Extractor Function

Use the following sample event to test the Lambda function triggered by an S3 upload:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "<your-bucket-name>"
        },
        "object": {
          "key": "<your-resume-file-path>"
        }
      }
    }
  ]
}
```
- 🔁 Replace `<your-bucket-name>` with your actual S3 bucket name and `<your-resume-file-path>` with the path of the uploaded file in the same s3 bucket.