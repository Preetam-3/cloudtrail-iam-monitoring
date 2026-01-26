# CloudTrail IAM Security Monitoring – Project Report

## 1. Project Objective

The objective of this project was to design and implement a lightweight security
monitoring pipeline for AWS IAM and CloudWatch activity using CloudTrail and the
Elastic Stack.

The system detects and visualizes sensitive AWS activity such as:
- IAM user and policy changes
- CloudWatch Logs activity
- API activity recorded by CloudTrail

This project simulates a real-world security monitoring use case relevant to
SRE and DevOps roles.

---

## 2. Architecture Overview

The monitoring pipeline follows this flow:

1. AWS CloudTrail records management events
2. CloudTrail stores logs in an S3 bucket
3. An AWS Lambda function is triggered on new log delivery
4. Lambda parses CloudTrail JSON logs
5. Parsed events are indexed into Elasticsearch (Elastic Cloud)
6. Kibana dashboards and alert rules visualize and monitor activity

This architecture avoids running any EC2 instances and relies entirely on
managed AWS services.

---

## 3. Components Used

### 3.1 AWS CloudTrail
- Enabled for management events
- Logs delivered to an S3 bucket
- Source of all AWS API activity

### 3.2 Amazon S3
- Stores CloudTrail log files
- Triggers Lambda on object creation

### 3.3 AWS Lambda
- Reads CloudTrail log files from S3
- Extracts relevant fields
- Sends events to Elasticsearch using HTTPS

### 3.4 Elastic Cloud (Elasticsearch & Kibana)
- Elasticsearch stores indexed CloudTrail events
- Kibana used for:
  - Data exploration
  - Dashboards
  - Alert rules

---

## 4. Data Ingestion Process

1. CloudTrail generates log files in JSON format
2. Files are uploaded to the S3 bucket
3. S3 triggers the Lambda function
4. Lambda:
   - Decompresses log files
   - Parses CloudTrail records
   - Pushes events to Elasticsearch index `cloudtrail-*`
5. Elasticsearch makes the data searchable in near real-time

Typical ingestion latency observed: **1–5 minutes**

---

## 5. Dashboards Created

### 5.1 IAM & CloudWatch Activity Dashboard

The main dashboard includes:
- Event count over time
- CloudTrail event types
- CloudWatch Logs activity (`eventSource: logs.amazonaws.com`)
- Time-based aggregation of AWS activity

This dashboard helps quickly identify spikes or unusual API behavior.

Dashboard export:
- `dashboards/iam-activity-dashboard.ndjson`

---

## 6. Alerts Configuration

An Elasticsearch query-based alert was created with the following logic:

- Query: CloudTrail events with
  - `eventSource: logs.amazonaws.com`
- Condition:
  - Trigger when event count is greater than 0
- Schedule:
  - Evaluated every 1 minute

This alert demonstrates how AWS activity can be continuously monitored
and flagged in near real-time.

Alert actions were intentionally kept minimal for demonstration purposes.

---

## 7. Validation & Testing

The system was validated by:
- Generating CloudTrail events via AWS Console actions
- Verifying Lambda execution in CloudWatch Logs
- Confirming indexed events in Elasticsearch
- Visualizing data in Kibana dashboards
- Observing alert executions in rule history

All components were verified independently.

---

## 8. Cost Considerations

To avoid unnecessary cost:
- Only management events were enabled
- No CloudTrail data events were enabled
- No EC2 instances were used
- Elastic Cloud free/trial tier was used

This makes the setup suitable for short-term projects and demos.

---

## 9. Limitations

- No IAM data events (e.g., S3 object-level events)
- Alerts do not notify external systems (email/Slack)
- No anomaly detection or ML-based alerting

These were excluded to keep the project simple and cost-effective.

---

## 10. Future Improvements

Possible enhancements include:
- Enabling selective data events
- Adding Slack or email alert actions
- Implementing IAM-specific anomaly detection
- Infrastructure provisioning using Terraform
- Role-based dashboards for security teams

---

## 11. Conclusion

This project demonstrates the design of a basic but realistic AWS security
monitoring pipeline using CloudTrail and the Elastic Stack.

It highlights practical skills in:
- AWS logging and monitoring
- Serverless data ingestion
- Elasticsearch indexing
- Kibana visualization and alerting

The architecture and implementation are directly applicable to SRE and
DevOps monitoring scenarios.

