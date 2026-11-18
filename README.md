# PES1UG24CS541_Vrunda_SE_LAB
# Software Engineering Labs: Incident Escalation & On-Call Rotation Engine

**PES University – Department of Computer Science and Engineering**
**Course:** Software Engineering Lab
**Problem Statement #48:** Developer Tools & IT Operations

| Name | SRN | Section |
|------|-----|---------|
| Vrunda C | PES1UG24CS541 | I |

---

## Project Overview

The **Incident Escalation & On-Call Rotation Engine** is a DevOps on-call management system. It:

- organises team **shift rotations**, with a primary and a secondary on-call engineer for each shift;
- **ingests monitoring alerts** and routes them to the engineer currently on call;
- sends notifications through **multi-tier phone, SMS, email and webhook escalation ladders**. If the primary engineer does not acknowledge within **5 minutes**, the alert escalates to the secondary engineer and then to the Incident Commander;
- tracks **incident post-mortems** with an auto-generated timeline, root cause and action items.

**Actors:** On-Call Engineer, Incident Commander
**Supporting systems:** Monitoring System, Notification Gateway (Phone / SMS / Email / Webhook)

---

## Repository Structure

```
SELABS/
│
├── README.md                                   This file
│
├── Lab1-Incident-Escalation-OnCall/            Lab 1: Requirements Engineering & UML Use-Case Modelling
│   ├── README.md
│   ├── requirements/requirements.md            FR-001 to FR-005, NFR-001 to NFR-002
│   ├── uml/use-case-diagram.drawio             Use-case diagram with «include» and «extend»
│   └── use-case-flow/incident-escalation-flow.md
│
├── Lab2/                                       Lab 2: Agile Backlog Creation & Sprint Simulation in Jira
│   ├── PES1UG24CS541_SE_Lab-2.pdf              Jira screenshots + reflection answers
│   └── PES1UG24CS541_SE_Lab-2.docx
│
├── Lab3/                                       Lab 3: Component Modelling & Architectural Pattern Selection
│   ├── README.md
│   ├── component-diagram.drawio                Editable UML component diagram
│   ├── component-diagram.png
│   ├── component-diagram.pdf
│   ├── Architecture_Justification.docx         One-page architecture justification
│   └── Architecture_Justification.pdf
│
└── lab7/                                       Lab 7: Fuzzing for Input Validation Bugs (Daycare Fees)
    ├── README.md
    ├── SE_LAB_7_PES1UG24CS541.pdf              Report with screenshots for Steps 1-6
    ├── daycare_fees.py                         Fixed application script
    ├── test_daycare_fees.py                    Hypothesis fuzz tests (66 cases)
    ├── original/daycare_fees_original.py       Original buggy script (for reproducing the failures)
    └── screenshots/                            Individual screenshot images
```

---

## Lab 1: Requirements Engineering & UML Use-Case Modelling

### Requirements Summary

| ID | Type | Requirement | Priority |
|----|------|-------------|----------|
| FR-001 | Functional | Ingest incident alerts, identify the active on-call engineer from the rotation schedule, and escalate to the secondary engineer if the alert is not acknowledged within 5 minutes | High |
| FR-002 | Functional | Create, edit and publish gap-free rotation schedules with a primary and a secondary engineer and shift-swap overrides | High |
| FR-003 | Functional | Configure a multi-tier escalation ladder (Primary → Secondary → Incident Commander) with per-tier channels and 1–5 minute timeouts | High |
| FR-004 | Functional | Acknowledge incidents by SMS reply, phone keypress or web console and later resolve them. Acknowledgement cancels any pending escalation | High |
| FR-005 | Functional | Auto-generate the incident timeline and record the post-mortem before a P1/P2 incident can be closed | Medium |
| NFR-001 | Performance & Security | Alert dispatch via webhook, SMS and email must initiate within 3 seconds of alert ingestion | High |
| NFR-002 | Reliability & Availability | 99.95% monthly availability, zero lost alerts, persisted escalation timers, failover within 60 seconds | High |

The full table, with acceptance criteria and rationale, is in [`Lab1-Incident-Escalation-OnCall/requirements/requirements.md`](Lab1-Incident-Escalation-OnCall/requirements/requirements.md).

### Use-Case Diagram Highlights

- **«include»:** *Handle Incident Alert* always includes *Identify Active On-Call Engineer* and *Dispatch Alert Notification*. *Conduct Post-Mortem* always includes *Generate Incident Timeline*.
- **«extend»:** *Escalate to Secondary Engineer* extends *Handle Incident Alert* at the **Acknowledgement Timeout** extension point, under the condition *not acknowledged within 5 minutes*.

### Use-Case Flow

**UC-01 – Handle Incident Alert** (primary actor: On-Call Engineer). The main success scenario covers alert ingestion, engineer lookup, dispatch within 3 seconds and acknowledgement within 5 minutes. The alternate flow covers the acknowledgement timeout and escalation to the secondary engineer.

---

## Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Jira space:** `PES1UG24CS541_Incident Escalation & On-Call Rotation Engine` (key **IEORE**, Scrum, company-managed)

### Epics

| Key | Epic | Source |
|-----|------|--------|
| IEORE-1 | On-Call Rotation Management | FR-002 |
| IEORE-2 | Escalation Policy Configuration | FR-003 |
| IEORE-3 | Alert Ingestion & Escalation | FR-001 |
| IEORE-4 | Incident Response & Post-Mortem | FR-004, FR-005 |
| IEORE-5 | Performance, Security & Reliability | NFR-001, NFR-002 |

