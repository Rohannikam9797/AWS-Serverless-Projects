# Serverless Contact Form API

> **AWS • ap-south-1 (Mumbai) • AWS SAA-003 + CLF-02**

## 📌 Overview

A fully serverless contact form backend built on AWS.  
When a user submits a contact form, the request flows through:

**API Gateway → Lambda → DynamoDB** (stores the message) + **SES** (sends email notification)

No servers to manage. No infrastructure to maintain. 100% serverless. ✅

---

## ☁️ AWS Services Used

| Service | Name | Purpose |
|---|---|---|
| **API Gateway** | ContactFormAPI | Exposes `POST /contact` REST endpoint |
| **Lambda** | ContactFormHandler | Validates & processes form data (Python 3.11) |
| **DynamoDB** | ServerlessContactForm | Stores all contact form submissions |
| **SES** | SESSendEmailPolicy | Sends email notification on new submission |
| **IAM Role** | ContactFormLambdaRole | Grants least-privilege permissions to Lambda |
| **CloudWatch** | /aws/lambda/ContactFormHandler | Logs all Lambda executions |

---

## 🔄 Request Flow

```
User / Client (Browser / Postman)
        │
        │  HTTP POST /contact
        ▼
API Gateway (ContactFormAPI)
  REST API · Regional · ap-south-1
        │
        │  Invoke
        ▼
Lambda Function (ContactFormHandler)
  Python 3.11 · 128 MB · 10s timeout
        │
        ├──── PutItem ──────► DynamoDB (ServerlessContactForm)
        │                       Partition key: submissionId (String)
        │
        └──── SendEmail ────► SES (Email Notification)
                                    │
                                    └──── Logs ──► CloudWatch
        │
        ▼
200 OK  {"message": "Submission successful!", "submissionId": "..."}
```

---

## 🔐 IAM Role — ContactFormLambdaRole

**Policies Attached (3):**

| Policy | Type | Permission |
|---|---|---|
| `AWSLambdaBasicExecutionRole` | AWS Managed | CloudWatch Logs |
| `DynamoDBPutPolicy` | Customer Inline | `dynamodb:PutItem` on ServerlessContactForm |
| `SESSendEmailPolicy` | Customer Inline | `ses:SendEmail` on all SES resources |

**Role ARN:**
```
arn:aws:iam::accountno:role/ContactFormLambdaRole
```

---
 🗄️ DynamoDB Table

| Property | Value |
|---|---|
| **Table Name** | `ServerlessContactForm` |
| **Partition Key** | `submissionId` (String) |
| **Capacity Mode** | On-demand |
| **Table Class** | DynamoDB Standard |
| **Region** | ap-south-1 |
| **Table ARN** | `arn:aws:dynamodb:ap-south-1:YOUR_ACCOUNT_ID:table/ServerlessContactForm` |

---

⚡ Lambda Function

| Property | Value |
|---|---|
| **Function Name** | `ContactFormHandler` |
| **Runtime** | Python 3.11 |
| **Architecture** | x86_64 |
| **Memory** | 128 MB |
| **Timeout** | 10 seconds |
| **Execution Role** | ContactFormLambdaRole |
| **Function ARN** | `arn:aws:lambda:ap-south-1:YOUR_ACCOUNT_ID:function:ContactFormHandler` |

---

 🌐 API Gateway

| Property | Value |
|---|---|
| **API Name** | `ContactFormAPI` |
| **Type** | REST API |
| **Endpoint Type** | Regional |
| **Resource** | `/contact` |
| **Method** | `POST` |
| **Integration** | Lambda (ContactFormHandler) |
| **Stage** | `prod` |
| **Invoke URL** | `https://td7wi05qql.execute-api.ap-south-1.amazonaws.com/prod` |

---

 🧪 Test the API

```bash
curl -X POST https://td7wi05qql.execute-api.ap-south-1.amazonaws.com/prod/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rohan",
    "email": "rohannikam9798@gmail.com",
    "message": "My first serverless project!"
  }'
```

**Expected Response:**
```json
{
  "message": "Submission successful!",
  "submissionId": "6c838aeb-93ce-4406-8868-908918c9fa9c"
}
```

---

📁 Project Structure

```
Part1-Serverless-Contact-Form/
│
├── README.md
├── lambda/
│   └── lambda_function.py
│
├── iam/
│   ├── ContactFormLambdaRole-trust-policy.json
│   ├── DynamoDBPutPolicy.json
│   └── SESSendEmailPolicy.json
│
└── screenshots/
    ├── dynamodb/
    ├── iam/
    ├── lambda/
    ├── api-gateway/
    ├── cloudwatch/
    └── testing/
```
  ✅ Completion Checklist

- [x] DynamoDB table `ServerlessContactForm` created ✅
- [x] IAM Role `ContactFormLambdaRole` created with 3 policies ✅
- [x] Lambda function `ContactFormHandler` deployed (Python 3.11) ✅
- [x] Lambda test passed — `Executing function: succeeded` ✅
- [x] API Gateway `ContactFormAPI` created (REST, Regional) ✅
- [x] `/contact` resource + `POST` method created ✅
- [x] API deployed to `prod` stage ✅
- [x] CloudWatch log group `/aws/lambda/ContactFormHandler` active ✅
- [x] End-to-end curl test passed — 7 records saved in DynamoDB ✅
- [x] **Part 1 Complete** 🎉

---

👤 Author

  Rohan Nikam
- GitHub: [@rohan-nikam9797](https://github.com/rohan-nikam9797)
- Certification Track: AWS SAA-003 + CLF-02
- Region: ap-south-1 (Mumbai)
