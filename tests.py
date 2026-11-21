"""
AGENT GATEKEEPER – INDIGO EDITION
Automated Verification Suite (tests.py)

STUDENT DETAILS:
- Enrolment Number: PGD202566590
- Company: IndiGo Airlines
- Project: AI Agent Authorization System

Test suite containing exactly six pytest-discoverable test functions
evaluating the authorization decision engine against the academic test matrix.
Uses isolated in-memory test data to prevent modifying persistent audit records.

Run via:
    py -3.14 -m pytest -v tests.py
or:
    py -3.14 tests.py
"""

import sys
from gatekeeper_engine import evaluate_request, get_isolated_test_agents


# -----------------------------------------------------------------------------
# TEST FIXTURE (Isolated in-memory test data)
# -----------------------------------------------------------------------------
def get_test_fixture():
    """Returns isolated mock agents dictionary preventing real audit log side effects."""
    return get_isolated_test_agents()


# -----------------------------------------------------------------------------
# EXACTLY SIX PYTEST DISCOVERABLE TEST FUNCTIONS
# -----------------------------------------------------------------------------

def test_1_registered_agent_view_fares_allow_r3():
    """
    TEST 1:
    Scenario: Registered active agent requests to View Fares (Rs. 0).
    Expected Decision: ALLOW
    Expected Rule: R3
    Rationale: Informational query with zero financial commitment.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Adarsh Sharma",
        agent_name="Test Active Agent",
        agent_id="TEST-REG-ACTIVE",
        action="View Fares",
        amount=0.0,
        agents_dict=mock_agents
    )

    assert result.decision == "ALLOW", f"Expected ALLOW but got {result.decision}"
    assert result.rule_number == "R3", f"Expected R3 but got {result.rule_number}"
    assert "ALLOWED under Rule R3" in result.decision_explanation


def test_2_unknown_agent_booking_block_r2():
    """
    TEST 2:
    Scenario: Unknown/unregistered agent attempts to Book Flight (Rs. 5,000).
    Expected Decision: BLOCK
    Expected Rule: R2
    Rationale: Zero-trust security blocks unregistered agent IDs.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Unknown Customer",
        agent_name="Ghost Bot",
        agent_id="TEST-UNKNOWN-999",
        action="Book Flight",
        amount=5000.0,
        agents_dict=mock_agents
    )

    assert result.decision == "BLOCK", f"Expected BLOCK but got {result.decision}"
    assert result.rule_number == "R2", f"Expected R2 but got {result.rule_number}"
    assert "Rule R2" in result.decision_explanation


def test_3_registered_agent_booking_above_15k_block_r4():
    """
    TEST 3:
    Scenario: Registered agent attempts to Book Flight exceeding limit (Rs. 20,000).
    Expected Decision: BLOCK
    Expected Rule: R4
    Rationale: High-value automated booking above Rs. 15,000 threshold must be blocked.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Adarsh Sharma",
        agent_name="Test Active Agent",
        agent_id="TEST-REG-ACTIVE",
        action="Book Flight",
        amount=20000.0,
        agents_dict=mock_agents
    )

    assert result.decision == "BLOCK", f"Expected BLOCK but got {result.decision}"
    assert result.rule_number == "R4", f"Expected R4 but got {result.rule_number}"
    assert "Rule R4" in result.decision_explanation


def test_4_registered_agent_booking_below_15k_ask_customer_r5():
    """
    TEST 4:
    Scenario: Registered agent attempts to Book Flight within limit (Rs. 10,000).
    Expected Decision: ASK CUSTOMER
    Expected Rule: R5
    Rationale: Bookings of Rs. 15,000 or below require direct customer authorization.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Adarsh Sharma",
        agent_name="Test Active Agent",
        agent_id="TEST-REG-ACTIVE",
        action="Book Flight",
        amount=10000.0,
        agents_dict=mock_agents
    )

    assert result.decision == "ASK CUSTOMER", f"Expected ASK CUSTOMER but got {result.decision}"
    assert result.rule_number == "R5", f"Expected R5 but got {result.rule_number}"
    assert result.customer_response == "Pending"
    assert "Rule R5" in result.decision_explanation


