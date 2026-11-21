# AGENT GATEKEEPER – INDIGO EDITION
### AI Agent Authorization & Governance System (Academic Simulation Prototype)

---

## 🎓 Student & Academic Project Information
- **Student Enrolment Number:** `PGD202566590`
- **Partner Organization / Brand:** IndiGo Airlines (InterGlobe Aviation Ltd.)
- **Project Domain:** AI Agent Authorization & Zero-Trust Governance Gateway
- **Technology Stack:** Python 3.14, Streamlit, Pandas, JSON & CSV Persistent Storage
- **Platform Compatibility:** Windows 10/11, macOS, Linux

> [!NOTE]
> **Academic Simulation Disclaimer:** This system is an educational authorization gateway prototype designed for academic evaluation. It does not interface with live IndiGo production reservation systems, GDS, or payment gateways. Policy thresholds and rules are academic simulation parameters.

---

## ✈️ System Overview & Objective
With the rapid emergence of autonomous AI agents (personal travel bots, corporate booking assistants, automated itinerary planners) acting on behalf of airline passengers, airlines require a robust **Zero-Trust Gatekeeper** layer.

**Agent Gatekeeper – IndiGo Edition** acts as an intermediary authorization firewall. Whenever an external AI agent requests to perform an operation (viewing fares, booking tickets, modifying itineraries, or requesting refunds), the Gatekeeper evaluates the request against **eight strict business policies** to determine whether to:
1. **ALLOW:** Low-risk, non-financial operations (e.g., viewing fares by registered agents).
2. **ASK CUSTOMER:** Operations that commit funds or alter bookings, requiring direct human-in-the-loop authorization.
3. **BLOCK:** Revoked credentials, unknown/unregistered bots, high-value unauthorized bookings, or malformed requests.

---

## 🏛️ Business Rules Matrix (R1 to R8)

The Gatekeeper implements a strict 3-tier hierarchical evaluation pipeline:
1. **Tier 1 (Integrity & Validation):** Check completeness and validity first (**R8**).
2. **Tier 2 (Identity & Credential Check):** Verify revocation status (**R1**) and registered existence (**R2**). *Revoked agents can never bypass R1.*
3. **Tier 3 (Policy Action Rules):** Evaluate action type and monetary thresholds (**R3, R4, R5, R6, R7**).

| Rule ID | Policy Name | Condition / Scenario | Decision | Priority / Tier |
| :---: | :--- | :--- | :---: | :---: |
| **R1** | **Revoked Agent Policy** | Agent permission status is `REVOKED` | **BLOCK** | Tier 2 (Precedence over actions) |
| **R2** | **Unknown Agent & Identity Policy** | Agent ID unknown OR agent name / customer ownership mismatches registry | **BLOCK** | Tier 2 (Anti-spoofing check) |
| **R3** | **View Fares Policy** | Registered active agent requests `View Fares` | **ALLOW** | Tier 3 (Zero financial liability) |
| **R4** | **Standard Booking Policy** | Flight booking amount **< Rs. 15,000** | **ALLOW** | Tier 3 (Automated standard booking) |
| **R5** | **High-Value Booking Policy** | Flight booking amount **≥ Rs. 15,000** | **ASK CUSTOMER** | Tier 3 (Human-in-the-loop consent) |
| **R6** | **Change Booking Policy** | Any request to `Change Booking` | **ASK CUSTOMER** | Tier 3 (Itinerary change impact) |
| **R7** | **Refund Request Policy** | Any request to `Request Refund` | **ASK CUSTOMER** | Tier 3 (Financial credit reversal) |
| **R8** | **Request Validation Policy** | Missing fields, invalid action, or negative amount | **BLOCK** | Tier 1 (Evaluated first) |

---

## 📂 Project File Structure

```text
Agent Gatekeeper/
│
├── app.py                      # Main Streamlit web application & UI/UX dashboard
├── gatekeeper_engine.py        # Core authorization decision engine & persistence logic
├── tests.py                    # Standalone CLI automated verification test suite
├── requirements.txt            # Python dependencies (Streamlit, Pandas)
├── README.md                   # Full system documentation & run instructions
├── PROMPTS.md                  # Development history, prompt log & design decisions
│
└── data/                       # Persistent file storage
    ├── agents.json             # Registered and revoked AI agents (JSON)
    └── audit_log.csv           # Persistent immutable audit ledger (CSV)
```

