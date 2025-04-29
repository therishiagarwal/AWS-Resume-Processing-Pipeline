### 🚀 Docker Build & Deployment for AWS Lambda via ECR

This project uses a containerized [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html) function built with Docker. Below are the steps to build, test locally, and push to AWS Elastic Container Registry (ECR).

---

### 🛠️ 1. Build the Lambda-Compatible Docker Image
```bash
docker build -f Dockerfile.lambda -t <image-name> .
```
- Replace `<image-name>` with your desired local Docker image name (e.g., `resume-uploader`).

### 🔖 2. Tag the Docker Image for ECR
```bash
docker tag <image-name>:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<repository-name>
```
- Example: `docker tag resume-uploader:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/resume-uploader`

### ☁️ 3. Push the Docker Image to AWS ECR
```bash
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<repository-name>
```
- Make sure the ECR repository exists. You can create it with:
```bash
aws ecr create-repository --repository-name <repository-name>
```

### 🧪 4. Run the Image Locally for Testing
```bash
docker run -p 8000:8000 --env-file .env <image-name>
```
- Optional: Use AWS Lambda Runtime Interface Emulator for full local emulation.
To build be push the docker file to ecr

### 🔐 Notes
- Ensure you’re authenticated to AWS ECR:

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

- Replace all placeholders like `<aws_account_id>`, `<region>`, `<repository-name>`, and `<image-name>` accordingly.




event example to test the lambda extracter function
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "resume-parser-uploads-rishi"
        },
        "object": {
          "key": "CV_RishiAgarwal.pdf"
        }
      }
    }
  ]
}
