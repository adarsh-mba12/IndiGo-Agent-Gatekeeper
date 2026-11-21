"""
AGENT GATEKEEPER – INDIGO EDITION
Core Decision Engine and Persistence Layer

Student Details:
- Enrolment Number: PGD202566590
- Company: IndiGo Airlines
- Project: AI Agent Authorization System
"""

import os
import json
import csv
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd

# Project Root and File Paths via pathlib
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
AGENTS_FILE = DATA_DIR / "agents.json"
AUDIT_LOG_FILE = DATA_DIR / "audit_log.csv"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# System Metadata
STUDENT_ENROLMENT = "PGD202566590"
COMPANY_NAME = "IndiGo Airlines"
APP_TITLE = "AGENT GATEKEEPER – INDIGO EDITION"
PROJECT_NAME = "AI Agent Authorization System"

# Business Constants
BOOKING_LIMIT = 15000.0
VALID_ACTIONS = ["View Fares", "Book Flight", "Change Booking", "Request Refund"]

# Rules Reference Matrix
RULES_CATALOG = {
    "R1": {
        "title": "Revoked Agent Policy",
        "description": "Revoked agents must always be BLOCKED.",
        "decision": "BLOCK",
        "priority": 2
    },
    "R2": {
        "title": "Unknown Agent Policy",
        "description": "Unknown or unregistered agents must always be BLOCKED.",
        "decision": "BLOCK",
        "priority": 2
    },
    "R3": {
        "title": "View Fares Policy",
        "description": "Registered agents requesting to view fares must be ALLOWED.",
        "decision": "ALLOW",
        "priority": 3
    },
    "R4": {
        "title": "Standard Flight Booking Policy",
        "description": "Flight booking below Rs. 15,000 is ALLOWED.",
        "decision": "ALLOW",
        "priority": 3
    },
    "R5": {
        "title": "High-Value Flight Booking Policy",
        "description": "Flight booking of Rs. 15,000 and above must return ASK CUSTOMER.",
        "decision": "ASK CUSTOMER",
        "priority": 3
    },
    "R6": {
        "title": "Change Booking Policy",
        "description": "Change booking must return ASK CUSTOMER.",
        "decision": "ASK CUSTOMER",
        "priority": 3
    },
    "R7": {
        "title": "Refund Request Policy",
        "description": "Refund requests must return ASK CUSTOMER.",
        "decision": "ASK CUSTOMER",
        "priority": 3
    },
    "R8": {
        "title": "Request Validation Policy",
        "description": "Invalid or incomplete requests must be BLOCKED.",
        "decision": "BLOCK",
        "priority": 1
    }
}


@dataclass
class EvaluationResult:
    request_id: str
    timestamp: str
    customer_name: str
    agent_name: str
    agent_id: str
    action: str
    amount: float
    decision: str  # ALLOW | ASK CUSTOMER | BLOCK
    rule_number: str  # R1 - R8
    rule_description: str
    decision_explanation: str
    customer_response: str  # N/A | Pending | Approved | Rejected
    response_timestamp: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def get_data_paths(base_dir: Optional[Union[Path, str]] = None) -> Tuple[Path, Path]:
    """Returns absolute paths to agents.json and audit_log.csv using pathlib."""
    if base_dir is None:
        data_dir = DATA_DIR
    else:
        data_dir = Path(base_dir).resolve() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "agents.json", data_dir / "audit_log.csv"