### Sprints

| Sprint | User Stories | Story Points | Result |
|--------|--------------|--------------|--------|
| Sprint 1 | IEORE-6 Create Rotation Schedule (5), IEORE-7 Configure Multi-Tier Escalation Ladder (5), IEORE-8 Ingest and Route Incident Alerts (5), IEORE-9 Acknowledge and Resolve Incident (5), IEORE-10 Dispatch Alerts Within 3 Seconds Securely (8) | 28 | All 5 done (28 → 0) |
| Sprint 2 | IEORE-11 Auto-Escalate Unacknowledged Incidents (8), IEORE-12 Survive Node Failure Without Losing Alerts (5), IEORE-13 Record Post-Mortem (5), IEORE-14 View Schedule and Request Shift Swap (3), IEORE-15 Set Notification Channels per Tier (3) | 24 | All 5 done (24 → 0) |

The PDF contains the backlog, epics, story points, active sprint boards, both burndown charts and the four reflection answers.

---

## Lab 3: Component Modelling & Architectural Pattern Selection

**Selected architecture:** **Microservices**

### Components

| Component | Responsibility |
|-----------|----------------|
| On-Call Web & Mobile Console | Client used by On-Call Engineers and the Incident Commander |
| Alert Ingestion Service | Authenticates and validates incoming monitoring alerts |
| Rotation Schedule Service | Manages rotations and answers "who is on call now?" |
| Escalation Engine | Runs the escalation ladder and the 5-minute acknowledgement timers |
| Notification Dispatcher | Sends phone, SMS, email and webhook notifications in parallel |
| Incident & Post-Mortem Service | Incident lifecycle, acknowledgement, timeline and post-mortems |
| Incident & Schedule Database | Persistent storage for schedules, incidents and escalation timers |

**External systems:** Monitoring System, Notification Gateway

### Interfaces (provided ● / required ◡)

| Interface | Provider → Consumer | Protocol |
|-----------|---------------------|----------|
| IAlertIngest | Alert Ingestion Service → Monitoring System | HTTPS webhook + HMAC |
| IScheduleMgmt | Rotation Schedule Service → Console | HTTPS REST API |
| IIncidentMgmt | Incident & Post-Mortem Service → Console, Escalation Engine | HTTPS REST API / REST API call |
| IEscalationControl | Escalation Engine → Alert Ingestion Service, Incident & Post-Mortem Service | Async message queue |
| IOnCallLookup | Rotation Schedule Service → Escalation Engine | gRPC call |
| INotify | Notification Dispatcher → Escalation Engine | Async message queue |
| IChannelDelivery | Notification Gateway → Notification Dispatcher | HTTPS API / SMTP |
| «use» | Rotation, Escalation, Incident services → Database | SQL queries (TLS) |

### Why Microservices?

1. **Independent scaling:** During an alert storm, only Ingestion, Escalation and Dispatch are scaled out.
2. **Fault isolation:** A failure in post-mortems or the console never stops the critical ingest → escalate → notify path (NFR-002).
3. **Security:** Narrow interfaces, HMAC-signed webhooks, token-authenticated console access, mutual TLS between services and per-service database credentials.
4. **Performance:** Asynchronous queues and parallel dispatch keep alert dispatch under 3 seconds even at peak load (NFR-001).

---

## Lab 7: Fuzzing for Input Validation Bugs

**Problem:** L6_L7_48 Daycare Fees | **Tools:** Python, Hypothesis, pytest | **Folder:** [`lab7/`](lab7/)

Property-based fuzzing with Hypothesis was run against `daycare_fees.py`, which has three functions: `parse_enrolment`, `hours_average` and `payable_fee`.

| | Original code | Fixed code |
|---|---|---|
| Tests passing | 5 / 66 | **66 / 66** |

### Bugs Found

- **Crashes:** `None` and other non-string input, missing or extra `:` / `|` separators, empty CSV elements (`1,,3`), non-numeric text and decimals in the hours list.
- **Silent wrong answers:** `nan` / `inf` accepted as numbers, negative hours accepted, `hours_average("1,2")` returned `1` because of floor division, and a **negative discount increased the bill** (`3000|-9999` gave 13539.0).

### Fix

All three functions are now total: they never raise and return `None` for invalid input, and `main()` prints a clear message. Numbers must be plain ASCII decimals, finite and in range (hours 0-168, fee at most 10,000,000), and averages use true division.

The full write-up with screenshots for Steps 1-6 is in [`lab7/SE_LAB_7_PES1UG24CS541.pdf`](lab7/SE_LAB_7_PES1UG24CS541.pdf), and [`lab7/README.md`](lab7/README.md) has the bug table and run instructions.

---

## Viewing the Diagrams

The `.drawio` files can be opened in any of these:

1. **diagrams.net (browser):** <https://app.diagrams.net/> → **File → Open from → Device** (or **GitHub**).
2. **draw.io Desktop:** <https://github.com/jgraph/drawio-desktop/releases>
3. **VS Code:** the *Draw.io Integration* extension (`hediet.vscode-drawio`).

The Lab 3 diagram is also provided as ready-to-view PNG and PDF files.

---

## Tools Used

| Purpose | Tool |
|---------|------|
| Requirements & specifications | Markdown, Microsoft Word |
| UML diagrams | draw.io (diagrams.net) |
| Agile backlog & sprints | Jira Software (Scrum) |
| Fuzz testing | Python, Hypothesis, pytest |
| Version control | Git & GitHub |
