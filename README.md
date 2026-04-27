# DevOps Challenge Starter Kit

Welcome to the DevOps Engineer Take-Home Challenge! This starter kit provides you with basic services that need to be containerized, deployed, and monitored as part of the challenge.

## 📁 Project Structure

```
devops-challenge-starter-kit/
├── sample-api/              # ML Model serving API
│   ├── app.py              # Main application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Basic Dockerfile (needs optimization!)
├── preprocessing-service/   # Data preprocessing service
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml      # Basic compose file (needs enhancement!)
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🎯 What You Need to Do

This starter kit provides **basic, unoptimized** implementations. Your job is to:

### 1. **Containerization & Optimization**
- ✅ Review and optimize the Dockerfiles
- ✅ Implement multi-stage builds
- ✅ Add health checks
- ✅ Use non-root users
- ✅ Minimize image sizes

### 2. **Local Development**
- ✅ Enhance docker-compose.yml
- ✅ Add proper networking
- ✅ Configure volume management
- ✅ Add monitoring stack (Prometheus, Grafana)

### 3. **Infrastructure as Code**
- ✅ Create Kubernetes manifests
- ✅ Write Terraform/IaC files
- ✅ Define multiple environments

### 4. **CI/CD Pipeline**
- ✅ Set up automated testing
- ✅ Create build and deploy pipelines
- ✅ Implement deployment strategies

### 5. **Monitoring & Observability**
- ✅ Configure Prometheus metrics
- ✅ Create Grafana dashboards
- ✅ Set up alerting rules
- ✅ Implement distributed tracing (bonus)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local testing)
- kubectl (for Kubernetes deployment)
- Terraform (for IaC)

### Running Locally

1. **Copy environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

2. **Start services with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Test the APIs:**
   
   **ML API (Port 5000):**
   ```bash
   # Health check
   curl http://localhost:5000/health
   
   # Make a prediction
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "This is a great product!"}'
   ```
   
   **Preprocessing Service (Port 5001):**
   ```bash
   # Health check
   curl http://localhost:5001/health
   
   # Preprocess text
   curl -X POST http://localhost:5001/preprocess \
     -H "Content-Type: application/json" \
     -d '{"text": "  Clean   THIS  text!!! ", "operations": ["clean", "normalize"]}'
   ```

### Running Tests Locally

```bash
# API tests
cd sample-api
python -m pytest tests/  # You'll need to create these!

# Preprocessing tests
cd preprocessing-service
python -m pytest tests/  # You'll need to create these!
```

## 📊 Available Endpoints

### ML Model API (`:5000`)
- `GET /` - Service information
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Basic metrics
- `POST /predict` - Single prediction
- `POST /batch-predict` - Batch predictions

### Preprocessing Service (`:5001`)
- `GET /` - Service information
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Basic metrics
- `POST /preprocess` - Preprocess single text
- `POST /batch-preprocess` - Batch preprocessing

## 🔍 What We're Looking For

Your submission will be evaluated on:

1. **Production Readiness**
   - Are your containers optimized?
   - Is security considered?
   - Are proper health checks in place?

2. **Automation**
   - How much is automated vs manual?
   - Is the CI/CD pipeline complete?
   - Can infrastructure be deployed with one command?

3. **Observability**
   - Can you monitor system health?
   - Are metrics meaningful?
   - Would you be alerted to issues?

4. **Documentation**
   - Can someone else run your solution?
   - Are design decisions explained?
   - Is there operational documentation?

5. **Best Practices**
   - Is the code organized?
   - Are secrets managed properly?
   - Are resources properly limited?

## 📝 Notes

- These services are **intentionally basic**. You should enhance them!
- The Dockerfiles are **not optimized**. That's part of your task!
- There's **no monitoring** yet. You need to add it!
- The **security could be better**. Improve it!
- **Tests are missing**. You should add them!

## ⚠️ Important Reminders

- Don't commit secrets or credentials
- Document your design decisions
- Make it easy to run and test
- Think about production scenarios
- Consider failure modes

## 🎁 Bonus Ideas

If you finish early, consider:
- Adding API authentication
- Implementing rate limiting
- Setting up a service mesh
- Adding distributed tracing
- Creating a web dashboard
- Implementing chaos engineering tests
- Adding automated performance tests

## 📬 Questions?

If you have questions about the challenge, make reasonable assumptions and document them in your submission README.

Good luck! 🚀

---

**Remember:** This is your chance to show us how you think about production systems. We're more interested in your approach and decision-making than perfect execution. Document your trade-offs, explain your choices, and show us your DevOps mindset!


-------


# DevOps Challenge — Pathway AI  
Microservices Architecture with Docker, Flask, and Python

This repository contains both:
1. **Your completed implementation**, fully containerized, optimized, and production‑ready  
2. **The original Starter Kit instructions**, preserved for clarity on what the challenge expected  

The goal is to clearly show what was provided and how the final solution addresses every requirement.

---

# ============================================
# 1️⃣ PROJECT IMPLEMENTATION - with help from Copilot to generate 
# ============================================

## 📁 Project Structure

devops-challenge-starter-kit/
│
├── sample-api/                 # Main inference API
│   ├── app.py                  # Updated and corrected API logic
│   ├── requirements.txt        # Updated dependencies
│   └── Dockerfile              # Optimized multi-stage Dockerfile
│
├── preprocessing-service/      # Text preprocessing microservice
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── docker-compose.yml          # Enhanced compose file with healthchecks, networking, etc.


---

# 🚀 Services Overview

## 1. sample-api (port 5000)
The main API that:
- Receives raw text  
- Sends it to the preprocessing-service  
- Performs a dummy ML inference using NumPy  
- Returns prediction + confidence  

### Endpoints:
- `GET /health`
- `GET /ready`
- `GET /metrics`
- `POST /predict`

### Workflow:
1. Receive raw text  
2. Send to `preprocessing-service:5001/preprocess`  
3. Receive cleaned text  
4. Run dummy inference  
5. Return result  

---

## 2. preprocessing-service (port 5001)
Handles text cleaning and normalization.

### Endpoints:
- `GET /health`
- `GET /ready`
- `GET /metrics`
- `POST /preprocess`
- `POST /batch-preprocess`

### Supported operations:
- clean  
- normalize  
- remove_urls  
- remove_emails  

---

# 🐳 Docker Implementation

Both services use:

- Multi-stage builds  
- `python:3.11-slim`  
- `pip install --no-cache-dir`  
- Non-root user  
- Healthchecks  
- Minimal image footprint  
- Consistent structure  

---

# 🧩 docker-compose.yml

Includes:

### ✔ Custom network  
### ✔ Healthchecks for both services  
### ✔ `depends_on` with `service_healthy`  
### ✔ Correct port mappings  
### ✔ Isolated build contexts  

### Optional features - BUT NOT ALL ACTIVATED:
- Restart policy  
- Resource limits  
- Logging driver  
- Prometheus + Grafana stack  
- Persistent volumes  

---

# Running the Project

### 1. Build the services
```bash

docker-compose build

docker-compose up

curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \

curl http://localhost:5001/health
curl -X POST http://localhost:5001/preprocess \
  -H "Content-Type: application/json" \

  #Monitoring stack with Prometheus/Grafana is included in the repository as a next step, while the local compose file focuses on validating service integration and health checks first.
