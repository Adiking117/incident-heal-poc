# 🚨 Incident AIOps Pipeline

### Autonomous Incident Detection and Self‑Healing Infrastructure

An **end‑to‑end AIOps pipeline** that detects application failures using
observability tools and automatically remediates the problem using an
**AI agent**.

This project demonstrates how modern production systems can move toward
**self‑healing infrastructure**.

------------------------------------------------------------------------

# ⭐ What This Project Demonstrates

This project simulates a **real production incident workflow**:

1.  A microservice begins failing
2.  Prometheus detects abnormal metrics
3.  Alertmanager triggers an alert
4.  A webhook converts the alert into an event
5.  RabbitMQ streams the event
6.  An AI agent analyzes the incident
7.  The agent automatically fixes the issue by restarting the failing
    Docker container

Result:

✅ Automated incident detection\
✅ Event‑driven architecture\
✅ AI‑powered operations (AIOps)\
✅ Self‑healing systems

------------------------------------------------------------------------

# 🧠 Problem This Project Solves

In real systems:

• Services crash\
• Engineers get paged\
• Engineers manually investigate\
• Engineers restart services

Problems with this approach:

❌ Slow recovery time\
❌ Human dependency\
❌ Alert fatigue\
❌ Operational overhead

This project introduces **AI‑driven incident automation**.

The system automatically:

1.  Detects failures
2.  Generates alerts
3.  Streams events
4.  Analyzes incidents using AI
5.  Performs automatic remediation

This dramatically **reduces mean time to recovery (MTTR).**

------------------------------------------------------------------------

# 🏗️ System Architecture

    Traffic Generator
            │
            ▼
    FastAPI Payment Service
            │
            ▼
    Prometheus Metrics Endpoint
            │
            ▼
    Prometheus Alert Rule
            │
            ▼
    Alertmanager
            │
            ▼
    Webhook Receiver
            │
            ▼
    RabbitMQ Queue
            │
            ▼
    AI Incident Agent
            │
            ▼
    Docker Container Restart

------------------------------------------------------------------------

# ⚙️ Technologies Used

  Technology     Purpose
  -------------- -------------------------------
  FastAPI        Simulated microservice
  Prometheus     Monitoring and metrics
  Alertmanager   Alert routing
  RabbitMQ       Event streaming
  Docker         Containerized application
  LangChain      AI agent framework
  MCP Server     Tool interface for automation
  Groq LLM       AI reasoning model
  Python         Application logic

------------------------------------------------------------------------

# 📁 Project Structure

    Incident-AIOPS
    │
    ├── app.py
    ├── traffic.py
    │
    ├── prometheus.yml
    ├── alerts.yml
    │
    ├── alertmanager.yml
    │
    ├── alert_webhook_async.py
    │
    ├── incident_consumer_agent_async.py
    │
    ├── docker-compose.yml
    │
    └── agent
        └── server
            └── mcp_server.py

------------------------------------------------------------------------

# 🔧 System Components Explained

## 1️⃣ FastAPI Payment Service

The FastAPI application simulates a **payment microservice**.

After a few requests the service intentionally starts failing.

This increases a Prometheus metric:

    payment_errors_total

Prometheus monitors this metric.

------------------------------------------------------------------------

## 2️⃣ Prometheus Monitoring

Prometheus continuously scrapes the service metrics.

Configuration example:

    scrape_interval: 5s

Prometheus collects metrics from:

    http://localhost:5000/metrics

------------------------------------------------------------------------

## 3️⃣ Alert Rule

Prometheus evaluates rules defined in:

    alerts.yml

Example rule:

    payment_errors_total > 3

If the condition persists for **10 seconds**, the alert fires.

------------------------------------------------------------------------

## 4️⃣ Alertmanager

Alertmanager receives alerts from Prometheus.

It routes alerts to the configured receiver.

In this project:

    Webhook Receiver

------------------------------------------------------------------------

## 5️⃣ Webhook Service

The webhook service:

• Receives alerts from Alertmanager\
• Converts alerts to events\
• Publishes events to RabbitMQ

This decouples monitoring from incident automation.

------------------------------------------------------------------------

## 6️⃣ RabbitMQ Event Queue

RabbitMQ acts as an **event streaming system**.

It stores incident events in the queue:

    incidents

This allows asynchronous processing.

------------------------------------------------------------------------

## 7️⃣ AI Incident Agent

The AI agent:

