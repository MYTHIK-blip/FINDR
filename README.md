# 🧭 FINDR — Aotearoa Employment & Contract Intelligence Agent

## Ethos
FINDR exists to **connect anyone, regardless of circumstance, to viable work, tenders, training, or contract opportunities** in Aotearoa New Zealand.  
It is built with **dignity, transparency, and resilience** at its core — capable of serving those who are homeless, veterans, displaced professionals, students, young adults, or anyone seeking meaningful income and purpose.

Our guiding principle: *remove friction between a person and their next opportunity, while protecting privacy, safety, and agency.*

---

## Vision
A **national, barrier-aware opportunity finder** that:
- Aggregates **all public and partner-accessible work/tender/training sources**.
- Normalizes and enriches listings into **clear, machine- and human-readable formats**.
- Scores and ranks results for **fit, urgency, accessibility, and fairness**.
- Delivers actionable outputs — ready to upload to a CRM, save as CSV, integrate into downstream workflows, or provide as plain readable listings.

---

## Purpose
FINDR serves:
- Individuals in *any* employment situation or life stage.
- SMEs, NGOs, iwi, and community groups seeking to hire or subcontract locally.
- Career services, veterans’ networks, and youth employment programs.
- Researchers, civic agencies, and AI-assisted workforce projects.

---

## Core Operations

### 1. **Harvest**
Scrape or query sources (where legally permitted) across:
- **Government & Official**
  - GETS (Government Electronic Tenders Service)
  - MBIE open procurement datasets
  - Local council tender portals (LG Tenders)
  - NZDF Careers
  - MFAT tender notices
  - Ministry of Education & school employment boards
- **General Job Boards**
  - Trade Me Jobs
  - Seek NZ
  - Indeed NZ
  - LinkedIn Jobs (NZ filter)
- **Freelance & Contract**
  - Builderscrack
  - Zealancer
  - Unicorn Factory NZ
  - Twine (NZ-specific filter)
- **Youth & Student**
  - Student Job Search
  - University/polytechnic job boards
- **Training/Education**
  - NZQA-approved training providers
  - Micro-credential portals
- **Community & Gig**
  - Facebook Marketplace Jobs (manual moderation)
  - Local bulletin boards / NGO listings

---

### 2. **Normalize & Store**
- Convert to a unified `Opportunity` schema.
- Retain raw HTML/JSON snapshots for audit.
- Store normalized data in **DuckDB** and export as:
  - CSV
  - JSONL
  - Parquet
  - CRM-import-ready formats

---

### 3. **Enrich & Score**
- Extract key metadata: location, commute time, pay range, urgency, required docs/certs, eligibility for subsidies.
- Match against candidate constraints and supports.
- Score using a configurable YAML rubric:
  - Skill fit
  - Accessibility/barrier considerations
  - Pay adequacy
  - Growth/training potential
  - Employer reputation and stability

---

### 4. **Output & Integration**
- Outputs:
  - **Human-readable:** Web UI, printable PDF lists, plain text
  - **Machine-readable:** CSV, JSONL, CRM import
- Integrations:
  - CRM systems
  - Email alerts
  - Webhooks
  - Local or cloud-based dashboards

---

## Constraints & Compliance

### NZ Legislation Alignment
FINDR aligns with:
- **NZ Privacy Act 2020**
  - Opt-in collection of personal data
  - Right to access and correct personal info
  - Data minimization and retention limits
- **Unsolicited Electronic Messages Act 2007**
  - No sending unsolicited job offers without consent
- **Employment Relations Act 2000**
  - Clarity around contract types, pay, and conditions
- **AI Principles (MBIE/DIA frameworks)**
  - Transparency in scoring and matching
  - Explainability of recommendations
  - Fairness: avoid bias against protected groups
- **Robots.txt & Platform TOS**
  - Only scrape public data where permitted; respect API terms

---

## Outputs
FINDR can deliver results as:
- **Readable lists**: PDF, Markdown, or plaintext for individuals
- **Data feeds**: CSV/JSONL/Parquet for systems
- **CRM-ready**: field-aligned CSV/JSON
- **API endpoints**: FastAPI layer for real-time queries

---

## Status
🚧 **Early Development** — core schema, mock pipelines, and source adapters in progress.

---

## Roadmap
- [ ] Scaffold repo structure
- [ ] Implement GETS + Trade Me adapters
- [ ] Add scoring & explainability module
- [ ] Streamlit operator UI
- [ ] CSV/PDF export
- [ ] Expand to 10+ NZ sources
- [ ] Integrate with CRM/webhook

