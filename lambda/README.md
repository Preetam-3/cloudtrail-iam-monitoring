# CloudTrail to Elasticsearch Lambda

## Overview

This AWS Lambda function is responsible for ingesting AWS CloudTrail logs from
Amazon S3 and forwarding them to Elasticsearch for indexing and analysis.

It acts as the core ingestion layer in the CloudTrail security monitoring
pipeline.

---

## Purpose

The Lambda function solves the following problem:

- CloudTrail logs are delivered to S3 as compressed JSON files
- These logs are not searchable or queryable in raw S3
- Security monitoring requires near real-time indexing into Elasticsearch

This function:
1. Is triggered automatically when new CloudTrail logs arrive in S3
2. Parses CloudTrail records
3. Pushes structured events into Elasticsearch

---

## Trigger

- **Source:** Amazon S3
- **Event type:** `ObjectCreated`
- **Bucket:** CloudTrail log bucket

Each time CloudTrail writes a new log file, this Lambda is invoked.

---

## Input

The Lambda receives an S3 event notification containing:
- Bucket name
- Object key (CloudTrail log file path)

The log file:
- Is gzip-compressed
- Contains one or more CloudTrail event records

---

## Processing Logic

High-level execution flow:

1. Lambda is triggered by S3
2. Downloads the CloudTrail log file
3. Decompresses the `.gz` file
4. Parses the JSON payload
5. Iterates over `Records[]`
6. Extracts relevant fields from each event
7. Sends events to Elasticsearch via HTTPS

The function is designed to be **stateless** and **idempotent**.

---

## Elasticsearch Indexing

- Target index pattern: `cloudtrail-*`
- Each CloudTrail record is indexed as a separate document
- Indexing is done using the Elasticsearch REST API

Authentication is handled using:
- Elasticsearch endpoint
- API key (stored as Lambda environment variable)

---

## Environment Variables

The following environment variables are required:

| Variable Name | Description |
|---------------|-------------|
| `ELASTICSEARCH_URL` | Elasticsearch cluster endpoint |
| `ELASTIC_API_KEY` | API key for authentication |
| `INDEX_NAME` | Target index name (e.g. `cloudtrail-logs`) |

---

## Permissions Required (IAM Role)

The Lambda execution role requires:

- `s3:GetObject` on the CloudTrail bucket
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`

No write access to S3 is required.

---

## Logging & Observability

- Lambda execution logs are available in CloudWatch Logs
- Logs include:
  - Invocation start/end
  - Processed S3 object path
  - Indexing success or failure

These logs are useful for debugging ingestion delays or failures.

---

## Error Handling

- Malformed records are skipped
- Network or indexing errors are logged
- Lambda execution does not fail the entire batch on a single bad record

This prevents ingestion from blocking on partial failures.

---

## Deployment Notes

- Runtime: Python 3.x
- Memory: Default (can be tuned if required)
- Timeout: Must be sufficient to process large CloudTrail files

The function is deployed manually for this project but can be automated
using Terraform or CloudFormation.

---

## Security Considerations

- Elasticsearch credentials are stored as environment variables
- No credentials are hardcoded in the source code
- HTTPS is used for all outbound communication

---

## Summary

This Lambda function is the ingestion backbone of the CloudTrail monitoring
system. It enables near real-time visibility into AWS account activity by
transforming raw CloudTrail logs into searchable Elasticsearch documents.

The design prioritizes:
- Simplicity
- Cost efficiency
- Security
- Operational clarity