def test_5_revoked_agent_view_fares_block_r1():
    """
    TEST 5:
    Scenario: Revoked agent attempts to View Fares (Rs. 0).
    Expected Decision: BLOCK
    Expected Rule: R1
    Rationale: Revoked agents must never bypass Rule R1, even for zero-cost fare lookups.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Vikram Malhotra",
        agent_name="Test Revoked Agent",
        agent_id="TEST-REG-REVOKED",
        action="View Fares",
        amount=0.0,
        agents_dict=mock_agents
    )

    assert result.decision == "BLOCK", f"Expected BLOCK but got {result.decision}"
    assert result.rule_number == "R1", f"Expected R1 but got {result.rule_number}"
    assert "REVOKED" in result.decision_explanation
    assert "Rule R1" in result.decision_explanation


def test_6_registered_agent_request_refund_ask_customer_r7():
    """
    TEST 6:
    Scenario: Registered agent requests a refund (Rs. 5,000).
    Expected Decision: ASK CUSTOMER
    Expected Rule: R7
    Rationale: Financial refund requests initiate fund reversal and require customer approval.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Adarsh Sharma",
        agent_name="Test Active Agent",
        agent_id="TEST-REG-ACTIVE",
        action="Request Refund",
        amount=5000.0,
        agents_dict=mock_agents
    )

    assert result.decision == "ASK CUSTOMER", f"Expected ASK CUSTOMER but got {result.decision}"
    assert result.rule_number == "R7", f"Expected R7 but got {result.rule_number}"
    assert result.customer_response == "Pending"
    assert "Rule R7" in result.decision_explanation


def test_7_agent_name_mismatch_block_r2():
    """
    TEST 7:
    Scenario: Registered Agent ID with unknown/mismatched agent name.
    Expected Decision: BLOCK
    Expected Rule: R2
    Rationale: Prevents bot spoofing and unauthorized agent identity impersonation.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Adarsh Sharma",
        agent_name="Unknown Travel AI",  # Mismatched agent name
        agent_id="TEST-REG-ACTIVE",
        action="View Fares",
        amount=0.0,
        agents_dict=mock_agents
    )

    assert result.decision == "BLOCK", f"Expected BLOCK but got {result.decision}"
    assert result.rule_number == "R2", f"Expected R2 but got {result.rule_number}"
    assert "Agent identity mismatch" in result.decision_explanation
    assert "Rule R2" in result.decision_explanation


def test_8_customer_ownership_mismatch_block_r2():
    """
    TEST 8:
    Scenario: Registered Agent ID with unknown/mismatched customer name.
    Expected Decision: BLOCK
    Expected Rule: R2
    Rationale: Prevents cross-customer agent hijacking and unauthorized delegation.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Unauthorized Customer",  # Mismatched customer name
        agent_name="Test Active Agent",
        agent_id="TEST-REG-ACTIVE",
        action="View Fares",
        amount=0.0,
        agents_dict=mock_agents
    )

    assert result.decision == "BLOCK", f"Expected BLOCK but got {result.decision}"
    assert result.rule_number == "R2", f"Expected R2 but got {result.rule_number}"
    assert "Customer ownership mismatch" in result.decision_explanation
    assert "Rule R2" in result.decision_explanation


def test_9_revoked_agent_with_mismatch_still_blocked_r1():
    """
    TEST 9:
    Scenario: Revoked agent attempted with mismatched agent or customer name.
    Expected Decision: BLOCK
    Expected Rule: R1
    Rationale: Revoked agents must always be BLOCKED under R1 with highest priority.
    """
    mock_agents = get_test_fixture()
    result = evaluate_request(
        customer_name="Random User",
        agent_name="Unknown Bot",
        agent_id="TEST-REG-REVOKED",
        action="View Fares",
        amount=0.0,
        agents_dict=mock_agents
    )

    assert result.decision == "BLOCK", f"Expected BLOCK but got {result.decision}"
    assert result.rule_number == "R1", f"Expected R1 but got {result.rule_number}"
    assert "Rule R1" in result.decision_explanation


# -----------------------------------------------------------------------------
# DIRECT EXECUTION SUPPORT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        import pytest
        sys.exit(pytest.main(["-v", __file__]))
    except ImportError:
        # Fallback runner if pytest is executed as raw python
        tests = [
            test_1_registered_agent_view_fares_allow_r3,
            test_2_unknown_agent_booking_block_r2,
            test_3_registered_agent_booking_above_15k_block_r4,
            test_4_registered_agent_booking_below_15k_ask_customer_r5,
            test_5_revoked_agent_view_fares_block_r1,
            test_6_registered_agent_request_refund_ask_customer_r7,
            test_7_agent_name_mismatch_block_r2,
            test_8_customer_ownership_mismatch_block_r2,
            test_9_revoked_agent_with_mismatch_still_blocked_r1,
        ]
        print(f"Running {len(tests)} tests...")
        for test in tests:
            test()
            print(f"[PASS] {test.__name__}")
        print("All tests passed successfully!")
