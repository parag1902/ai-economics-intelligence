
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Economics Intelligence",
    page_icon="📊",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ---------------- STYLE ----------------

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.title("AI Economics Intelligence")
st.caption(
    "Intelligent cost forecasting and economics "
    "for Agentic AI applications"
)

st.divider()

# ---------------- WORKFLOW DISCOVERY ----------------

st.sidebar.title("Configuration")

if st.sidebar.button("Refresh Applications"):
    st.session_state.pop("workflows", None)
    st.session_state.pop("forecast_result", None)
    st.rerun()

try:
    response = requests.get(
        f"{API_URL}/workflows",
        timeout=15
    )
    response.raise_for_status()
    workflows = response.json()
    st.session_state["workflows"] = workflows

except requests.exceptions.RequestException as error:
    st.error(f"Unable to retrieve workflows: {error}")
    st.info("Make sure your FastAPI backend is running.")
    st.stop()

if not workflows:
    st.warning("No workflows found. Add workflows to sample_workflows.py.")
    st.stop()

workflow_options = {
    item["application_name"]: item["workflow_id"]
    for item in workflows
}

selected_application = st.sidebar.selectbox(
    "Select Application",
    options=list(workflow_options.keys())
)

workflow_id = workflow_options[selected_application]

# Reset forecast when selected workflow changes
if st.session_state.get("selected_workflow") != workflow_id:
    st.session_state["selected_workflow"] = workflow_id
    st.session_state.pop("forecast_result", None)

# ---------------- GENERATE FORECAST ----------------

if st.sidebar.button("Generate Forecast", type="primary"):
    st.session_state["run_forecast"] = True

if "run_forecast" not in st.session_state:
    st.session_state["run_forecast"] = True

if st.session_state["run_forecast"]:

    with st.spinner("Analysing workflow and generating forecast..."):

        try:
            response = requests.post(
                f"{API_URL}/forecast/{workflow_id}",
                timeout=120
            )
            response.raise_for_status()

            st.session_state["forecast_result"] = response.json()
            st.session_state["run_forecast"] = False

        except requests.exceptions.RequestException as error:
            st.error(f"Forecast generation failed: {error}")
            st.stop()

# ---------------- DISPLAY RESULTS ----------------

if "forecast_result" in st.session_state:

    result = st.session_state["forecast_result"]

    workflow = result["workflow_analysis"]
    forecast = result["forecast"]
    scenarios = forecast["scenario_forecasts"]

    expected = scenarios["expected"]
    low = scenarios["low"]
    high = scenarios["high"]

    # ---------------- OVERVIEW ----------------

    st.subheader("Application Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Application", workflow["application_name"])
    col2.metric("AI Model", forecast["model_name"])

    col3.metric(
        "Monthly Executions",
        f'{expected["monthly"]["executions"]:,}'
    )

    total_calls = sum(
        step.get("calls_per_execution", 0)
        for step in expected["step_forecasts"]
    )

    col4.metric("LLM Calls / Execution", total_calls)

    st.divider()

    # ---------------- COST FORECAST ----------------

    st.subheader("Monthly Cost Forecast")

    currency = forecast["currency"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Low Scenario",
        f'{currency} {low["monthly"]["estimated_cost"]:.4f}'
    )

    col2.metric(
        "Expected Scenario",
        f'{currency} {expected["monthly"]["estimated_cost"]:.4f}'
    )

    col3.metric(
        "High Scenario",
        f'{currency} {high["monthly"]["estimated_cost"]:.4f}'
    )

    scenario_df = pd.DataFrame({
        "Scenario": ["Low", "Expected", "High"],
        "Monthly Cost": [
            low["monthly"]["estimated_cost"],
            expected["monthly"]["estimated_cost"],
            high["monthly"]["estimated_cost"]
        ]
    })

    st.plotly_chart(
        px.bar(
            scenario_df,
            x="Scenario",
            y="Monthly Cost",
            color="Scenario",
            title="Monthly Cost Comparison",
            text_auto=".4f"
        ),
        use_container_width=True
    )

    st.divider()

    # ---------------- TOKEN ANALYTICS ----------------

    st.subheader("Token Consumption Analytics")

    token_col1, token_col2, token_col3 = st.columns(3)

    token_col1.metric(
        "Input Tokens / Execution",
        f'{expected["per_execution"]["input_tokens"]:,}'
    )

    token_col2.metric(
        "Output Tokens / Execution",
        f'{expected["per_execution"]["output_tokens"]:,}'
    )

    token_col3.metric(
        "Total Monthly Tokens",
        f'{expected["monthly"]["total_tokens"]:,}'
    )

    token_df = pd.DataFrame({
        "Token Type": ["Input Tokens", "Output Tokens"],
        "Tokens": [
            expected["monthly"]["input_tokens"],
            expected["monthly"]["output_tokens"]
        ]
    })

    st.plotly_chart(
        px.pie(
            token_df,
            names="Token Type",
            values="Tokens",
            title="Monthly Input vs Output Tokens",
            hole=0.45
        ),
        use_container_width=True
    )

    st.divider()

    # ---------------- STAGE BREAKDOWN ----------------

    st.subheader("Workflow Stage Cost Breakdown")

    agent_rows = []

    for step in expected["step_forecasts"]:

        if step.get("uses_llm"):
            agent_rows.append({
                "Workflow Stage": step["step_name"],
                "LLM Calls": step["calls_per_execution"],
                "Input Tokens": step["total_input_tokens"],
                "Output Tokens": step["total_output_tokens"],
                "Total Tokens": step["total_tokens"],
                "Cost / Execution": step["cost_per_execution"]
            })

    agent_df = pd.DataFrame(agent_rows)

    if not agent_df.empty:

        st.dataframe(
            agent_df,
            use_container_width=True,
            hide_index=True
        )

        st.plotly_chart(
            px.bar(
                agent_df,
                x="Workflow Stage",
                y="Total Tokens",
                title="Token Consumption by Workflow Stage",
                color="Workflow Stage"
            ),
            use_container_width=True
        )
    else:
        st.info("No LLM-based stages identified.")

    st.divider()

    # ---------------- WORKFLOW INTELLIGENCE ----------------

    st.subheader("Workflow Intelligence")

    st.write(f"**Workflow Summary:** {workflow['workflow_summary']}")

    st.write(
        f"**Analysis Confidence:** "
        f"{workflow['confidence'].title()}"
    )

    for step in workflow["execution_steps"]:

        with st.expander(step["step_name"]):

            st.write(
                f"**Uses LLM:** "
                f"{'Yes' if step['likely_uses_llm'] else 'No'}"
            )

            st.write(
                f"**LLM Calls:** "
                f"{step['min_llm_calls']} - "
                f"{step['max_llm_calls']}"
            )

            st.write(f"**Reasoning:** {step['reasoning']}")

    # ---------------- ASSUMPTIONS ----------------

    st.divider()

    st.subheader("Forecast Assumptions & Limitations")

    st.info(forecast["warning"])

    with st.expander("View assumptions and missing information"):

        st.write("**Assumptions**")

        for assumption in workflow["assumptions"]:
            st.write(f"- {assumption}")

        st.write("**Missing Information**")

        for item in workflow["missing_information"]:
            st.write(f"- {item}")

    st.caption(
        f"Pricing source: {forecast['pricing_source']} | "
        f"Estimation method: {forecast['estimation_method']}"
    )

else:
    st.info("Select an application and generate its forecast.")
