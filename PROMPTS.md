# PROMPTS & SYSTEM ARCHITECTURE DOCUMENTATION
### Project: AGENT GATEKEEPER – INDIGO EDITION
**Student Enrolment:** `PGD202566590` | **Organization:** IndiGo Airlines | **Project:** AI Agent Authorization System

---

## 1. Original User Specification & Requirements Prompt

```text
Act as a senior Python developer and UI/UX designer. Build a complete, functional web
application called:

AGENT GATEKEEPER – INDIGO EDITION

STUDENT DETAILS:
Enrolment Number: PGD202566590
Company: IndiGo Airlines
Project: AI Agent Authorization System

OBJECTIVE:
Build a prototype that evaluates requests from customers' external AI agents and decides whether
to ALLOW, ASK CUSTOMER or BLOCK the request.

TECHNOLOGY:
- Python 3.14
- Streamlit
- Pandas
- CSV and JSON persistent storage

DESIGN:
- Professional airline-inspired dashboard
- Navy blue, white and light grey theme
- Modern sidebar navigation
- Attractive KPI cards
- Responsive layout
- Clear decision indicators

MODULE 1: DASHBOARD
Display:
- Application name and logo-style branding
- Student enrolment number PGD202566590
- Total registered agents
- Active agents
- Revoked agents
- Total requests
- ALLOW count
- ASK CUSTOMER count
- BLOCK count

MODULE 2: AGENT REGISTRATION
Create a registration form with:
- Customer name
- Agent name
- Unique agent ID
- Registration timestamp
- Agent permission status
Save registered agents persistently.
Prevent duplicate agent IDs.

MODULE 3: REQUEST EVALUATION
Create an input form containing:
- Customer name
- Agent name
- Agent ID
- Requested action
- Booking amount in INR

Available actions:
1. View Fares
2. Book Flight
3. Change Booking
4. Request Refund

Implement these eight business rules:
R1: Revoked agents must always be BLOCKED.
R2: Unknown or unregistered agents must always be BLOCKED.
R3: Registered agents requesting to view fares must be ALLOWED.
R4: Flight booking above Rs. 15,000 must be BLOCKED.
R5: Flight booking of Rs. 15,000 or below must return ASK CUSTOMER.
R6: Change booking must return ASK CUSTOMER.
R7: Refund requests must return ASK CUSTOMER.
R8: Invalid or incomplete requests must be BLOCKED.

IMPORTANT:
Validate request information first.
Then check revoked and unknown agent status.
Apply the appropriate action rule afterward.
Ensure a revoked agent can never bypass R1.

Every decision must show:
- ALLOW / ASK CUSTOMER / BLOCK
- Rule number
- Reason for decision
- Date and time

MODULE 4: CUSTOMER CONFIRMATION
For ASK CUSTOMER decisions:
- Show Approve button.
- Show Reject button.
- Record customer response.
- Save response timestamp.
- Display approval status.
This is a simulated confirmation process.
Never execute real bookings or payments.

MODULE 5: AGENT REVOCATION
Display registered agents.
Allow administrator to revoke an agent.
Add a confirmation step before revocation.
Save exact revocation date and timestamp.
Change status to REVOKED.
Preserve historical records.
Any revoked agent attempting another request must receive BLOCK under R1.

MODULE 6: AUDIT LOG
Maintain a persistent audit log.
Record:
- Request ID
- Date and time
- Customer name
- Agent name
- Agent ID
- Requested action
- Amount
- Decision
- Rule number
- Decision explanation
- Customer response
Provide a searchable audit table.
Add CSV export functionality.

MODULE 7: TEST CENTRE
Implement six actual automated test cases:
TEST 1: Registered agent, View Fares, Rs. 0 -> Expected: ALLOW, R3
TEST 2: Unknown agent, Book Flight, Rs. 5,000 -> Expected: BLOCK, R2
TEST 3: Registered agent, Book Flight, Rs. 20,000 -> Expected: BLOCK, R4
TEST 4: Registered agent, Book Flight, Rs. 10,000 -> Expected: ASK CUSTOMER, R5
TEST 5: Revoked agent, View Fares, Rs. 0 -> Expected: BLOCK, R1
TEST 6: Registered agent, Request Refund, Rs. 5,000 -> Expected: ASK CUSTOMER, R7

Display:
- Test number
- Input scenario
- Expected result
- Actual result
- Rule number
- PASS or FAIL
Execute tests against the actual decision engine.
Do not hardcode test results.
Use isolated test data.

FILE STRUCTURE:
Create:
app.py
tests.py
requirements.txt
README.md
PROMPTS.md

Create a data folder containing:
agents.json
audit_log.csv
```