1.  Consumes events from RabbitMQ
2.  Analyzes the alert payload
3.  Decides what action to take
4.  Executes remediation tools

The agent has access to the tool:

    restartdockercontainer

------------------------------------------------------------------------

## 8️⃣ Automated Remediation

If the AI agent detects a payment service failure:

It executes:

    docker restart incident-app

The system automatically recovers.

------------------------------------------------------------------------

# 🚀 Installation Guide (Step‑by‑Step)

This guide assumes basic knowledge of:

• Python\
• Docker\
• Command line

------------------------------------------------------------------------

# Step 1 --- Clone Repository

    git clone https://github.com/yourusername/incident-aiops-pipeline.git

    cd incident-aiops-pipeline

------------------------------------------------------------------------

# Step 2 --- Install Python

Download Python:

https://www.python.org/downloads/

Verify installation:

    python --version

------------------------------------------------------------------------

# Step 3 --- Create Virtual Environment

    python -m venv venv

Activate environment.

### Windows

    venv\Scripts\activate

### Linux / Mac

    source venv/bin/activate

------------------------------------------------------------------------

# Step 4 --- Install Dependencies

    pip install fastapi
    pip install uvicorn
    pip install prometheus-client
    pip install aio-pika
    pip install requests
    pip install python-dotenv
    pip install langchain
    pip install langchain-groq
    pip install langchain-mcp-adapters

------------------------------------------------------------------------

# Step 5 --- Install Docker

Install Docker from:

https://docs.docker.com/get-docker/

Verify installation:

    docker --version

------------------------------------------------------------------------

# Step 6 --- Start RabbitMQ

Run RabbitMQ using Docker:

    docker compose up -d

RabbitMQ UI:

    http://localhost:15672

Login:

    username: guest
    password: guest

------------------------------------------------------------------------

# Step 7 --- Setup Prometheus

Download Prometheus:

https://prometheus.io/download/

Extract files.

Place configuration files:

    prometheus.yml
    alerts.yml

Start Prometheus:

    prometheus.exe

Prometheus UI:

    http://localhost:9090

------------------------------------------------------------------------

# Step 8 --- Setup Alertmanager

Download Alertmanager:

https://prometheus.io/download/

Run Alertmanager:

    alertmanager.exe --config.file=alertmanager.yml

UI:

    http://localhost:9093

------------------------------------------------------------------------

# Step 9 --- Build Docker Image

    docker build -t incident-poc .

------------------------------------------------------------------------

# Step 10 --- Run Application

    docker run -p 5000:5000 --name incident-app incident-poc

------------------------------------------------------------------------

# Step 11 --- Start Webhook

    uvicorn alert_webhook_async:app --port 7000

------------------------------------------------------------------------

# Step 12 --- Start AI Consumer

    python incident_consumer_agent_async.py

------------------------------------------------------------------------

# Step 13 --- Generate Traffic

    python traffic.py

This will start generating requests.

Eventually the service fails and triggers alerts.

------------------------------------------------------------------------

# 🔄 Full Incident Flow

1️⃣ Traffic generator hits the payment API

    GET /payment

2️⃣ Service begins failing

Metric increases:

    payment_errors_total

3️⃣ Prometheus detects the issue

4️⃣ Alertmanager sends alert

5️⃣ Webhook receives alert

6️⃣ RabbitMQ publishes event

7️⃣ AI agent consumes event

8️⃣ Agent calls remediation tool

9️⃣ Docker container restarts

System recovers automatically.

------------------------------------------------------------------------

# 📊 Example Logs

Consumer output:

    🔥 INCIDENT EVENT RECEIVED

    Payload: PaymentServiceDown

    🤖 Agent calling tool: restartdockercontainer

    Container 'incident-app' restarted successfully

------------------------------------------------------------------------

# 🎯 Final Result

The pipeline successfully demonstrates:

✔ Observability‑driven automation\
✔ Event‑driven incident pipelines\
✔ AI‑powered operations\
✔ Self‑healing infrastructure

------------------------------------------------------------------------

# 🔮 Possible Improvements

Future enhancements could include:

• Slack integration\
• PagerDuty alerts\
• Kubernetes support\
• AI root cause analysis\
• Automated rollback\
• Multi‑service monitoring\
• Incident dashboards

------------------------------------------------------------------------

# 👨‍💻 Author

Aditya

AIOps \| Platform Engineering \| AI Infrastructure

------------------------------------------------------------------------

# ⭐ If you found this project useful

Give the repository a **star ⭐ on GitHub**.
