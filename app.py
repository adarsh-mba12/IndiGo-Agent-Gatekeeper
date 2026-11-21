"""
AGENT GATEKEEPER – INDIGO EDITION
Interactive Web Dashboard & AI Agent Authorization System

STUDENT DETAILS:
- Enrolment Number: PGD202566590
- Company: IndiGo Airlines
- Project: AI Agent Authorization System

Built with Streamlit, Python 3.14, and Pandas.
"""

import os
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

import gatekeeper_engine as engine

# Establish Project Root and Data Paths via pathlib
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
AUDIT_LOG_FILE = DATA_DIR / "audit_log.csv"
AGENTS_FILE = DATA_DIR / "agents.json"

# -----------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agent Gatekeeper – IndiGo Edition",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM AIRLINE-THEMED CSS STYLING
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* Global Styles */
    :root {
        --indigo-navy: #001b94;
        --indigo-blue: #0044cc;
        --sky-blue: #e8f0fe;
        --light-bg: #f8fafc;
        --card-border: #e2e8f0;
        --text-dark: #0f172a;
    }

    /* Top Header Branding */
    .brand-header {
        background: linear-gradient(135deg, #001b94 0%, #0033aa 60%, #0052cc 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(0, 27, 148, 0.15);
    }
    .brand-header h1 {
        color: white !important;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .brand-header p {
        color: #dbeafe !important;
        margin: 6px 0 0 0;
        font-size: 15px;
    }
    .student-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.35);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 10px;
        color: #ffffff;
    }

    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 14px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: white;
        border: 1px solid var(--card-border);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0, 27, 148, 0.08);
    }
    .kpi-title {
        font-size: 12px;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        margin-top: 6px;
        color: var(--indigo-navy);
    }
    .kpi-value.allow { color: #059669; }
    .kpi-value.ask { color: #d97706; }
    .kpi-value.block { color: #dc2626; }

    /* Decision Indicators */
    .decision-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.5px;
        text-align: center;
    }
    .badge-allow {
        background-color: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }
    .badge-ask {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    .badge-block {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }
    .badge-active {
        background-color: #e0e7ff;
        color: #3730a3;
        border: 1px solid #c7d2fe;
    }
    .badge-revoked {
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
    }

    /* Decision Hero Banner */
    .decision-hero {
        padding: 20px 24px;
        border-radius: 12px;
        margin: 20px 0;
        border-left: 6px solid;
    }
    .hero-allow {
        background-color: #ecfdf5;
        border-color: #10b981;
        color: #064e3b;
    }
    .hero-ask {
        background-color: #fffbeb;
        border-color: #f59e0b;
        color: #78350f;
    }
    .hero-block {
        background-color: #fef2f2;
        border-color: #ef4444;
        color: #7f1d1d;
    }

    /* Sidebar info box */
    .sidebar-info {
        background: #f1f5f9;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid var(--indigo-navy);
        font-size: 12px;
        margin-top: 14px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DATA REPOSITORIES & SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
def init_session_state():
    """Initializes session state tracking."""
    if "current_eval" not in st.session_state:
        st.session_state.current_eval = None
    if "eval_msg" not in st.session_state:
        st.session_state.eval_msg = None


init_session_state()


# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & BRANDING
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 12px; border-bottom: 1px solid #e2e8f0;">
            <div style="font-size: 36px; line-height: 1;">✈️</div>
            <h2 style="color: #001b94; margin: 4px 0 0 0; font-size: 20px; font-weight: 800;">IndiGo Airlines</h2>
            <div style="color: #64748b; font-size: 13px; font-weight: 600;">AGENT GATEKEEPER</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-info">
            <b>ACADEMIC PROTOTYPE</b><br>
            <b>Enrolment:</b> PGD202566590<br>
            <b>Company:</b> IndiGo Airlines<br>
            <b>Project:</b> AI Agent Authorization System
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    menu_option = st.radio(
        "NAVIGATION MENU",
        options=[
            "📊 Dashboard",
            "📝 Agent Registration",
            "🛡️ Request Evaluation",
            "🤝 Customer Confirmation",
            "🚫 Agent Revocation",
            "📜 Audit Log",
            "🧪 Test Centre"
        ],
        index=0
    )

    st.markdown("---")

    # Quick Stats in Sidebar
    agents_list = engine.load_agents(AGENTS_FILE)
    audit_df = engine.load_audit_log(AUDIT_LOG_FILE)
    active_count = sum(1 for a in agents_list if a.get("status") == "ACTIVE")
    revoked_count = sum(1 for a in agents_list if a.get("status") == "REVOKED")
    pending_conf_count = len(audit_df[audit_df["customer_response"] == "Pending"]) if not audit_df.empty else 0

    st.caption("GATEWAY METRICS")
    st.write(f"• **Active Agents:** {active_count}")
    st.write(f"• **Revoked Agents:** {revoked_count}")
    st.write(f"• **Total Audit Records:** {len(audit_df)}")
    if pending_conf_count > 0:
        st.warning(f"⚠️ {pending_conf_count} Confirmation(s) Pending")

    st.markdown("---")
    st.caption("DISCLAIMER: Academic simulation prototype. No real IndiGo reservation or financial transactions are performed.")


# -----------------------------------------------------------------------------
# GLOBAL HEADER BAR
# -----------------------------------------------------------------------------
def render_header(subtitle: str):
    st.markdown(f"""
        <div class="brand-header">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <h1>✈️ AGENT GATEKEEPER – INDIGO EDITION</h1>
                    <p>{subtitle}</p>
                </div>
                <div style="text-align: right;">
                    <span class="student-badge">ENROLMENT: PGD202566590</span>
                    <div style="color: #93c5fd; font-size: 11px; margin-top: 4px;">IndiGo AI Agent Authorization Gateway</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MODULE 1: DASHBOARD
# -----------------------------------------------------------------------------
if menu_option == "📊 Dashboard":
    render_header("Executive Operational Dashboard & Zero-Trust Agent Authorization Metrics")

    agents_list = engine.load_agents(AGENTS_FILE)
    audit_df = engine.load_audit_log(AUDIT_LOG_FILE)

    total_agents = len(agents_list)
    active_agents = sum(1 for a in agents_list if a.get("status") == "ACTIVE")
    revoked_agents = sum(1 for a in agents_list if a.get("status") == "REVOKED")

    total_requests = len(audit_df)
    allow_count = len(audit_df[audit_df["decision"] == "ALLOW"]) if not audit_df.empty else 0
    ask_count = len(audit_df[audit_df["decision"] == "ASK CUSTOMER"]) if not audit_df.empty else 0
    block_count = len(audit_df[audit_df["decision"] == "BLOCK"]) if not audit_df.empty else 0

    # KPI Metrics Row
    st.markdown("""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-title">Total Agents</div>
                <div class="kpi-value">{total_agents}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Active Agents</div>
                <div class="kpi-value" style="color: #001b94;">{active_agents}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Revoked Agents</div>
                <div class="kpi-value" style="color: #475569;">{revoked_agents}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Requests</div>
                <div class="kpi-value">{total_requests}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">ALLOW Count</div>
                <div class="kpi-value allow">{allow_count}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">ASK CUSTOMER</div>
                <div class="kpi-value ask">{ask_count}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">BLOCK Count</div>
                <div class="kpi-value block">{block_count}</div>
            </div>
        </div>
    """.format(
        total_agents=total_agents,
        active_agents=active_agents,
        revoked_agents=revoked_agents,
        total_requests=total_requests,
        allow_count=allow_count,
        ask_count=ask_count,
        block_count=block_count
    ), unsafe_allow_html=True)

    # Visual Analytics & Recent Activity
    col_chart, col_recent = st.columns([1, 1])

    with col_chart:
        st.subheader("📊 Authorization Decision Distribution")
        if total_requests > 0:
            decision_counts = audit_df["decision"].value_counts().reset_index()
            decision_counts.columns = ["Decision", "Count"]
            st.bar_chart(decision_counts.set_index("Decision"), color="#001b94")
        else:
            st.info("No request logs recorded yet. Submit evaluation requests to populate metrics.")

        st.subheader("📋 Policy Rules Summary")
        st.markdown("""
        - **R1:** Revoked agents must always be **BLOCKED**.
        - **R2:** Unknown or unregistered agents must always be **BLOCKED**.
        - **R3:** Registered agents requesting to view fares must be **ALLOWED**.
        - **R4:** Flight booking below Rs. 15,000 is **ALLOWED**.
        - **R5:** Flight booking of Rs. 15,000 and above must return **ASK CUSTOMER**.
        - **R6:** Change booking must return **ASK CUSTOMER**.
        - **R7:** Refund requests must return **ASK CUSTOMER**.
        - **R8:** Invalid or incomplete requests must be **BLOCKED**.
        """)

    with col_recent:
        st.subheader("🕒 Recent Authorization Requests")
        if not audit_df.empty:
            recent_df = audit_df.tail(6).iloc[::-1][
                ["request_id", "timestamp", "agent_id", "action", "amount", "decision", "rule_number"]
            ]
            st.dataframe(
                recent_df,
                hide_index=True,
                column_config={
                    "request_id": "Request ID",
                    "timestamp": "Timestamp",
                    "agent_id": "Agent ID",
                    "action": "Action",
                    "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                    "decision": "Decision",
                    "rule_number": "Rule"
                }
            )
        else:
            st.info("No requests evaluated yet.")

        # Pending Confirmation Alert Card
        pending_records = audit_df[audit_df["customer_response"] == "Pending"] if not audit_df.empty else pd.DataFrame()
        if not pending_records.empty:
            st.warning(f"⚡ **{len(pending_records)} Request(s) Awaiting Customer Authorization.** Navigate to **Customer Confirmation** to review.")


# -----------------------------------------------------------------------------
# MODULE 2: AGENT REGISTRATION
# -----------------------------------------------------------------------------
elif menu_option == "📝 Agent Registration":
    render_header("Register External AI Agents into IndiGo Trust Repository")

    st.markdown("""
        External AI agents (such as personal travel assistants, corporate booking bots, or meta-search agents)
        must be formally registered and assigned an authorization identity before interacting with IndiGo Gatekeeper.
    """)

    col_form, col_list = st.columns([1, 1])

    with col_form:
        st.subheader("Register New AI Agent")
        with st.form("agent_registration_form", clear_on_submit=False):
            reg_customer = st.text_input("Customer Name *", placeholder="e.g. Adarsh Sharma")
            reg_agent_name = st.text_input("Agent Name *", placeholder="e.g. FlightWise AI")
            reg_agent_id = st.text_input("Unique Agent ID *", placeholder="e.g. 6E-AGT-104")
            st.text_input("Initial Permission Status", value="ACTIVE", disabled=True)
            st.caption("Note: Agent ID must be unique. Duplicate IDs will be rejected.")

            submitted = st.form_submit_button("Register Agent", type="primary")

            if submitted:
                success, msg, new_agent = engine.register_agent(
                    customer_name=reg_customer,
                    agent_name=reg_agent_name,
                    agent_id=reg_agent_id
                )
                if success:
                    st.success(f"✅ {msg}")
                    st.toast(f"Agent {reg_agent_id} registered successfully!", icon="✈️")
                else:
                    st.error(f"❌ {msg}")

    with col_list:
        st.subheader("Registered Agents Directory")
        current_agents = engine.load_agents(AGENTS_FILE)
        if current_agents:
            df_agents = pd.DataFrame(current_agents)
            st.dataframe(
                df_agents[["agent_id", "agent_name", "customer_name", "status", "registered_at"]],
                hide_index=True,
                column_config={
                    "agent_id": "Agent ID",
                    "agent_name": "Agent Name",
                    "customer_name": "Owner / Customer",
                    "status": "Permission Status",
                    "registered_at": "Registration Time"
                }
            )
        else:
            st.info("No agents registered yet.")


# -----------------------------------------------------------------------------
# MODULE 3: REQUEST EVALUATION
# -----------------------------------------------------------------------------
elif menu_option == "🛡️ Request Evaluation":
    render_header("AI Agent Request Evaluation Engine")

    st.markdown("""
        Submit and evaluate transactions requested by an external AI agent. The Gatekeeper applies
        strict zero-trust validation and business policies (R1 to R8) to decide **ALLOW**, **ASK CUSTOMER**, or **BLOCK**.
    """)

    agents_dict = engine.get_agents_dict()
    agents_list = engine.load_agents()

    # Preset Quick-Load Scenarios for easy testing
    with st.expander("⚡ Quick-Load Test Scenario Presets (Optional)"):
        p_row1 = st.columns(4)
        if p_row1[0].button("Test 1 (R3: Fares)"):
            st.session_state.quick_customer = "Adarsh Sharma"
            st.session_state.quick_agent_name = "SkyTravel AI"
            st.session_state.quick_agent_id = "6E-AGT-101"
            st.session_state.quick_action = "View Fares"
            st.session_state.quick_amount = 0.0
        if p_row1[1].button("Test 2 (R2: Unknown)"):
            st.session_state.quick_customer = "Ghost User"
            st.session_state.quick_agent_name = "GhostBot"
            st.session_state.quick_agent_id = "UNKNOWN-BOT-99"
            st.session_state.quick_action = "Book Flight"
            st.session_state.quick_amount = 5000.0
        if p_row1[2].button("Test 3 (R5: >=15k)"):
            st.session_state.quick_customer = "Adarsh Sharma"
            st.session_state.quick_agent_name = "SkyTravel AI"
            st.session_state.quick_agent_id = "6E-AGT-101"
            st.session_state.quick_action = "Book Flight"
            st.session_state.quick_amount = 20000.0
        if p_row1[3].button("Test 4 (R4: <15k)"):
            st.session_state.quick_customer = "Adarsh Sharma"
            st.session_state.quick_agent_name = "SkyTravel AI"
            st.session_state.quick_agent_id = "6E-AGT-101"
            st.session_state.quick_action = "Book Flight"
            st.session_state.quick_amount = 10000.0

        p_row2 = st.columns(4)
        if p_row2[0].button("Test 5 (R1: Revoked)"):
            st.session_state.quick_customer = "Vikram Malhotra"
            st.session_state.quick_agent_name = "Rogue TravelBot"
            st.session_state.quick_agent_id = "6E-AGT-999"
            st.session_state.quick_action = "View Fares"
            st.session_state.quick_amount = 0.0
        if p_row2[1].button("Test 6 (R7: Refund)"):
            st.session_state.quick_customer = "Adarsh Sharma"
            st.session_state.quick_agent_name = "SkyTravel AI"
            st.session_state.quick_agent_id = "6E-AGT-101"
            st.session_state.quick_action = "Request Refund"
            st.session_state.quick_amount = 5000.0
        if p_row2[2].button("Test 7 (R2: Spoofed Agent)"):
            st.session_state.quick_customer = "Adarsh Sharma"
            st.session_state.quick_agent_name = "Unknown Travel AI"
            st.session_state.quick_agent_id = "6E-AGT-101"
            st.session_state.quick_action = "View Fares"
            st.session_state.quick_amount = 0.0
        if p_row2[3].button("Test 8 (R2: Owner Mismatch)"):
            st.session_state.quick_customer = "Unauthorized Customer"
            st.session_state.quick_agent_name = "SkyTravel AI"
            st.session_state.quick_agent_id = "6E-AGT-101"
            st.session_state.quick_action = "View Fares"
            st.session_state.quick_amount = 0.0

    eval_col1, eval_col2 = st.columns([1, 1])

    with eval_col1:
        st.subheader("Transaction Evaluation Form")

        # Prepopulate if preset was selected
        default_customer = st.session_state.get("quick_customer", "Adarsh Sharma")
        default_agent_name = st.session_state.get("quick_agent_name", "SkyTravel AI")
        default_agent_id = st.session_state.get("quick_agent_id", "6E-AGT-101")
        default_action = st.session_state.get("quick_action", "View Fares")
        default_amount = st.session_state.get("quick_amount", 0.0)

        with st.form("request_evaluation_form"):
            in_customer = st.text_input("Customer Name", value=default_customer)
            in_agent_name = st.text_input("Agent Name", value=default_agent_name)
            in_agent_id = st.text_input("Agent ID", value=default_agent_id, help="Enter exact registered Agent ID or any unknown ID to test R2.")

            action_index = engine.VALID_ACTIONS.index(default_action) if default_action in engine.VALID_ACTIONS else 0
            in_action = st.selectbox("Requested Action", options=engine.VALID_ACTIONS, index=action_index)
            in_amount = st.number_input(
                "Booking Amount in INR (₹)",
                min_value=0.0,
                max_value=1000000.0,
                value=float(default_amount),
                step=500.0,
                help="Applies to flight bookings and refunds. Rs. 0 for View Fares."
            )

            btn_evaluate = st.form_submit_button("Evaluate Request", type="primary")

            if btn_evaluate:
                eval_result = engine.evaluate_request(
                    customer_name=in_customer,
                    agent_name=in_agent_name,
                    agent_id=in_agent_id,
                    action=in_action,
                    amount=in_amount,
                    agents_dict=agents_dict
                )
                engine.log_audit_record(eval_result)
                st.session_state.current_eval = eval_result
                st.toast(f"Decision: {eval_result.decision} ({eval_result.rule_number})", icon="🛡️")

    with eval_col2:
        st.subheader("Authorization Decision Outcome")

        curr = st.session_state.current_eval
        if curr:
            hero_class = "hero-allow" if curr.decision == "ALLOW" else ("hero-ask" if curr.decision == "ASK CUSTOMER" else "hero-block")
            badge_class = "badge-allow" if curr.decision == "ALLOW" else ("badge-ask" if curr.decision == "ASK CUSTOMER" else "badge-block")
            icon = "✅" if curr.decision == "ALLOW" else ("⚠️" if curr.decision == "ASK CUSTOMER" else "🛑")

            st.markdown(f"""
                <div class="decision-hero {hero_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 22px; font-weight: 800;">{icon} {curr.decision}</span>
                        <span class="decision-badge {badge_class}">RULE {curr.rule_number}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 14px; font-weight: 600;">
                        {curr.rule_description}
                    </div>
                    <div style="margin-top: 8px; font-size: 13px;">
                        <b>Explanation:</b> {curr.decision_explanation}
                    </div>
                    <hr style="margin: 12px 0; border: 0; border-top: 1px solid rgba(0,0,0,0.1);">
                    <div style="font-size: 12px; color: #475569;">
                        <b>Request ID:</b> <code>{curr.request_id}</code> | <b>Timestamp:</b> {curr.timestamp}<br>
                        <b>Agent:</b> {curr.agent_id} ({curr.agent_name}) | <b>Action:</b> {curr.action} (₹{curr.amount:,.2f})
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # In-line Customer Confirmation Prompt for ASK CUSTOMER
            if curr.decision == "ASK CUSTOMER":
                st.markdown("#### 🤝 Simulated Customer Authorization Required")
                st.info("The external agent's request requires direct approval from the customer before execution.")

                col_approve, col_reject = st.columns(2)
                with col_approve:
                    if st.button("👍 Approve Request", type="primary", key="inline_approve"):
                        engine.update_customer_response(curr.request_id, "Approved")
                        st.session_state.current_eval.customer_response = "Approved"
                        st.success(f"Customer approved request {curr.request_id} successfully!")
                        st.rerun()

                with col_reject:
                    if st.button("👎 Reject Request", type="secondary", key="inline_reject"):
                        engine.update_customer_response(curr.request_id, "Rejected")
                        st.session_state.current_eval.customer_response = "Rejected"
                        st.error(f"Customer rejected request {curr.request_id}.")
                        st.rerun()

                st.write(f"**Current Status:** `{curr.customer_response}`")
        else:
            st.info("Fill out the form on the left and click **Evaluate Request** to view real-time authorization analysis.")


# -----------------------------------------------------------------------------
# MODULE 4: CUSTOMER CONFIRMATION
# -----------------------------------------------------------------------------
elif menu_option == "🤝 Customer Confirmation":
    render_header("Customer Authorization Simulation & Confirmation Queue")

    st.markdown("""
        Under policy rules **R5**, **R6**, and **R7**, sensitive or financial transactions trigger an **ASK CUSTOMER**
        decision. This module allows the customer to review pending agent requests and grant or deny approval.
        *(Academic simulation: No financial transactions or airline seat reservations are executed.)*
    """)

    audit_df = engine.load_audit_log(AUDIT_LOG_FILE)
    pending_df = audit_df[audit_df["customer_response"] == "Pending"] if not audit_df.empty else pd.DataFrame()

    tab_pending, tab_history = st.tabs(["Pending Approvals Queue", "Confirmation History"])

    with tab_pending:
        st.subheader(f"Pending Requests Awaiting Customer Decision ({len(pending_df)})")

        if pending_df.empty:
            st.success("🎉 No requests are currently pending customer authorization.")
        else:
            for _, row in pending_df.iterrows():
                req_id = row["request_id"]
                with st.expander(f"⚠️ {row['action']} - ₹{float(row['amount']):,.2f} | Agent: {row['agent_id']} ({req_id})", expanded=True):
                    c1, c2, c3 = st.columns([2, 1, 1])
                    with c1:
                        st.write(f"• **Customer:** {row['customer_name']}")
                        st.write(f"• **Agent:** {row['agent_name']} (`{row['agent_id']}`)")
                        st.write(f"• **Action:** {row['action']} (Amount: ₹{float(row['amount']):,.2f})")
                        st.write(f"• **Triggered Rule:** `{row['rule_number']}` ({row['decision_explanation']})")
                        st.write(f"• **Initiated At:** {row['timestamp']}")

                    with c2:
                        if st.button("✅ Approve", key=f"app_{req_id}", type="primary"):
                            engine.update_customer_response(req_id, "Approved")
                            st.success(f"Approved {req_id}")
                            st.rerun()

                    with c3:
                        if st.button("❌ Reject", key=f"rej_{req_id}", type="secondary"):
                            engine.update_customer_response(req_id, "Rejected")
                            st.error(f"Rejected {req_id}")
                            st.rerun()

    with tab_history:
        st.subheader("Historical Customer Confirmations")
        if not audit_df.empty:
            resolved_df = audit_df[audit_df["customer_response"].isin(["Approved", "Rejected"])]
            if not resolved_df.empty:
                st.dataframe(
                    resolved_df[["request_id", "timestamp", "customer_name", "agent_id", "action", "amount", "customer_response", "response_timestamp"]],
                    hide_index=True,
                    column_config={
                        "request_id": "Request ID",
                        "timestamp": "Request Time",
                        "customer_name": "Customer",
                        "agent_id": "Agent ID",
                        "action": "Action",
                        "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                        "customer_response": "Decision Response",
                        "response_timestamp": "Response Timestamp"
                    }
                )
            else:
                st.info("No customer responses recorded yet.")


# -----------------------------------------------------------------------------
# MODULE 5: AGENT REVOCATION
# -----------------------------------------------------------------------------
elif menu_option == "🚫 Agent Revocation":
    render_header("Administrator Agent Credential Revocation Center")

    st.markdown("""
        Administrators can revoke an external AI agent's authorization credentials at any time.
        Once revoked, the agent's historical records are strictly preserved, but **any future request
        from this agent will immediately be BLOCKED under Rule R1**, even for zero-cost informational requests.
    """)

    agents_list = engine.load_agents(AGENTS_FILE)
    active_agents = [a for a in agents_list if a.get("status") == "ACTIVE"]

    col_rev_form, col_rev_list = st.columns([1, 1])

    with col_rev_form:
        st.subheader("Revoke Agent Authorization")

        if not active_agents:
            st.warning("No ACTIVE agents available to revoke.")
        else:
            agent_options = {f"{a['agent_id']} – {a['agent_name']} ({a['customer_name']})": a["agent_id"] for a in active_agents}
            selected_label = st.selectbox("Select Active Agent to Revoke", options=list(agent_options.keys()))
            target_agent_id = agent_options[selected_label]

            selected_agent_record = next(a for a in active_agents if a["agent_id"] == target_agent_id)

            st.write(f"• **Agent ID:** `{selected_agent_record['agent_id']}`")
            st.write(f"• **Agent Name:** {selected_agent_record['agent_name']}")
            st.write(f"• **Owner:** {selected_agent_record['customer_name']}")
            st.write(f"• **Registered On:** {selected_agent_record['registered_at']}")

            st.markdown("---")
            confirm_box = st.checkbox(
                f"⚠️ I confirm the immediate revocation of Agent '{target_agent_id}'.",
                value=False,
                help="This action decommissioned the agent's credentials. All future requests will be rejected under Rule R1."
            )

            btn_revoke = st.button("Revoke Agent Credentials", type="primary", disabled=not confirm_box)

            if btn_revoke and confirm_box:
                success, msg = engine.revoke_agent(target_agent_id)
                if success:
                    st.success(f"✅ {msg}")
                    st.toast(f"Agent {target_agent_id} revoked successfully!", icon="🚫")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    with col_rev_list:
        st.subheader("All Agents & Status History")
        if agents_list:
            df_all = pd.DataFrame(agents_list)
            st.dataframe(
                df_all[["agent_id", "agent_name", "status", "registered_at", "revoked_at"]],
                hide_index=True,
                column_config={
                    "agent_id": "Agent ID",
                    "agent_name": "Agent Name",
                    "status": "Current Status",
                    "registered_at": "Registered At",
                    "revoked_at": "Revocation Timestamp"
                }
            )
        else:
            st.info("No agents recorded.")


# -----------------------------------------------------------------------------
# MODULE 6: AUDIT LOG
# -----------------------------------------------------------------------------
elif menu_option == "📜 Audit Log":
    render_header("Comprehensive Persistent Authorization Audit Trail")

    st.markdown("""
        Every agent evaluation is immutably recorded in the persistent audit ledger with full decision trace,
        rule numbers, customer response timestamps, and transaction metadata.
    """)

    audit_df = engine.load_audit_log(AUDIT_LOG_FILE)

    if audit_df.empty:
        st.info("Audit log is currently empty.")
    else:
        # Search & Filters
        fcol1, fcol2, fcol3, fcol4 = st.columns([2, 1, 1, 1])

        with fcol1:
            search_query = st.text_input("🔍 Search Audit Records", placeholder="Search by customer, agent, or reason...")
        with fcol2:
            filter_decision = st.selectbox("Filter Decision", options=["All", "ALLOW", "ASK CUSTOMER", "BLOCK"])
        with fcol3:
            filter_action = st.selectbox("Filter Action", options=["All"] + engine.VALID_ACTIONS)
        with fcol4:
            filter_response = st.selectbox("Customer Response", options=["All", "Pending", "Approved", "Rejected", "N/A"])

        filtered_df = audit_df.copy()

        # Apply Filters
        if search_query:
            q = search_query.strip().lower()
            filtered_df = filtered_df[
                filtered_df["customer_name"].str.lower().str.contains(q, na=False) |
                filtered_df["agent_id"].str.lower().str.contains(q, na=False) |
                filtered_df["agent_name"].str.lower().str.contains(q, na=False) |
                filtered_df["decision_explanation"].str.lower().str.contains(q, na=False) |
                filtered_df["request_id"].str.lower().str.contains(q, na=False)
            ]

        if filter_decision != "All":
            filtered_df = filtered_df[filtered_df["decision"] == filter_decision]

        if filter_action != "All":
            filtered_df = filtered_df[filtered_df["action"] == filter_action]

        if filter_response != "All":
            filtered_df = filtered_df[filtered_df["customer_response"] == filter_response]

        # Display Metrics
        st.caption(f"Showing **{len(filtered_df)}** of **{len(audit_df)}** total audit log entries.")

        # Interactive Table
        st.dataframe(
            filtered_df[[
                "request_id", "timestamp", "customer_name", "agent_id", "agent_name",
                "action", "amount", "decision", "rule_number", "customer_response", "decision_explanation"
            ]],
            hide_index=True,
            column_config={
                "request_id": "Request ID",
                "timestamp": "Timestamp",
                "customer_name": "Customer",
                "agent_id": "Agent ID",
                "agent_name": "Agent Name",
                "action": "Action",
                "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                "decision": "Decision",
                "rule_number": "Rule",
                "customer_response": "Customer Response",
                "decision_explanation": "Decision Reason"
            }
        )

        # CSV Export Functionality
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Audit Log to CSV",
            data=csv_data,
            file_name=f"indigo_agent_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            type="primary"
        )


# -----------------------------------------------------------------------------
# MODULE 7: TEST CENTRE
# -----------------------------------------------------------------------------
elif menu_option == "🧪 Test Centre":
    render_header("Automated 6-Point Academic Policy Verification Suite")

    st.markdown("""
        The Test Centre verifies the Gatekeeper's decision engine against the 6 required academic test cases.
        Tests execute dynamically against the live evaluation engine using an isolated test fixture to guarantee
        that test data never pollutes production audit logs.
    """)

    # Required Test Cases Definition Table
    st.markdown("#### Academic Test Case Specifications")
    st.markdown("""
    | Test # | Scenario Description | Input Parameters | Expected Decision | Expected Rule |
    | :---: | :--- | :--- | :---: | :---: |
    | **1** | Registered agent requesting to view fares | Agent: `ACTIVE`, Action: `View Fares`, Amount: `Rs. 0` | **ALLOW** | **R3** |
    | **2** | Unknown / unregistered agent attempting booking | Agent: `UNKNOWN`, Action: `Book Flight`, Amount: `Rs. 5,000` | **BLOCK** | **R2** |
    | **3** | Flight booking of Rs. 15,000 and above | Agent: `ACTIVE`, Action: `Book Flight`, Amount: `Rs. 20,000` | **ASK CUSTOMER** | **R5** |
    | **4** | Flight booking below Rs. 15,000 | Agent: `ACTIVE`, Action: `Book Flight`, Amount: `Rs. 10,000` | **ALLOW** | **R4** |
    | **5** | Revoked agent requesting to view fares | Agent: `REVOKED`, Action: `View Fares`, Amount: `Rs. 0` | **BLOCK** | **R1** |
    | **6** | Registered agent requesting refund | Agent: `ACTIVE`, Action: `Request Refund`, Amount: `Rs. 5,000` | **ASK CUSTOMER** | **R7** |
    | **7** | Agent name mismatch with registered ID | Agent: `MISMATCH`, Action: `View Fares`, Amount: `Rs. 0` | **BLOCK** | **R2** |
    | **8** | Customer ownership mismatch with registered ID | Customer: `MISMATCH`, Action: `View Fares`, Amount: `Rs. 0` | **BLOCK** | **R2** |
    """)

    st.markdown("---")

    btn_run_tests = st.button("🚀 Execute Automated Test Suite", type="primary")

    if btn_run_tests or "test_results" in st.session_state:
        if btn_run_tests:
            st.session_state.test_results = engine.run_automated_tests()

        results = st.session_state.test_results
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r["passed"])

        if passed_tests == total_tests:
            st.success(f"🎉 **ALL {total_tests}/{total_tests} TESTS PASSED (100% RELIABILITY).** System complies fully with IndiGo AI Agent Gatekeeper specifications.")
        else:
            st.error(f"⚠️ {passed_tests}/{total_tests} tests passed.")

        # Test Results Display Cards
        for t in results:
            pass_status = t["passed"]
            status_badge = '<span class="decision-badge badge-allow">✔ PASS</span>' if pass_status else '<span class="decision-badge badge-block">✘ FAIL</span>'
            border_color = "#10b981" if pass_status else "#ef4444"

            st.markdown(f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-left: 6px solid {border_color}; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; font-size: 15px; color: #001b94;">TEST {t['test_number']}: {t['title']}</span>
                        {status_badge}
                    </div>
                    <div style="font-size: 13px; color: #475569; margin-top: 6px;">
                        <b>Scenario:</b> {t['input_scenario']}
                    </div>
                    <div style="font-size: 13px; margin-top: 6px; display: flex; gap: 24px;">
                        <span><b>Expected:</b> <code>{t['expected_decision']}</code> ({t['expected_rule']})</span>
                        <span><b>Actual:</b> <code>{t['actual_decision']}</code> ({t['actual_rule']})</span>
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 6px; background: #f8fafc; padding: 6px 10px; border-radius: 4px;">
                        <b>Engine Trace:</b> {t['explanation']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.caption("Tests executed dynamically via `gatekeeper_engine.run_automated_tests()` with isolated in-memory registry.")