def load_agents(agents_path: Optional[Union[Path, str]] = None) -> List[dict]:
    """Loads all registered agents from JSON file. Initializes if missing."""
    if agents_path is None:
        agents_path = AGENTS_FILE
    else:
        agents_path = Path(agents_path)

    if not agents_path.exists():
        initial_agents = [
            {
                "agent_id": "6E-AGT-101",
                "agent_name": "SkyTravel AI",
                "customer_name": "Adarsh Sharma",
                "registered_at": datetime.now().isoformat(timespec="seconds"),
                "status": "ACTIVE",
                "revoked_at": None
            },
            {
                "agent_id": "6E-AGT-102",
                "agent_name": "FlySmart Assistant",
                "customer_name": "Priya Patel",
                "registered_at": datetime.now().isoformat(timespec="seconds"),
                "status": "ACTIVE",
                "revoked_at": None
            },
            {
                "agent_id": "6E-AGT-999",
                "agent_name": "Rogue TravelBot",
                "customer_name": "Vikram Malhotra",
                "registered_at": datetime.now().isoformat(timespec="seconds"),
                "status": "REVOKED",
                "revoked_at": datetime.now().isoformat(timespec="seconds")
            }
        ]
        save_agents(initial_agents, agents_path)
        return initial_agents

    try:
        with open(agents_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def get_agents_dict(agents_path: Optional[Union[Path, str]] = None) -> Dict[str, dict]:
    """Returns a dict mapping normalized uppercase agent_id to agent records."""
    agents_list = load_agents(agents_path)
    return {agent["agent_id"].strip().upper(): agent for agent in agents_list if "agent_id" in agent}


def save_agents(agents: List[dict], agents_path: Optional[Union[Path, str]] = None) -> None:
    """Persists agents list to JSON."""
    if agents_path is None:
        agents_path = AGENTS_FILE
    else:
        agents_path = Path(agents_path)
    with open(agents_path, "w", encoding="utf-8") as f:
        json.dump(agents, f, indent=2, ensure_ascii=False)


def register_agent(
    customer_name: str,
    agent_name: str,
    agent_id: str,
    agents_path: Optional[Union[Path, str]] = None
) -> Tuple[bool, str, Optional[dict]]:
    """
    Registers a new external agent.
    Validates input and ensures no duplicate agent IDs exist.
    """
    c_name = customer_name.strip() if customer_name else ""
    a_name = agent_name.strip() if agent_name else ""
    a_id = agent_id.strip() if agent_id else ""

    if not c_name or not a_name or not a_id:
        return False, "All fields (Customer Name, Agent Name, Agent ID) are mandatory.", None

    agents = load_agents(agents_path)
    normalized_new_id = a_id.upper()

    for agent in agents:
        if agent.get("agent_id", "").strip().upper() == normalized_new_id:
            return False, f"Agent ID '{a_id}' already exists in registry. Duplicate IDs are rejected.", None

    now_ts = datetime.now().isoformat(timespec="seconds")
    new_agent = {
        "agent_id": a_id,
        "agent_name": a_name,
        "customer_name": c_name,
        "registered_at": now_ts,
        "status": "ACTIVE",
        "revoked_at": None
    }

    agents.append(new_agent)
    save_agents(agents, agents_path)
    return True, f"Agent '{a_name}' ({a_id}) registered successfully with status ACTIVE.", new_agent


def revoke_agent(agent_id: str, agents_path: Optional[Union[Path, str]] = None) -> Tuple[bool, str]:
    """
    Revokes an agent's authorization.
    Preserves historical records and marks status as REVOKED with exact timestamp.
    """
    if not agent_id:
        return False, "Agent ID is required to revoke."

    agents = load_agents(agents_path)
    norm_id = agent_id.strip().upper()
    found = False

    for agent in agents:
        if agent.get("agent_id", "").strip().upper() == norm_id:
            found = True
            if agent.get("status") == "REVOKED":
                return False, f"Agent '{agent_id}' is already REVOKED since {agent.get('revoked_at')}."
            agent["status"] = "REVOKED"
            agent["revoked_at"] = datetime.now().isoformat(timespec="seconds")
            break

    if not found:
        return False, f"Agent ID '{agent_id}' not found in registry."

    save_agents(agents, agents_path)
    return True, f"Agent '{agent_id}' authorization has been REVOKED. All subsequent requests will be BLOCKED under R1."


def load_audit_log(audit_path: Optional[Union[Path, str]] = None) -> pd.DataFrame:
    """Loads audit log into pandas DataFrame with schema validation and fallback parser."""
    if audit_path is None:
        audit_path = AUDIT_LOG_FILE
    else:
        audit_path = Path(audit_path)

    columns = [
        "request_id", "timestamp", "customer_name", "agent_name",
        "agent_id", "action", "amount", "decision", "rule_number",
        "decision_explanation", "customer_response", "response_timestamp"
    ]

    if not audit_path.exists() or audit_path.stat().st_size == 0:
        df = pd.DataFrame(columns=columns)
        return df

    try:
        # Standard pandas read with quoting enabled and keeping 'N/A' literal
        df = pd.read_csv(audit_path, dtype=str, keep_default_na=False)
    except Exception:
        # Resilient fallback parser: uses csv.reader line by line to preserve records
        records = []
        try:
            with open(audit_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                for row in reader:
                    if row:
                        if len(row) < len(columns):
                            row = row + [""] * (len(columns) - len(row))
                        records.append(row[:len(columns)])
            df = pd.DataFrame(records, columns=columns)
        except Exception:
            df = pd.DataFrame(columns=columns)

    # Ensure all columns exist
    for col in columns:
        if col not in df.columns:
            df[col] = ""

    # Convert amount to numeric for sorting and analytics
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    return df


def log_audit_record(record: EvaluationResult, audit_path: Optional[Union[Path, str]] = None) -> None:
    """Appends an evaluation record to the persistent audit log CSV."""
    if audit_path is None:
        audit_path = AUDIT_LOG_FILE
    else:
        audit_path = Path(audit_path)

    file_exists = audit_path.exists() and audit_path.stat().st_size > 0
    headers = [
        "request_id", "timestamp", "customer_name", "agent_name",
        "agent_id", "action", "amount", "decision", "rule_number",
        "decision_explanation", "customer_response", "response_timestamp"
    ]

    with open(audit_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow([
            record.request_id,
            record.timestamp,
            record.customer_name,
            record.agent_name,
            record.agent_id,
            record.action,
            f"{record.amount:.2f}",
            record.decision,
            record.rule_number,
            record.decision_explanation,
            record.customer_response,
            record.response_timestamp
        ])


def update_customer_response(
    request_id: str,
    response: str,
    audit_path: Optional[Union[Path, str]] = None
) -> Tuple[bool, str]:
    """
    Updates the customer confirmation response for an ASK CUSTOMER request.
    Allowed responses: 'Approved' | 'Rejected'
    """
    if audit_path is None:
        audit_path = AUDIT_LOG_FILE
    else:
        audit_path = Path(audit_path)

    df = load_audit_log(audit_path)
    if df.empty:
        return False, "Audit log is empty."

    norm_req_id = request_id.strip()
    idx_matches = df[df["request_id"].str.strip() == norm_req_id].index

    if len(idx_matches) == 0:
        return False, f"Request ID '{request_id}' not found in audit log."

    idx = idx_matches[0]
    now_ts = datetime.now().isoformat(timespec="seconds")
    df.at[idx, "customer_response"] = response
    df.at[idx, "response_timestamp"] = now_ts

    df.to_csv(audit_path, index=False)
    return True, f"Request '{request_id}' status updated to '{response}' at {now_ts}."


# ==========================================
# MODULE 3: REQUEST EVALUATION ENGINE
# ==========================================

def evaluate_request(
    customer_name: Optional[str],
    agent_name: Optional[str],
    agent_id: Optional[str],
    action: Optional[str],
    amount: Optional[float],
    agents_dict: Dict[str, dict]
) -> EvaluationResult:
    """
    Evaluates an external AI agent's request against the 8 IndiGo business rules.

    Strict Order of Evaluation:
    1. Validation first (R8): Incomplete or invalid requests are BLOCKED.
    2. Check revoked status (R1): Revoked agents must always be BLOCKED.
       Ensures revoked agents can never bypass R1 even for View Fares or low amounts.
    3. Check unknown/unregistered status (R2): Unregistered agents are BLOCKED.
    4. Action rules:
       - R3: View Fares -> ALLOW
       - R4: Book Flight > 15,000 -> BLOCK
       - R5: Book Flight <= 15,000 -> ASK CUSTOMER
       - R6: Change Booking -> ASK CUSTOMER
       - R7: Request Refund -> ASK CUSTOMER
    """
    now_ts = datetime.now().isoformat(timespec="seconds")
    random_suffix = uuid.uuid4().hex[:6].upper()
    req_id = f"REQ-{datetime.now().strftime('%Y%m%d')}-{random_suffix}"

    # Sanitization
    c_name = customer_name.strip() if isinstance(customer_name, str) else ""
    a_name = agent_name.strip() if isinstance(agent_name, str) else ""
    a_id = agent_id.strip() if isinstance(agent_id, str) else ""
    act = action.strip() if isinstance(action, str) else ""

    # Validate amount
    amt = 0.0
    amount_valid = True
    try:
        if amount is not None:
            amt = float(amount)
            if amt < 0.0:
                amount_valid = False
        else:
            amount_valid = False
    except (ValueError, TypeError):
        amount_valid = False

    # -------------------------------------------------------------
    # STEP 1: VALIDATION CHECK (R8)
    # -------------------------------------------------------------
    if not c_name or not a_name or not a_id or act not in VALID_ACTIONS or not amount_valid:
        reasons = []
        if not c_name:
            reasons.append("Customer name missing")
        if not a_name:
            reasons.append("Agent name missing")
        if not a_id:
            reasons.append("Agent ID missing")
        if act not in VALID_ACTIONS:
            reasons.append(f"Invalid action '{act}'")
        if not amount_valid:
            reasons.append("Invalid or negative booking amount")

        explanation = f"Invalid or incomplete request: {', '.join(reasons)}. BLOCKED under Rule R8."
        return EvaluationResult(
            request_id=req_id,
            timestamp=now_ts,
            customer_name=c_name or "Unknown",
            agent_name=a_name or "Unknown",
            agent_id=a_id or "MISSING_ID",
            action=act or "None",
            amount=amt if amount_valid else -1.0,
            decision="BLOCK",
            rule_number="R8",
            rule_description=RULES_CATALOG["R8"]["description"],
            decision_explanation=explanation,
            customer_response="N/A"
        )

    # -------------------------------------------------------------
    # STEP 2: CHECK AGENT IDENTITY & STATUS (R1, R2)
    # -------------------------------------------------------------
    norm_agent_id = a_id.upper()
    registered_agent = agents_dict.get(norm_agent_id)

    # R1: Check Revoked Status FIRST - Revoked agents must NEVER bypass R1
    if registered_agent is not None:
        agent_status = registered_agent.get("status", "").upper()
        if agent_status == "REVOKED":
            revocation_time = registered_agent.get("revoked_at", "historical record")
            explanation = (
                f"Agent '{a_id}' ({registered_agent.get('agent_name', a_name)}) has been REVOKED "
                f"(revoked on: {revocation_time}). Revoked agents are strictly prohibited under Rule R1."
            )
            return EvaluationResult(
                request_id=req_id,
                timestamp=now_ts,
                customer_name=c_name,
                agent_name=a_name,
                agent_id=a_id,
                action=act,
                amount=amt,
                decision="BLOCK",
                rule_number="R1",
                rule_description=RULES_CATALOG["R1"]["description"],
                decision_explanation=explanation,
                customer_response="N/A"
            )
        elif agent_status != "ACTIVE":
            explanation = f"Agent status is '{agent_status}'. Unauthorized agent BLOCKED under Rule R1."
            return EvaluationResult(
                request_id=req_id,
                timestamp=now_ts,
                customer_name=c_name,
                agent_name=a_name,
                agent_id=a_id,
                action=act,
                amount=amt,
                decision="BLOCK",
                rule_number="R1",
                rule_description=RULES_CATALOG["R1"]["description"],
                decision_explanation=explanation,
                customer_response="N/A"
            )

    # R2: Check Unknown / Unregistered Status
    if registered_agent is None:
        explanation = (
            f"Agent ID '{a_id}' is unknown or not registered in the IndiGo Gatekeeper repository. "
            "Unregistered agents are strictly prohibited under Rule R2."
        )
        return EvaluationResult(
            request_id=req_id,
            timestamp=now_ts,
            customer_name=c_name,
            agent_name=a_name,
            agent_id=a_id,
            action=act,
            amount=amt,
            decision="BLOCK",
            rule_number="R2",
            rule_description=RULES_CATALOG["R2"]["description"],
            decision_explanation=explanation,
            customer_response="N/A"
        )

    # -------------------------------------------------------------
    # STRICT IDENTITY & OWNERSHIP VERIFICATION (RULE R2)
    # -------------------------------------------------------------
    # Verify submitted agent name matches registered agent name
    reg_agent_name = str(registered_agent.get("agent_name", "")).strip()
    if a_name.strip().lower() != reg_agent_name.lower():
        explanation = (
            f"Agent identity mismatch: Submitted agent name '{a_name}' does not match registered "
            f"agent name '{reg_agent_name}' for Agent ID '{a_id}'. Unauthorized or spoofed agent BLOCKED under Rule R2."
        )
        return EvaluationResult(
            request_id=req_id,
            timestamp=now_ts,
            customer_name=c_name,
            agent_name=a_name,
            agent_id=a_id,
            action=act,
            amount=amt,
            decision="BLOCK",
            rule_number="R2",
            rule_description=RULES_CATALOG["R2"]["description"],
            decision_explanation=explanation,
            customer_response="N/A"
        )

    # Verify customer ownership matches registered customer
    reg_customer_name = str(registered_agent.get("customer_name", "")).strip()
    if c_name.strip().lower() != reg_customer_name.lower():
        explanation = (
            f"Customer ownership mismatch: Submitted customer '{c_name}' does not match registered "
            f"owner '{reg_customer_name}' for Agent ID '{a_id}'. Unauthorized delegation BLOCKED under Rule R2."
        )
        return EvaluationResult(
            request_id=req_id,
            timestamp=now_ts,
            customer_name=c_name,
            agent_name=a_name,
            agent_id=a_id,
            action=act,
            amount=amt,
            decision="BLOCK",
            rule_number="R2",
            rule_description=RULES_CATALOG["R2"]["description"],
            decision_explanation=explanation,
            customer_response="N/A"
        )

    # -------------------------------------------------------------
    # STEP 3: ACTION SPECIFIC RULES (R3 - R7)
    # (Agent is verified REGISTERED and ACTIVE)
    # -------------------------------------------------------------

    # R3: View Fares
    if act == "View Fares":
        explanation = (
            f"Registered agent '{a_id}' is requesting to view flight fares (Amount: Rs. {amt:,.2f}). "
            "Informational requests carry zero financial commitment. ALLOWED under Rule R3."
        )
        return EvaluationResult(
            request_id=req_id,
            timestamp=now_ts,
            customer_name=c_name,
            agent_name=a_name,
            agent_id=a_id,
            action=act,
            amount=amt,
            decision="ALLOW",
            rule_number="R3",
            rule_description=RULES_CATALOG["R3"]["description"],
            decision_explanation=explanation,
            customer_response="N/A"
        )

    # R4 & R5: Book Flight
    if act == "Book Flight":
        if amt < BOOKING_LIMIT:
            explanation = (
                f"Flight booking amount of Rs. {amt:,.2f} is below Rs. {BOOKING_LIMIT:,.2f}. "
                "Automated standard booking is ALLOWED under Rule R4."
            )
            return EvaluationResult(
                request_id=req_id,
                timestamp=now_ts,
                customer_name=c_name,
                agent_name=a_name,
                agent_id=a_id,
                action=act,
                amount=amt,
                decision="ALLOW",
                rule_number="R4",
                rule_description=RULES_CATALOG["R4"]["description"],
                decision_explanation=explanation,
                customer_response="N/A"
            )
        else:
            explanation = (
                f"Flight booking amount of Rs. {amt:,.2f} is Rs. {BOOKING_LIMIT:,.2f} or above. "
                "Human-in-the-loop authorization required. ASK CUSTOMER under Rule R5."
            )
            return EvaluationResult(
                request_id=req_id,
                timestamp=now_ts,
                customer_name=c_name,
                agent_name=a_name,
                agent_id=a_id,
                action=act,
                amount=amt,
                decision="ASK CUSTOMER",
                rule_number="R5",
                rule_description=RULES_CATALOG["R5"]["description"],
                decision_explanation=explanation,
                customer_response="Pending"
            )

    # R6: Change Booking
    if act == "Change Booking":
        explanation = (
            "Booking modification impacts flight itineraries and may incur fare differences. "
            "Customer authorization required. ASK CUSTOMER under Rule R6."
        )
        return EvaluationResult(
            request_id=req_id,
            timestamp=now_ts,
            customer_name=c_name,
            agent_name=a_name,
            agent_id=a_id,
            action=act,
            amount=amt,
            decision="ASK CUSTOMER",
            rule_number="R6",
            rule_description=RULES_CATALOG["R6"]["description"],
            decision_explanation=explanation,
            customer_response="Pending"
        )

    # R7: Request Refund
    if act == "Request Refund":
        explanation = (
            f"Refund request of Rs. {amt:,.2f} initiates financial reversal on customer account. "
            "Direct customer confirmation required. ASK CUSTOMER under Rule R7."
        )
        return EvaluationResult(
            request_id=req_id,
            timestamp=now_ts,
            customer_name=c_name,
            agent_name=a_name,
            agent_id=a_id,
            action=act,
            amount=amt,
            decision="ASK CUSTOMER",
            rule_number="R7",
            rule_description=RULES_CATALOG["R7"]["description"],
            decision_explanation=explanation,
            customer_response="Pending"
        )

    # Fallback to R8 if any unanticipated edge case occurs
    return EvaluationResult(
        request_id=req_id,
        timestamp=now_ts,
        customer_name=c_name,
        agent_name=a_name,
        agent_id=a_id,
        action=act,
        amount=amt,
        decision="BLOCK",
        rule_number="R8",
        rule_description=RULES_CATALOG["R8"]["description"],
        decision_explanation="Unhandled or invalid request scenario. BLOCKED under Rule R8.",
        customer_response="N/A"
    )


# ==========================================
# MODULE 7: AUTOMATED TEST SUITE ENGINE
# ==========================================

def get_isolated_test_agents() -> Dict[str, dict]:
    """Provides isolated mock agent registry for testing to prevent side-effects."""
    return {
        "TEST-REG-ACTIVE": {
            "agent_id": "TEST-REG-ACTIVE",
            "agent_name": "Test Active Agent",
            "customer_name": "Adarsh Sharma",
            "registered_at": "2026-11-20T10:00:00",
            "status": "ACTIVE",
            "revoked_at": None
        },
        "TEST-REG-REVOKED": {
            "agent_id": "TEST-REG-REVOKED",
            "agent_name": "Test Revoked Agent",
            "customer_name": "Vikram Malhotra",
            "registered_at": "2026-11-19T08:00:00",
            "status": "REVOKED",
            "revoked_at": "2026-11-20T09:00:00"
        }
    }


def run_automated_tests() -> List[dict]:
    """
    Executes the six required automated test scenarios against the actual decision engine.
    Uses isolated mock data so actual audit log and agents file remain unpolluted.
    """
    mock_agents = get_isolated_test_agents()

    scenarios = [
        {
            "test_number": 1,
            "title": "Registered agent, View Fares, Rs. 0",
            "customer_name": "Adarsh Sharma",
            "agent_name": "Test Active Agent",
            "agent_id": "TEST-REG-ACTIVE",
            "action": "View Fares",
            "amount": 0.0,
            "expected_decision": "ALLOW",
            "expected_rule": "R3"
        },
        {
            "test_number": 2,
            "title": "Unknown agent, Book Flight, Rs. 5,000",
            "customer_name": "Unknown Customer",
            "agent_name": "Ghost Bot",
            "agent_id": "TEST-UNKNOWN-999",
            "action": "Book Flight",
            "amount": 5000.0,
            "expected_decision": "BLOCK",
            "expected_rule": "R2"
        },
        {
            "test_number": 3,
            "title": "Registered agent, Book Flight, Rs. 20,000 (>= Rs. 15,000)",
            "customer_name": "Adarsh Sharma",
            "agent_name": "Test Active Agent",
            "agent_id": "TEST-REG-ACTIVE",
            "action": "Book Flight",
            "amount": 20000.0,
            "expected_decision": "ASK CUSTOMER",
            "expected_rule": "R5"
        },
        {
            "test_number": 4,
            "title": "Registered agent, Book Flight, Rs. 10,000 (< Rs. 15,000)",
            "customer_name": "Adarsh Sharma",
            "agent_name": "Test Active Agent",
            "agent_id": "TEST-REG-ACTIVE",
            "action": "Book Flight",
            "amount": 10000.0,
            "expected_decision": "ALLOW",
            "expected_rule": "R4"
        },
        {
            "test_number": 5,
            "title": "Revoked agent, View Fares, Rs. 0",
            "customer_name": "Vikram Malhotra",
            "agent_name": "Test Revoked Agent",
            "agent_id": "TEST-REG-REVOKED",
            "action": "View Fares",
            "amount": 0.0,
            "expected_decision": "BLOCK",
            "expected_rule": "R1"
        },
        {
            "test_number": 6,
            "title": "Registered agent, Request Refund, Rs. 5,000",
            "customer_name": "Adarsh Sharma",
            "agent_name": "Test Active Agent",
            "agent_id": "TEST-REG-ACTIVE",
            "action": "Request Refund",
            "amount": 5000.0,
            "expected_decision": "ASK CUSTOMER",
            "expected_rule": "R7"
        },
        {
            "test_number": 7,
            "title": "Agent Name Mismatch (Spoofing Attempt), Rs. 0",
            "customer_name": "Adarsh Sharma",
            "agent_name": "Unknown Travel AI",
            "agent_id": "TEST-REG-ACTIVE",
            "action": "View Fares",
            "amount": 0.0,
            "expected_decision": "BLOCK",
            "expected_rule": "R2"
        },
        {
            "test_number": 8,
            "title": "Customer Ownership Mismatch (Hijacking Attempt), Rs. 0",
            "customer_name": "Unauthorized Customer",
            "agent_name": "Test Active Agent",
            "agent_id": "TEST-REG-ACTIVE",
            "action": "View Fares",
            "amount": 0.0,
            "expected_decision": "BLOCK",
            "expected_rule": "R2"
        }
    ]

    results = []
    for sc in scenarios:
        res = evaluate_request(
            customer_name=sc["customer_name"],
            agent_name=sc["agent_name"],
            agent_id=sc["agent_id"],
            action=sc["action"],
            amount=sc["amount"],
            agents_dict=mock_agents
        )

        decision_pass = (res.decision == sc["expected_decision"])
        rule_pass = (res.rule_number == sc["expected_rule"])
        passed = decision_pass and rule_pass

        results.append({
            "test_number": sc["test_number"],
            "title": sc["title"],
            "input_scenario": f"Customer: {sc['customer_name']} | Agent: {sc['agent_id']} | Action: {sc['action']} | Amount: Rs. {sc['amount']:,.2f}",
            "expected_decision": sc["expected_decision"],
            "expected_rule": sc["expected_rule"],
            "actual_decision": res.decision,
            "actual_rule": res.rule_number,
            "passed": passed,
            "explanation": res.decision_explanation,
            "timestamp": res.timestamp
        })

    return results