---

## 📦 System Modules

### Module 1: Dashboard
- **Branding & Identity:** Displays application name, student enrolment number (`PGD202566590`), and IndiGo navy blue aesthetic.
- **KPI Metrics:**
  - Total registered agents, Active agents, Revoked agents.
  - Total requests processed, ALLOW count, ASK CUSTOMER count, BLOCK count.
- **Analytics & History:** Visual decision distribution chart, quick policy reference, and a real-time feed of recent authorization decisions.

### Module 2: Agent Registration
- Form capturing: Customer Name, Agent Name, Unique Agent ID, Registration Timestamp, and default Permission Status (`ACTIVE`).
- **Duplicate Prevention:** Case-insensitive validation against `data/agents.json` to prevent duplicate agent registrations.
- Instant success feedback with newly registered agent metadata.

### Module 3: Request Evaluation
- Input form capturing: Customer Name, Agent Name, Agent ID, Requested Action, and Booking Amount in INR (₹).
- **Preset Quick-Load Buttons:** 1-click test scenarios for effortless demonstration.
- **Real-Time Evaluation:** Instant visual outcome cards with color-coded badges:
  - 🟢 **ALLOW** (Green)
  - 🟡 **ASK CUSTOMER** (Amber)
  - 🔴 **BLOCK** (Red)
- Displays Rule number, reason, timestamp, and generated Request ID.
- **Integrated Customer Simulator:** If an `ASK CUSTOMER` decision is rendered, an interactive confirmation panel appears inline.

### Module 4: Customer Confirmation
- Dedicated queue for requests awaiting customer authorization.
- Provides interactive **Approve** and **Reject** buttons for simulated customer decisions.
- Persists customer response (`Approved` or `Rejected`) and exact response timestamp directly into `data/audit_log.csv`.
- Tabbed view displaying pending queues versus resolved confirmation history.

### Module 5: Agent Revocation
- Administrative control panel displaying all registered agents.
- **Confirmation Step:** Requires explicit confirmation checkbox before revoking credentials.
- Records exact revocation timestamp, changes status to `REVOKED`, and preserves historical audit trail.
- Strict enforcement: Any revoked agent attempting future requests will immediately be **BLOCKED under Rule R1**.

### Module 6: Audit Log
- Persistent, searchable, and filterable transaction ledger.
- Filters by: Text search (customer, agent, explanation), Decision (ALLOW, ASK CUSTOMER, BLOCK), Action type, and Customer response.
- **CSV Export:** One-click download button to export the audit log.

### Module 7: Test Centre
- In-app execution of the **6 required academic test scenarios** plus boundary validation tests.
- Dynamically executes against the live `evaluate_request()` engine using isolated mock data (preventing audit log pollution).
- Displays Test Number, Input Scenario, Expected Result, Actual Result, Rule Number, and PASS/FAIL indicators.

---

## 🚀 Installation & Running Instructions on Windows

### Prerequisites
- Windows 10 or Windows 11
- Python 3.10+ (Recommended: **Python 3.14**)

### Step 1: Open Terminal in Project Directory
Open **PowerShell** or **Command Prompt** and navigate to the project directory:
```powershell
cd "c:\Users\adars\OneDrive\Desktop\Agent Gatekeeper"
```

### Step 2: Install Dependencies
Install required packages using the Python launcher:
```powershell
py -3.14 -m pip install -r requirements.txt
```
*(If `py` is not configured, run `python -m pip install -r requirements.txt`)*

### Step 3: Run the Automated CLI Test Suite (pytest)
Verify that all 6 required academic test scenarios pass with 100% compliance using pytest:
```powershell
py -3.14 -m pytest -v tests.py
```
*(You can also run directly with `py -3.14 tests.py`)*

