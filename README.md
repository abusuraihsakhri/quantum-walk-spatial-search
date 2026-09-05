# Quantum Walk Spatial Search

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Quantum Walk Spatial Search is an enterprise-grade analytical platform that implements continuous-time and discrete quantum walk algorithms for graph search operations. It provides a multi-agent consensus framework with cryptographic audit trails, PHI (Protected Health Information) outbound guards, and FastAPI-based REST APIs for task evaluation and monitoring.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **Multi-Agent Consensus**: Specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) evaluate tasks and produce consensus dossiers.
- **Enrichment Suite**: Pluggable engine modules for spatial search, CTQW graph connectivity, and implementation analysis.

---

## 💻 CLI Quickstart & Usage

### Installation
```bash
pip install -e .
```

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task identifier (default: TASK-2026-001)
- `--target`: Target entity identifier (default: KEY-TARGET-01)
- `--primary`: Primary metric value, must be finite (default: 28.5)
- `--secondary`: Secondary metric value, must be finite (default: 14.2)
- `--critical`: Flag for critical escalation (default: False)
- `--status`: Status descriptor, e.g., NOMINAL, DISCORDANT (default: DISCORDANT)

### Input Data Schema (CSV Batch)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task identifier | Required |
| `target_identifier` | Target entity identifier | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary measurement value | Required |
| `is_critical_flag` | Critical escalation flag | Optional |
| `status_descriptor` | Status code descriptor | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

Set the `AUDIT_SECRET_KEY` environment variable in production to ensure cryptographic audit trail integrity:

```bash
export AUDIT_SECRET_KEY="your-secure-random-key"
```

If not set, an ephemeral key is generated for development (with a warning).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
docker build -t quantum-walk-spatial-search .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY="your-secure-key" quantum-walk-spatial-search
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
quantum-walk-spatial-search/
├── agents/                  # Enterprise agent framework
│   ├── api.py              # FastAPI REST server
│   ├── base.py             # Security, PHI guard, audit trail
│   ├── models.py           # Pydantic data models
│   ├── supervisor.py       # Multi-agent orchestrator
│   ├── workers.py          # Specialized evaluation workers
│   ├── llm_factory.py      # LLM provider factory
│   ├── learning.py         # Bayesian calibration engine
│   ├── metrics.py          # Prometheus metrics collector
│   └── streamer.py         # WebSocket telemetry broadcaster
├── quantum_walk/           # Core quantum walk algorithms
│   ├── agents.py           # Sub-agent coordination
│   ├── engine.py           # Core algorithmic engine
│   ├── models.py           # Data models
│   ├── server.py           # FastAPI server factory
│   └── cli.py              # CLI entry point
├── tests/                  # Pytest test suite
├── web/index.html          # Operations console UI
├── cli.py                  # Main CLI entry point
├── simulator.py            # High-throughput simulation
├── enrichment.py           # Enrichment feature modules
├── pyproject.toml          # Project configuration
├── Dockerfile              # Container build
└── docker-compose.yml      # Multi-service orchestration
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
