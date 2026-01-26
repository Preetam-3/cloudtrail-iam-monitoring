
# AWS CloudTrail IAM Monitoring with Elastic Stack

## 📌 Overview
This project detects and monitors **IAM-related security events** in AWS using **CloudTrail**, **AWS Lambda**, and the **Elastic Stack**.  
It helps identify potentially dangerous actions like:
- IAM user creation
- Policy attachment
- Access key creation
- Unusual API activity

Alerts and dashboards are built in **Kibana** for near real-time visibility.

---

## 🏗 Architecture
![Architecture](architecture/architecture-diagram.png)

**Flow:**
1. AWS CloudTrail records management events
2. Logs are delivered to an S3 bucket
3. S3 triggers an AWS Lambda function
4. Lambda parses CloudTrail logs
5. Logs are ingested into ElasticSearch
6. Kibana dashboards & alert rules visualize and detect anomalies

---

## 🔧 Tech Stack
- AWS CloudTrail
- AWS S3
- AWS Lambda (Python)
- Elastic Cloud (Elasticsearch, Kibana)
- Kibana Query Language (KQL)

---

## 🚨 Detection Use Cases
- IAM user creation (`CreateUser`)
- Policy attachment (`AttachUserPolicy`)
- Access key creation (`CreateAccessKey`)
- Log activity spikes from `logs.amazonaws.com`

---

## 📊 Dashboards
Kibana dashboards show:
- IAM API call frequency
- Event timelines
- Suspicious activity spikes

📸 See screenshots in `/screenshots`

---

## ⚠️ Alerts
Kibana alert rules trigger when:
- IAM-sensitive actions occur
- Log activity exceeds thresholds

---

## 🧪 Validation
The system was validated by:
- Creating IAM users
- Attaching policies
- Observing CloudTrail events
- Verifying ingestion in Elasticsearch
- Confirming visibility in Kibana

---

## 🧹 Cleanup
All AWS resources can be safely deleted after use to avoid costs.

---

## 👤 Author
Preetam  
B.Tech CSE | Cybersecurity & Cloud