### Step 4: Launch the Streamlit Web Application
Start the interactive IndiGo Agent Gatekeeper application:
```powershell
py -3.14 -m streamlit run app.py
```
Or directly:
```powershell
streamlit run app.py
```
The application will launch automatically in your default web browser at:
`http://localhost:8501`

---

## 🧪 Automated Test Scenarios Reference

The test suite in `tests.py` and Module 7 verifies the following required scenarios:

| Test | Input Scenario | Expected Decision | Expected Rule | Verification Rationale |
| :---: | :--- | :---: | :---: | :--- |
| **TEST 1** | Registered agent, View Fares, Rs. 0 | **ALLOW** | **R3** | Low-risk read-only fare lookup by verified active agent. |
| **TEST 2** | Unknown agent, Book Flight, Rs. 5,000 | **BLOCK** | **R2** | Zero-trust: Unregistered bot credentials must be blocked. |
| **TEST 3** | Registered agent, Book Flight, Rs. 20,000 | **ASK CUSTOMER** | **R5** | Booking amount is ≥ Rs. 15,000; requires customer consent. |
| **TEST 4** | Registered agent, Book Flight, Rs. 10,000 | **ALLOW** | **R4** | Booking amount is < Rs. 15,000; automated booking permitted. |
| **TEST 5** | Revoked agent, View Fares, Rs. 0 | **BLOCK** | **R1** | R1 takes precedence over R3; revoked bots cannot view fares. |
| **TEST 6** | Registered agent, Request Refund, Rs. 5,000 | **ASK CUSTOMER** | **R7** | Refund triggers financial reversal; requires customer consent. |
| **TEST 7** | Agent Name Mismatch with registered ID | **BLOCK** | **R2** | Anti-spoofing: Submitted agent name must match registered name. |
| **TEST 8** | Customer Ownership Mismatch with registered ID | **BLOCK** | **R2** | Anti-hijacking: Submitted customer must match registered owner. |

---

## 👨‍🏫 Demonstration Walkthrough Guide

To present or demonstrate this application to faculty or evaluators:
1. **Launch Dashboard:** Show the IndiGo-branded dashboard, student enrolment number `PGD202566590`, and real-time KPI metrics.
2. **Register a New Agent:** Open **Agent Registration**, register an agent (e.g., `6E-AGT-200`, `Adarsh Assistant`), and attempt registering it again to demonstrate duplicate ID rejection.
3. **Execute Evaluation:** Open **Request Evaluation**, use the **Quick-Load Presets** to demonstrate:
   - *Test 1:* View Fares -> Generates green **ALLOW (R3)** badge.
   - *Test 3:* Book Flight Rs. 20,000 -> Generates amber **ASK CUSTOMER (R5)** card.
   - *Test 4:* Book Flight Rs. 10,000 -> Generates green **ALLOW (R4)** badge.
4. **Demonstrate Customer Consent:** In the Customer Confirmation simulator, click **Approve** or **Reject** to show live human-in-the-loop authorization updating in real time.
5. **Revoke an Agent:** Open **Agent Revocation**, select an active agent, check the confirmation box, and click **Revoke**. Return to **Request Evaluation** and submit a View Fares request for that agent to show it is **BLOCKED under R1**.
6. **Audit & Export:** Open **Audit Log**, filter by decision or keyword, and click **Export Audit Log to CSV**.
7. **Run Test Centre:** Open **Test Centre** and click **Execute Automated Test Suite** to show a 100% pass rate across all test cases.
## Automated Testing

The prototype was validated using pytest.

- Total automated test cases: 9
- Passed: 9
- Failed: 0

### Test Coverage
1. Registered agent viewing fares (R3).
2. Unknown agent attempting a booking (R2).
3. Booking of ₹15,000 and above (R5).
4. Booking below ₹15,000 (R4).
5. Revoked agent attempting access (R1).
6. Registered agent requesting a refund (R7).
7. Agent name mismatch (R2).
8. Customer ownership mismatch (R2).
9. Revoked agent with identity mismatch (R1).

Run the tests using:

py -3.14 -m pytest -v tests.py

**Note:** These are academic prototype rules and do not represent official IndiGo policies.