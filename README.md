# Serverless Note-Taking App

This project implements a simple note-taking application using AWS Lambda, API Gateway, and DynamoDB. Infrastructure is managed with Terraform.

## Features
- Add and view notes via HTTP API
- Serverless deployment using AWS Lambda
- DynamoDB for data storage
- Secure access via IAM roles

## Deployment

```bash
cd terraform
terraform init
terraform apply
```

## Lambda Deployment

```bash
cd lambda
zip -r ../lambda.zip .
```

Upload to AWS manually or automate via Terraform (pre-set in `main.tf`).