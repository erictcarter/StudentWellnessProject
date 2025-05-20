

# 🎓 Student Wellness Analytics Dashboard

**A Reproducible Platform for Integrating Academic and Mental Health Signals**



## 🔍 Overview

This project delivers a structured, SQL-centric analytics pipeline designed to analyze relationships between student performance and mental health. It is fully containerized, modular, and built for reproducibility and transparency across ingestion, transformation, modeling, and visualization layers.



## 🎯 Goals

* Quantify impact of mental health on academic outcomes
* Normalize and warehouse diverse student datasets
* Provide clean, auditable transformation logic (ELT)
* Serve insights via responsive, interactive dashboards
* Demonstrate scalable analytics using open-source tools

---

## 🧱 Architecture

### Data Flow

```text
CSV Sources → Staging (SQL) → OLTP Schema → Data Warehouse (Star) → Dash (SQLAlchemy)
```

### Core Components

| Layer           | Toolset                                       |
| --------------- | --------------------------------------------- |
| Data Storage    | PostgreSQL (OLTP + DW)                        |
| Ingestion       | SQL-based `\COPY` (Airbyte / NiFi optional)   |
| Transformation  | dbt (Core), SQL                               |
| Visualization   | Dash / Plotly (Metabase optional)             |
| Orchestration   | Prefect, Airflow *(optional)*                 |
| Security & Auth | Keycloak (RBAC, SSO)                          |
| Monitoring      | Prometheus, Grafana                           |
| Deployment      | Docker, Docker Compose, Watchtower, Portainer |
| Governance      | OpenMetadata                                  |

---

## 📁 Repository Layout

```
student_analytics_project/
├── dashboards/               # Dash-based frontend
│   └── student_analytics_dash/
├── db/                       # SQL logic & raw data
│   ├── init/
│   │   ├── init_schema.sql
│   │   ├── init_staging.sql
│   │   ├── load_main_tables.sql
│   │   ├── students.csv
│   │   └── StudentPerformanceFactors.csv
├── docker/                   # Container builds
│   ├── docker-compose.yml
│   └── Dockerfile.dash
├── docs/                     # Diagrams, trackers, metadata
└── README.md                 # This document
```

---

## ⚙️ Environment Setup

### Requirements

* Docker & Docker Compose
* Git
* Python 3.9+ (if running Dash locally)

### Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/erictcarter/student_analytics_project.git
cd student_analytics_project

# 2. Launch containers
cd docker
docker compose up -d
```

Services:

* `student_postgres` – PostgreSQL (data warehouse)
* `student_pgadmin` – GUI DB client
* `student_dash` – Dash app on port 8050
* `student_xrdp` *(optional)* – GUI over RDP

---

## 🧪 ETL: Data Warehouse Pipeline

### File References

| File                   | Description                     |
| ---------------------- | ------------------------------- |
| `init_schema.sql`      | Defines OLTP and DW schemas     |
| `init_staging.sql`     | Creates raw ingest tables       |
| `load_main_tables.sql` | Populates fact/dimension tables |

### Execution Steps

```bash
# Load CSVs into container
docker cp students.csv student_postgres:/students.csv
docker cp StudentPerformanceFactors.csv student_postgres:/StudentPerformanceFactors.csv

# Run inside container
docker exec -it student_postgres psql -U postgres -d student_analytics_db
\i /init_schema.sql
\i /init_staging.sql
\COPY staging_students FROM '/students.csv' DELIMITER ',' CSV HEADER;
\COPY staging_performance FROM '/StudentPerformanceFactors.csv' DELIMITER ',' CSV HEADER;
\i /load_main_tables.sql
```

---

## 📊 Dashboards (Dash + Plotly)

### Launch Locally

```bash
cd dashboards/student_analytics_dash
pip install -r requirements.txt
python app.py
```

App URL: [http://localhost:8050](http://localhost:8050)

---

## 🔐 Security + Observability

| Feature        | Implementation                    |
| -------------- | --------------------------------- |
| Authentication | Keycloak (SSO, Role-Based Access) |
| Monitoring     | Prometheus, Grafana               |
| Governance     | OpenMetadata (catalog, lineage)   |

---

## 🧠 Project Timeline (7 Days)

| Day | Focus                               |
| --- | ----------------------------------- |
| 1   | Architecture, Docker, ERD           |
| 2   | OLTP schema + data normalization    |
| 3   | Dimensional modeling (star schema)  |
| 4   | dbt setup (staging → marts)         |
| 5   | SQL analysis + Dash/Plotly frontend |
| 6   | Optional: NoSQL, Cloud models       |
| 7   | Final packaging & documentation     |

---

## 🔁 Reproducibility + CI Ideas

* Modular SQL-based transformations
* Source-controlled dbt DAGs
* Containerized ELT (idempotent builds)
* CI/CD via GitHub Actions + `docker-compose up --build`

---

## ✅ Validation Queries

```sql
-- Confirm row counts
SELECT 'fact' AS type, COUNT(*) FROM student_analytics_dw.fact_student_performance
UNION ALL
SELECT 'dim_student', COUNT(*) FROM student_analytics_dw.dim_student
UNION ALL
SELECT 'dim_health', COUNT(*) FROM student_analytics_dw.dim_health;
```

---

## 📦 Enhancements (Next Phase)

* [ ] Automate ETL via Prefect
* [ ] Streamlined .env and credentials management
* [ ] Optional ML hooks for predictive scoring

---

## 👥 Authors

| Name   | Role                            |
| ------ | ------------------------------- |
| Carter | Engine, Architecture, Integration, Dash |
| Anita  | DBT Tests, Schema + ERD Design             |
| Arnold | Data cleaning, Data Dictionary + Sources       |

---

## 📜 License

MIT — free to use, adapt, and share.

---

