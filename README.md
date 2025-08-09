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
