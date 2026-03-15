# Incident AIOps Pipeline (Learning Notes)

This project demonstrates a complete incident detection pipeline using
modern observability tools.

It simulates a failing microservice and automatically converts failures
into streaming incident events using:

-   Prometheus
-   Prometheus Alertmanager
-   Apache Kafka
-   FastAPI
-   Docker

The pipeline demonstrates how production systems detect incidents and
send them to automation platforms.

------------------------------------------------------------------------

# 1. Architecture Overview

Traffic Generator │ ▼ FastAPI Payment Service │ ▼ Prometheus Metrics
Scraping │ ▼ Prometheus Alert Rule Evaluation │ ▼ Alertmanager Alert
Routing │ ▼ Webhook Receiver │ ▼ Kafka Topic (incidents) │ ▼ Kafka
Consumer

Final output: a Kafka event representing an incident.

------------------------------------------------------------------------

# 2. Project Components

## Payment Service

Containerized FastAPI service simulating a payment system.

Behavior: - First 3 requests succeed - From 4th request onward service
fails - Exposes Prometheus metrics

## Prometheus

Scrapes metrics every **5 seconds** and evaluates alert rules.

## Alertmanager

Receives alerts and routes them to a webhook.

## Webhook Service

Receives alerts and forwards them to Kafka.

## Kafka

Stores incidents as streaming events.

## Consumer

Reads Kafka events and prints them.

------------------------------------------------------------------------

# 3. Requirements

## Docker

Install Docker Desktop.

Check installation:

docker --version

## Python

Python 3.9+

python --version

Install dependencies:

pip install fastapi uvicorn prometheus_client kafka-python requests

## Prometheus

Download from official Prometheus website.

Run:

prometheus.exe --config.file=prometheus.yml

## Alertmanager

Download Alertmanager.

Run:

alertmanager.exe --config.file=alertmanager.yml

------------------------------------------------------------------------

# 4. Kafka Setup (Docker)

docker-compose.yml

version: '3'

services:

zookeeper: image: confluentinc/cp-zookeeper:7.5.0 container_name:
zookeeper ports: - "2181:2181" environment: ZOOKEEPER_CLIENT_PORT: 2181

kafka: image: confluentinc/cp-kafka:7.5.0 container_name: kafka
depends_on: - zookeeper ports: - "9092:9092"

    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

Start Kafka:

docker-compose up -d

------------------------------------------------------------------------

# 5. Create Kafka Topic

docker exec -it kafka bash

Create topic:

kafka-topics --create --topic incidents --bootstrap-server
localhost:9092 --partitions 1 --replication-factor 1

Verify:

kafka-topics --list --bootstrap-server localhost:9092

------------------------------------------------------------------------

# 6. Payment Service (FastAPI)

File: app.py

Key features: - Simulates payment API - Exposes `/metrics` endpoint -
Uses Prometheus counter `payment_errors_total`

------------------------------------------------------------------------

# 7. Dockerize the Service

Dockerfile:

FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install fastapi uvicorn prometheus_client

EXPOSE 5000

CMD \["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"\]

Build image:

docker build -t incident-poc .

Run:

docker run -p 5000:5000 --name incident-app incident-poc

------------------------------------------------------------------------

# 8. Prometheus Configuration

prometheus.yml

global: scrape_interval: 5s

rule_files: - "alerts.yml"

alerting: alertmanagers: - static_configs: - targets: - localhost:9093

scrape_configs:

-   job_name: "incident-poc" static_configs:
    -   targets: \["localhost:5000"\]

------------------------------------------------------------------------

# 9. Alert Rules

alerts.yml

Alert fires when payment errors exceed threshold.

Example rule:

alert: PaymentServiceDown\
expr: payment_errors_total \> 3\
for: 10s

------------------------------------------------------------------------

# 10. Alertmanager Configuration

alertmanager.yml

route: receiver: kafka-webhook

receivers:

-   name: kafka-webhook webhook_configs:
    -   url: "http://localhost:7000/alert"

------------------------------------------------------------------------

# 11. Webhook Service

Receives alert and sends it to Kafka.

Endpoint:

POST /alert

Producer sends event to **incidents** topic.

Run:

uvicorn alert_webhook:app --port 7000

------------------------------------------------------------------------

# 12. Kafka Consumer

Consumer listens to the **incidents** topic and prints events.

Run:

python incident_consumer.py

Example Output:

🔥 INCIDENT EVENT RECEIVED Topic: incidents Partition: 0 Offset: 0

------------------------------------------------------------------------

# 13. Traffic Simulation

traffic.py repeatedly calls:

http://localhost:5000/payment

After 3 successful requests, failures start triggering alerts.

------------------------------------------------------------------------

# 14. Complete Event Flow

traffic.py\
↓\
FastAPI payment endpoint\
↓\
Prometheus metric increases\
↓\
Prometheus alert rule triggers\
↓\
Alertmanager routes alert\
↓\
Webhook receives alert\
↓\
Kafka producer sends message\
↓\
Kafka topic (incidents)\
↓\
Consumer processes incident

------------------------------------------------------------------------

# 15. Example Output

Webhook logs:

Alert received: PaymentServiceDown

Consumer logs:

🔥 INCIDENT EVENT RECEIVED Payload: {alert data}

------------------------------------------------------------------------

# 16. Concepts Learned

Metrics -- applications expose monitoring data\
Monitoring -- Prometheus scrapes metrics\
Alerting -- rules detect abnormal behavior\
Routing -- Alertmanager forwards alerts\
Streaming -- Kafka stores events\
Automation -- consumers can trigger remediation logic

------------------------------------------------------------------------

# Project Outcome

This project demonstrates a **production-style observability pipeline**
used in modern cloud platforms to detect and stream incidents in real
time.