---

## 2. Architectural Design Decisions

### 2.1 Decoupled Architecture (`gatekeeper_engine.py` & `app.py`)
To satisfy the requirement *"Keep business logic separate from UI where possible"* and allow both the Streamlit web interface (`app.py`) and the CLI automated verification suite (`tests.py`) to execute against the exact same logic, all business rules, persistence logic, and test runners were isolated in `gatekeeper_engine.py`.

### 2.2 Strict Rule Evaluation Hierarchy
The evaluation order strictly adheres to the security specification:
```text
Input Request -> Step 1: Input Validation (R8)
             -> Step 2: Agent Credential Check (R1, R2)
                 - If Revoked -> BLOCK (R1) [Cannot be bypassed!]
                 - If Unknown -> BLOCK (R2)
             -> Step 3: Action & Amount Policies (R3, R4, R5, R6, R7)
                 - View Fares -> ALLOW (R3)
                 - Book Flight > 15,000 -> BLOCK (R4)
                 - Book Flight <= 15,000 -> ASK CUSTOMER (R5)
                 - Change Booking -> ASK CUSTOMER (R6)
                 - Request Refund -> ASK CUSTOMER (R7)
```

### 2.3 Isolated Testing Architecture
In `gatekeeper_engine.py`, the `run_automated_tests()` function utilizes an isolated in-memory registry dictionary:
- `TEST-REG-ACTIVE`: Active registered agent.
- `TEST-REG-REVOKED`: Revoked agent (revoked timestamp preserved).
- `TEST-UNKNOWN-999`: Non-existent agent ID.

This guarantees that running automated tests from `tests.py` or the in-app Test Centre never injects mock records or alters the real production `data/agents.json` and `data/audit_log.csv`.

### 2.4 Human-in-the-Loop Confirmation Design
Requests resulting in `ASK CUSTOMER` trigger a two-level confirmation workflow:
1. **In-line Decision Simulator:** Directly beneath the evaluation result in Module 3.
2. **Dedicated Confirmation Queue:** In Module 4, with tabbed views for pending authorizations and past resolution history.
Both interfaces update the persistent audit log with the customer's response (`Approved` or `Rejected`) and the timestamp of confirmation.

### 2.5 Windows Console Compatibility
In `tests.py`, standard ASCII indicators (`[PASS]` / `[FAIL]`) and `sys.stdout.reconfigure(encoding="utf-8")` were implemented to avoid Windows `cp1252` encoding errors when executed in default PowerShell or Command Prompt terminals.
---

## 3. Post-Development Security Enhancements and Validation

After generating the initial prototype, I independently reviewed the agent authentication workflow and identified the need for stronger identity verification.

### 3.1 Additional Security Controls

The following enhancements were incorporated into the decision engine:

- **Agent Name Verification:** The submitted agent name must match the registered agent identity.
- **Customer Ownership Verification:** An agent must belong to the customer associated with the request.
- **Revocation Priority:** A revoked agent must remain blocked, including when other identity details do not match.

These checks strengthen protection against unauthorized agent access and identity misuse.

### 3.2 Expanded Automated Testing

The original six test scenarios were expanded to nine automated test cases.

| Additional test | Scenario | Expected result |
|---|---|---|
| Test 7 | Agent name mismatch | BLOCK – R2 |
| Test 8 | Customer ownership mismatch | BLOCK – R2 |
| Test 9 | Revoked agent with identity mismatch | BLOCK – R1 |

### 3.3 Validation Results

The completed test suite was executed locally using pytest.

- Total test cases: 9
- Passed: 9
- Failed: 0
- Test execution time: 0.73 seconds

Command used:

`py -3.14 -m pytest -v tests.py`

**Validation note:** All results represent testing of an academic simulation. The decision rules and ₹15,000 threshold are prototype assumptions and are not official IndiGo policies.
