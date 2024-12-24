# test_docker_lambda_repo
repo to test docker and lambda aws

[![Deploy Lambda Function](https://github.com/danyjabban/test_docker_lambda_repo/actions/workflows/main.yml/badge.svg)](https://github.com/danyjabban/test_docker_lambda_repo/actions/workflows/main.yml)


# resources:

1.
https://medium.com/@denissedamian/step-by-step-guide-to-ci-cd-for-aws-lambda-with-docker-and-github-actions-c02a9726fd44

2.
https://www.youtube.com/watch?v=wbsbXfkv47A

3.
The error `unauthorized: access token has insufficient scopes` typically indicates an issue with your permissions or authentication when pushing a Docker image to Amazon Elastic Container Registry (ECR). This happens when the token used to authenticate does not have the required scope to push images to the target ECR repository.

### Common Causes and Fixes:

#### 1. **Missing Login to ECR**
Ensure you are logging in to the Amazon ECR registry before pushing your Docker image. The login provides a valid authentication token for the `docker push` command. 

Check that your workflow includes the following step:

```yaml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v1
```

This action generates the proper authentication token for the ECR registry.

---

#### 2. **Incorrect IAM Permissions**
The IAM role or user associated with your AWS credentials must have the necessary permissions to push images to the specified ECR repository.

Ensure the IAM entity (user or role) has the following permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:GetAuthorizationToken",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:UploadLayerPart"
      ],
      "Resource": "*"
    }
  ]
}
```

For tighter security, replace `"Resource": "*"` with the ARN of your ECR repository.

---

#### 3. **Mismatch Between Region or Repository**
Ensure:
- The `aws-region` specified in the `aws-actions/configure-aws-credentials` step matches the region of your ECR repository.
- The repository name in your workflow matches the actual ECR repository name.

---

#### 4. **Incorrect ECR Repository Name**
If the repository doesn't exist in ECR, you'll also encounter this error. Confirm that the repository has been created and is accessible.

You can create a repository with the AWS CLI:
```bash
aws ecr create-repository --repository-name my-lambda-repo --region us-east-1
```

Replace `my-lambda-repo` with your desired repository name.

---

#### Updated Workflow Example:
Here is a validated workflow to address the issue:

```yaml
name: Deploy Lambda Function

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Build Docker Image
      run: docker build -t my-lambda .

    - name: Tag Docker Image
      run: docker tag my-lambda:latest ${{ steps.login-ecr.outputs.registry }}/my-lambda-repo:latest

    - name: Push Docker Image to ECR
      run: docker push ${{ steps.login-ecr.outputs.registry }}/my-lambda-repo:latest
```

### Checklist:
1. **AWS IAM Role/User Permissions**: Ensure sufficient permissions as shown above.
2. **Region Consistency**: Verify the AWS region matches the ECR repository region.
3. **ECR Repository Exists**: Confirm the repository exists in your account.
4. **AWS Actions**: Ensure all actions are up-to-date and properly configured.

Let me know if you continue to encounter issues!
