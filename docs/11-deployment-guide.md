# EduLafia Deployment Guide

## Document Information

- **Version**: 1.0.0
- **Last Updated**: 2026-03-26
- **Status**: Draft
- **Purpose**: Define production deployment procedures, infrastructure setup, and operational runbooks for EduLafia

---

## Table of Contents

1. [Infrastructure Overview](#1-infrastructure-overview)
2. [AWS Architecture](#2-aws-architecture)
3. [Environment Configuration](#3-environment-configuration)
4. [CI/CD Pipeline](#4-cicd-pipeline)
5. [Database Deployment](#5-database-deployment)
6. [Application Deployment](#6-application-deployment)
7. [Monitoring and Alerting](#7-monitoring-and-alerting)
8. [Backup and Disaster Recovery](#8-backup-and-disaster-recovery)
9. [Scaling Strategy](#9-scaling-strategy)
10. [Runbooks](#10-runbooks)
11. [Implementation Checklists](#11-implementation-checklists)

---

## 1. Infrastructure Overview

### 1.1 Target Architecture

```
                         ┌─────────────────┐
                         │   CloudFront    │
                         │   (CDN + WAF)   │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │   Route 53      │
                         │   (DNS)         │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │       ALB (Load Balancer)  │
                    │       (HTTPS + Health)     │
                    └─────────────┬─────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
     ┌────────▼───────┐ ┌───────▼────────┐ ┌───────▼────────┐
     │   ECS Fargate  │ │  ECS Fargate   │ │  ECS Fargate   │
     │   (API) x2     │ │  (Worker) x1   │ │  (Sync) x1     │
     └────────┬───────┘ └───────┬────────┘ └───────┬────────┘
              │                 │                   │
     ┌────────▼─────────────────▼───────────────────▼────────┐
     │                    VPC (Private Subnets)              │
     │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐│
     │  │PostgreSQL│  │  Redis   │  │ CouchDB  │  │  S3    ││
     │  │ (RDS)    │  │(ElastiC.)│  │ (Sync)   │  │(Files) ││
     │  └──────────┘  └──────────┘  └──────────┘  └────────┘│
     └───────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Container Runtime | AWS Fargate | Latest |
| Database | PostgreSQL (RDS) | 16.x |
| Cache | Redis (ElastiCache) | 7.x |
| Sync Server | CouchDB | 3.x |
| Object Storage | S3 | - |
| CDN | CloudFront | - |
| DNS | Route 53 | - |
| Load Balancer | ALB | - |
| Secrets | AWS Secrets Manager | - |
| Monitoring | CloudWatch + Datadog | - |
| CI/CD | GitHub Actions | - |

### 1.3 Regions

| Region | Purpose |
|--------|---------|
| af-south-1 (Cape Town) | Primary - lowest latency to Nigeria |
| eu-west-1 (Ireland) | Disaster recovery / read replicas |

---

## 2. AWS Architecture

### 2.1 VPC Configuration

```
VPC: 10.0.0.0/16

Public Subnets:
  10.0.1.0/24 (af-south-1a) - ALB
  10.0.2.0/24 (af-south-1b) - ALB
  10.0.3.0/24 (af-south-1c) - NAT Gateway

Private Subnets (Application):
  10.0.10.0/24 (af-south-1a) - ECS Tasks
  10.0.11.0/24 (af-south-1b) - ECS Tasks
  10.0.12.0/24 (af-south-1c) - ECS Tasks

Private Subnets (Data):
  10.0.20.0/24 (af-south-1a) - RDS, ElastiCache
  10.0.21.0/24 (af-south-1b) - RDS, ElastiCache
  10.0.22.0/24 (af-south-1c) - RDS (standby)
```

### 2.2 Security Groups

| SG Name | Inbound | Outbound |
|---------|---------|----------|
| alb-sg | 443 (HTTPS) from 0.0.0.0/0 | 8000 to ecs-api-sg |
| ecs-api-sg | 8000 from alb-sg | 5432 to rds-sg, 6379 to redis-sg, 5984 to couchdb-sg |
| ecs-worker-sg | - | 5432 to rds-sg, 6379 to redis-sg, 443 to internet |
| rds-sg | 5432 from ecs-api-sg, ecs-worker-sg | - |
| redis-sg | 6379 from ecs-api-sg, ecs-worker-sg | - |
| couchdb-sg | 5984 from ecs-api-sg, ecs-sync-sg | - |

### 2.3 IAM Roles

| Role | Permissions |
|------|-------------|
| ecs-task-role-api | S3 (school bucket), Secrets Manager (read), KMS (decrypt), SQS (send) |
| ecs-task-role-worker | S3 (school bucket), Secrets Manager (read), KMS (decrypt), SQS (receive/delete), SES (send) |
| ecs-task-role-sync | S3 (school bucket), Secrets Manager (read), KMS (decrypt) |
| ecs-execution-role | ECR (pull), CloudWatch (logs), Secrets Manager (read) |

---

## 3. Environment Configuration

### 3.1 Environment Variables

```bash
# Application
APP_NAME=edulafia
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=<from-secrets-manager>
APP_LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql+asyncpg://<user>:<pass>@<rds-endpoint>:5432/edulafia
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=rediss://<elasticache-endpoint>:6379/0
REDIS_PASSWORD=<from-secrets-manager>

# CouchDB (Sync)
COUCHDB_URL=https://<couchdb-endpoint>:5984
COUCHDB_USER=<from-secrets-manager>
COUCHDB_PASSWORD=<from-secrets-manager>

# AWS
AWS_REGION=af-south-1
AWS_S3_BUCKET=edulafia-uploads-prod
AWS_KMS_KEY_ID=<kms-key-arn>

# External Services
TERMII_API_KEY=<from-secrets-manager>
TERMII_SENDER_ID=EduLafia
WHATSAPP_PHONE_NUMBER_ID=<from-secrets-manager>
WHATSAPP_ACCESS_TOKEN=<from-secrets-manager>
PAYSTACK_SECRET_KEY=<from-secrets-manager>
FLUTTERWAVE_SECRET_KEY=<from-secrets-manager>
REMITA_MERCHANT_ID=<from-secrets-manager>
REMITA_API_KEY=<from-secrets-manager>

# JWT
JWT_SECRET_KEY=<from-secrets-manager>
JWT_ALGORITHM=RS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (for admin notifications)
SMTP_HOST=email-smtp.af-south-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=<from-secrets-manager>
SMTP_PASSWORD=<from-secrets-manager>
```

### 3.2 Secrets Management

```bash
# Store secrets in AWS Secrets Manager
aws secretsmanager create-secret \
  --name edulafia/production/database \
  --secret-string '{"username":"edulafia","password":"<generated-password>"}'

aws secretsmanager create-secret \
  --name edulafia/production/jwt \
  --secret-string '{"secret_key":"<generated-key>"}'

aws secretsmanager create-secret \
  --name edulafia/production/redis \
  --secret-string '{"auth_token":"<generated-token>"}'

aws secretsmanager create-secret \
  --name edulafia/production/termii \
  --secret-string '{"api_key":"<termii-api-key>"}'

aws secretsmanager create-secret \
  --name edulafia/production/paystack \
  --secret_string '{"secret_key":"<paystack-secret>"}'
```

---

## 4. CI/CD Pipeline

### 4.1 Pipeline Stages

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Lint &  │──>│  Test   │──>│  Build  │──>│ Deploy  │──>│  Smoke  │
│ Typecheck│   │         │   │  Image  │   │  Staging│   │  Test   │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └────┬────┘
                                                              │
                                                    ┌─────────▼────┐
                                                    │   Deploy     │
                                                    │  Production  │
                                                    └──────────────┘
```

### 4.2 GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

env:
  AWS_REGION: af-south-1
  ECR_REPOSITORY: edulafia-api

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check app/
      - run: mypy app/
      - run: pytest --cov=app -m "not slow and not e2e"

  build-and-push:
    needs: lint-and-test
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
      - uses: aws-actions/amazon-ecr-login@v2
        id: ecr-login
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ steps.ecr-login.outputs.registry }}/${{ env.ECR_REPOSITORY }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster edulafia-staging \
            --service edulafia-api \
            --force-new-deployment \
            --task-definition edulafia-api:${{ needs.build-and-push.outputs.image_tag }}
      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster edulafia-staging \
            --services edulafia-api
      - name: Run smoke tests
        run: |
          curl -f https://api-staging.edulafia.com/health || exit 1

  deploy-production:
    needs: [build-and-push, deploy-staging]
    runs-on: ubuntu-latest
    environment: production
    if: github.event.inputs.environment == 'production' || github.ref == 'refs/heads/main'
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN_PROD }}
          aws-region: ${{ env.AWS_REGION }}
      - name: Deploy to ECS (Production)
        run: |
          aws ecs update-service \
            --cluster edulafia-prod \
            --service edulafia-api \
            --force-new-deployment
      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster edulafia-prod \
            --services edulafia-api
      - name: Run production smoke tests
        run: |
          curl -f https://api.edulafia.com/health || exit 1
```

### 4.3 Dockerfile

```dockerfile
# Backend Dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app

COPY --from=builder /install /usr/local
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 4.4 ECS Task Definition

```json
{
  "family": "edulafia-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::role/ecs-execution-role",
  "taskRoleArn": "arn:aws:iam::role/ecs-task-role-api",
  "containerDefinitions": [
    {
      "name": "edulafia-api",
      "image": "<ecr-repo>:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        { "name": "APP_ENV", "value": "production" }
      ],
      "secrets": [
        { "name": "DATABASE_URL", "valueFrom": "arn:aws:secretsmanager:secret:edulafia/production/database" },
        { "name": "JWT_SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:secret:edulafia/production/jwt" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/edulafia-api",
          "awslogs-region": "af-south-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

## 5. Database Deployment

### 5.1 RDS Configuration

```yaml
RDS PostgreSQL:
  Instance: db.r6g.large (2 vCPU, 16 GB RAM)
  Storage: 100 GB gp3, auto-scaling to 500 GB
  Multi-AZ: Yes (synchronous standby)
  Backup: Daily automated, 30-day retention
  Encryption: AES-256 (AWS KMS)
  Parameter Group:
    max_connections: 200
    shared_buffers: 4GB
    effective_cache_size: 12GB
    work_mem: 16MB
    maintenance_work_mem: 1GB
    wal_level: replica
    max_wal_senders: 5
```

### 5.2 Database Migration Strategy

```bash
# Run migrations via ECS task
aws ecs run-task \
  --cluster edulafia-prod \
  --task-definition edulafia-migrate \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-private-1"],
      "securityGroups": ["sg-ecs-api"]
    }
  }'
```

### 5.3 Migration Safety

```
Pre-migration checklist:
1. Test migration on staging with production-like data
2. Take manual snapshot before migration
3. Schedule during low-traffic window (Saturday 2-4 AM WAT)
4. Have rollback script ready
5. Monitor RDS metrics during migration

Zero-downtime migration rules:
- Never rename columns (add new, migrate data, drop old)
- Never add NOT NULL without DEFAULT
- Add indexes CONCURRENTLY
- Use batched updates for large tables
- Set statement_timeout on migrations
```

---

## 6. Application Deployment

### 6.1 Deployment Strategy

Rolling deployment with health checks:

```
1. Deploy new task definition version
2. ECS starts new tasks (1 at a time)
3. ALB health check passes on new task
4. ECS drains old tasks (30-second drain period)
5. Repeat until all tasks updated
6. If health check fails, automatic rollback
```

### 6.2 Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    checks = {}
    
    # Database check
    try:
        await db.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception:
        checks["database"] = "unhealthy"
    
    # Redis check
    try:
        await redis.ping()
        checks["redis"] = "healthy"
    except Exception:
        checks["redis"] = "unhealthy"
    
    # CouchDB check
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{COUCHDB_URL}/")
            checks["couchdb"] = "healthy" if resp.status_code == 200 else "unhealthy"
    except Exception:
        checks["couchdb"] = "unhealthy"
    
    status = "healthy" if all(v == "healthy" for v in checks.values()) else "degraded"
    status_code = 200 if status == "healthy" else 503
    
    return JSONResponse(
        status_code=status_code,
        content={"status": status, "checks": checks, "version": APP_VERSION}
    )
```

### 6.3 Frontend Deployment

```bash
# Build React app
cd frontend
npm run build

# Deploy to S3
aws s3 sync dist/ s3://edulafia-frontend-prod/ --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id $CF_DISTRIBUTION_ID \
  --paths "/*"
```

---

## 7. Monitoring and Alerting

### 7.1 CloudWatch Dashboards

| Dashboard | Metrics |
|-----------|---------|
| API Performance | Request count, latency (p50/p95/p99), error rate, 5xx count |
| Database | Connections, CPU, memory, IOPS, replication lag |
| Cache | Hit rate, evictions, connections, memory |
| ECS | CPU utilization, memory utilization, running tasks |
| Sync | Pending documents, sync errors, replication lag |

### 7.2 Alerts

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| High Error Rate | 5xx > 1% for 5 min | Critical | Page on-call |
| High Latency | p95 > 2s for 10 min | High | Slack notification |
| DB Connections | > 80% max for 5 min | High | Slack + email |
| DB CPU | > 80% for 10 min | High | Slack notification |
| ECS Task Failure | Task stopped unexpectedly | Critical | Page on-call |
| Disk Usage | > 80% | Medium | Slack notification |
| Sync Lag | > 1000 pending docs for 30 min | Medium | Slack notification |
| Certificate Expiry | < 30 days | Low | Email notification |

### 7.3 Logging

```
Log Groups:
  /ecs/edulafia-api        - API server logs
  /ecs/edulafia-worker     - Background worker logs
  /ecs/edulafia-sync       - Sync server logs
  /aws/rds/instance/edulafia/postgresql - Database logs

Log Retention: 90 days

Structured Log Format:
{
  "timestamp": "2026-03-26T10:30:00Z",
  "level": "INFO",
  "logger": "app.modules.students.service",
  "message": "Student created",
  "request_id": "uuid",
  "user_id": "uuid",
  "school_id": "uuid",
  "context": {
    "student_id": "uuid",
    "admission_number": "EDU/2026/001"
  }
}
```

---

## 8. Backup and Disaster Recovery

### 8.1 Backup Strategy

| Data | Method | Frequency | Retention | Storage |
|------|--------|-----------|-----------|---------|
| PostgreSQL | RDS automated backup | Daily | 30 days | S3 (AWS managed) |
| PostgreSQL | Manual snapshot | Before migrations | 90 days | S3 (AWS managed) |
| CouchDB | Continuous replication | Real-time | - | Replica instance |
| CouchDB | Full backup | Daily | 30 days | S3 |
| S3 Files | Cross-region replication | Real-time | - | eu-west-1 |
| Secrets | AWS Secrets Manager | Versioned | All versions | AWS managed |

### 8.2 Recovery Objectives

| Metric | Target |
|--------|--------|
| RPO (Recovery Point Objective) | 1 hour |
| RTO (Recovery Time Objective) | 4 hours |

### 8.3 Disaster Recovery Procedure

```
Scenario: Primary region (af-south-1) is unavailable

1. Assessment (0-30 min)
   - Confirm regional outage via AWS status page
   - Activate DR team communication channel
   - Assess data freshness on DR replica

2. Failover (30-60 min)
   - Promote RDS read replica in eu-west-1 to primary
   - Update Route 53 to point to eu-west-1 ALB
   - Scale up ECS tasks in eu-west-1
   - Switch CouchDB replication direction

3. Validation (60-120 min)
   - Run smoke tests against DR environment
   - Verify data integrity
   - Monitor error rates and performance

4. Communication (concurrent)
   - Notify school administrators via email
   - Update status page
   - Provide estimated restoration time

5. Failback (when primary region restored)
   - Sync data from DR to primary
   - Test primary region thoroughly
   - Switch DNS back to primary
   - Scale down DR resources
```

---

## 9. Scaling Strategy

### 9.1 Auto-Scaling Rules

```yaml
ECS Auto-Scaling:
  Min Tasks: 2
  Max Tasks: 10
  Scaling Policies:
    - Metric: CPUUtilization
      Target: 70%
      Scale-out cooldown: 300s
      Scale-in cooldown: 600s
    - Metric: MemoryUtilization
      Target: 75%
    - Metric: RequestCountPerTarget
      Target: 1000 per 5 min

RDS Auto-Scaling:
  Read Replicas: 0-3
  Scale when: CPU > 70% or connections > 150

Redis Auto-Scaling:
  Shards: 1-3
  Scale when: Memory > 70% or CPU > 70%
```

### 9.2 Capacity Planning

| Users | API Tasks | DB Instance | Redis Nodes |
|-------|-----------|-------------|-------------|
| 0-1,000 | 2 | db.r6g.large | 1 cache.r6g.large |
| 1,000-5,000 | 3 | db.r6g.xlarge | 1 cache.r6g.xlarge |
| 5,000-20,000 | 5 | db.r6g.2xlarge | 2 cache.r6g.large |
| 20,000-50,000 | 8 | db.r6g.4xlarge | 3 cache.r6g.xlarge |

---

## 10. Runbooks

### 10.1 Database Connection Exhaustion

```
Symptoms: 500 errors, "too many connections" in logs

Diagnosis:
1. Check CloudWatch RDS connections metric
2. Check ECS task logs for connection errors
3. Identify long-running queries:
   SELECT pid, now() - pg_stat_activity.query_start AS duration, query
   FROM pg_stat_activity
   WHERE state != 'idle'
   ORDER BY duration DESC;

Mitigation:
1. Terminate long-running queries:
   SELECT pg_terminate_backend(<pid>);
2. Restart ECS tasks to reset connection pools
3. If persistent, increase max_connections parameter
```

### 10.2 High Error Rate

```
Symptoms: 5xx error rate > 1%, alerts firing

Diagnosis:
1. Check /health endpoint
2. Check ECS task status
3. Check CloudWatch logs for stack traces
4. Check recent deployments

Mitigation:
1. If recent deploy caused issues, rollback:
   aws ecs update-service --cluster edulafia-prod --service edulafia-api --task-definition <previous-version>
2. If DB issue, check connection pool and queries
3. If external service down, enable circuit breaker
```

### 10.3 Sync Failures

```
Symptoms: Pending documents increasing, sync errors in logs

Diagnosis:
1. Check CouchDB health
2. Check replication logs
3. Check for conflict documents

Mitigation:
1. Restart CouchDB replication:
   curl -X POST $COUCHDB/_replicate -d '{"source":"edulafia","target":"edulafia","cancel":true}'
   curl -X POST $COUCHDB/_replicate -d '{"source":"edulafia","target":"edulafia","continuous":true}'
2. Resolve conflicts manually via admin UI
3. If data corruption, restore from backup
```

---

## 11. Implementation Checklists

### 11.1 AWS Infrastructure Setup

- [ ] Create VPC with public/private subnets across 3 AZs
- [ ] Configure security groups for all components
- [ ] Create RDS PostgreSQL instance with Multi-AZ
- [ ] Create ElastiCache Redis cluster
- [ ] Create S3 buckets for uploads and backups
- [ ] Configure CloudFront distribution
- [ ] Set up Route 53 hosted zone and records
- [ ] Create ALB with HTTPS listener
- [ ] Configure WAF rules
- [ ] Set up IAM roles and policies
- [ ] Store all secrets in Secrets Manager
- [ ] Create KMS keys for encryption

### 11.2 ECS Setup

- [ ] Create ECR repositories (api, worker, sync)
- [ ] Create ECS clusters (staging, production)
- [ ] Define task definitions for all services
- [ ] Create ECS services with auto-scaling
- [ ] Configure service discovery
- [ ] Set up CloudWatch log groups
- [ ] Configure container insights

### 11.3 CI/CD Setup

- [ ] Configure GitHub Actions secrets
- [ ] Create deploy workflows for staging and production
- [ ] Set up branch protection rules
- [ ] Configure environment approvals for production
- [ ] Set up artifact caching
- [ ] Create rollback workflow

### 11.4 Monitoring Setup

- [ ] Create CloudWatch dashboards
- [ ] Configure all alerts with SNS topics
- [ ] Set up PagerDuty integration for critical alerts
- [ ] Configure Slack webhook for notifications
- [ ] Set up log retention policies
- [ ] Create custom metrics for business KPIs

### 11.5 Backup Setup

- [ ] Configure RDS automated backups (30-day retention)
- [ ] Set up CouchDB daily backup to S3
- [ ] Configure S3 cross-region replication
- [ ] Test restore procedures
- [ ] Document recovery runbooks
- [ ] Schedule quarterly DR drills

### 11.6 DNS and SSL Setup

- [ ] Register domain (edulafia.com)
- [ ] Configure Route 53 records
- [ ] Request ACM certificates for all subdomains
- [ ] Configure ALB HTTPS listener
- [ ] Set up CloudFront with SSL
- [ ] Enable HSTS headers

---

**End of Deployment Guide**
