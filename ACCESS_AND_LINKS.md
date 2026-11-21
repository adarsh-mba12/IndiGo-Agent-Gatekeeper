# IndiGo Agent Gatekeeper – Access and Links

## 1. GitHub Repository

Repository: https://github.com/adarsh-mba12/IndiGo-Agent-Gatekeeper

## 2. Run the Application

Open PowerShell inside the project directory and execute:

```powershell
py -3.14 -m streamlit run app.py --server.port 8505
```

Open in browser: http://localhost:8505

## 3. Run Automated Tests

```powershell
py -3.14 -m pytest -v tests.py
```

Expected result: 9 tests passed.

## 4. Sample Agent Access

| Agent ID | Agent Name | Status |
|---|---|---|
| 6E-AGT-101 | SkyTravel AI | Revoked |
| 6E-AGT-102 | FlySmart Assistant | Active |
| 6E-AGT-103 | SkyTravel AI | Active |
| 6E-AGT-999 | Rogue TravelBot | Revoked |

These are demonstration records for the academic prototype.

## 5. Authorization Rules

- R1: Revoked agent – BLOCK
- R2: Unknown agent or identity mismatch – BLOCK
- R3: Verified agent viewing fares – ALLOW
- R4: Verified booking below ₹15,000 – ALLOW
- R5: Verified booking of ₹15,000 or above – ASK CUSTOMER
- R6: Booking modification – ASK CUSTOMER
- R7: Refund request – ASK CUSTOMER
- R8: Invalid or incomplete request – BLOCK

## 6. Important Note

This is an academic simulation. It does not connect to IndiGo's live booking systems or provide real agent credentials.