---

**Maintainer:** [@mythik](https://github.com/mythik)  
**License:** Pending (AGPL-3.0 planned)


Every run produces two parallel outputs:

Human-facing → PDF (formatted, sections, easy reading, print-friendly)

Machine-facing → CSV / JSONL / Parquet (ready for data pipelines, CRM import, automation)

Harvest layer is source-rich (all NZ sources we listed) with a clean “adapter per source” structure so adding new ones is frictionless.

Pipeline handles:

Harvest → Normalize → Enrich → Summarize → Render → Export

Summarization step for human PDF is a separate, pluggable component so later we can swap in better LLM summarizers or template engines without touching the core.

Proposed Repo Structure
plaintext
Copy
Edit
FINDR/
  README.md
  .gitignore
  pyproject.toml
  requirements.txt
  docker-compose.yml
  src/
    findr/
      __init__.py
      config.py
      schema.py
      pipeline.py         # Orchestrates harvest → normalize → enrich → render → export
      harvest/            # Source adapters
        __init__.py
        gets.py
        trademe.py
        seek.py
        indeed.py
        linkedin.py
        builderscrack.py
        zealancer.py
        unicornfactory.py
        twine.py
        sjs.py
        councils.py
        nzdf.py
        education.py
        facebook_marketplace.py
      normalize.py        # Cleans per-source data into schema
      enrich.py           # Geo, pay, eligibility, tagging
      summarize.py        # Summarization logic for PDFs
      scoring.py
      render/
        pdf.py            # PDF generation
        html.py           # HTML dashboard export
      export/
        csv_export.py
        jsonl_export.py
        parquet_export.py
      utils/
        logging.py
        file_ops.py
        http_client.py
    tests/
      test_harvest.py
      test_normalize.py
      test_summarize.py
      test_export.py
  data/
    raw/                  # Raw HTML/JSON
    bronze/               # Normalized
    silver/               # Deduped & enriched
    gold/                 # Scored + ready to export
    reports/              # Generated PDFs/HTML
  rules/
    scoring.yaml
    filters.yaml
Processing Flow
mermaid
Copy
Edit
flowchart LR
  A[Harvest from All Sources] --> B[Normalize into Common Schema]
  B --> C[Enrich with Tags, Geo, Pay Bands]
  C --> D[Score & Rank Opportunities]
  D --> E[Summarize for PDF]
  D --> F[Export Machine Data (CSV, JSONL, Parquet)]
  E --> G[Generate PDF Report]
  G --> H[Reports Directory]
  F --> I[Data Exports Directory]
Output Formats
Human-Readable (Default)
PDF: Sectioned by category (jobs, tenders, gigs, training), sorted by score

Rich table layouts (title, pay, deadline, URL, fit score, supports)

Summary sections at top (“Best Matches”, “Urgent Deadlines”, “Training/Support Links”)

Machine-Readable
CSV: column-mapped for easy spreadsheet/CRM import

JSONL: streaming-friendly for APIs

Parquet: optimized for analytics (DuckDB, Spark, etc.)

Summarization Stage
The summarization module will:

Group opportunities by type, region, urgency

Condense descriptions to key bullet points (skills required, supports available, pay, contact)

Flag special categories:

“Barrier Friendly” (no address, flexible hours, wage subsidy eligible)

“Veteran/Service Member Priority”

“Student/Youth Focused”

NZ Source List (Adapters to Build)
GETS — Government Electronic Tenders Service

MBIE Open Procurement Data

Local Government Tenders (LG Tenders)

NZDF Careers

MFAT Tender Notices

Ministry of Education & school boards

Trade Me Jobs

Seek NZ

Indeed NZ

LinkedIn Jobs (NZ filter)

Builderscrack

Zealancer

Unicorn Factory NZ

Twine (NZ filter)

Student Job Search

University/polytechnic job boards

NZQA-approved training providers

Facebook Marketplace Jobs (with moderation layer)

Community/NGO job boards

Immediate Sprint Plan
Scaffold repo & directories (above)

Implement mock adapters for GETS, Trade Me, SJS — enough to run pipeline end-to-end

Build PDF renderer with placeholder styling

Hook summarizer into PDF step

Build CSV & JSONL exporters

Commit/push — verify in WSL2 that everything runs under mythik user