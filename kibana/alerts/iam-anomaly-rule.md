# IAM Anomaly Detection Rule

## Rule Type
Elasticsearch Query Rule

## Query
Detects IAM-related actions such as:
- CreateUser
- AttachUserPolicy
- CreateAccessKey

## Purpose
Identify unauthorized or suspicious IAM activity.

## Frequency
Runs every 1 minute.

## Outcome
Triggers alert when matching events are detected.

