
from backend.data.sample_workflows import SAMPLE_WORKFLOWS


def analyze_workflow(workflow_id: str) -> dict:
    """
    Analyses workflow information and identifies
    the components that may consume LLM tokens.
    """

    workflow = SAMPLE_WORKFLOWS.get(workflow_id)

    if workflow is None:
        raise ValueError(f"Workflow not found: {workflow_id}")

    agents = workflow.get("agents", [])

    analysis = {
        "application_name": workflow["application_name"],
        "business_use_case": workflow["business_use_case"],
        "model_name": workflow["model_name"],
        "expected_monthly_executions": (
            workflow["expected_monthly_executions"]
        ),
        "total_agents": len(agents),
        "agents": [],
        "execution_flow": workflow["execution_flow"],
        "tools": workflow["tools"]
    }

    for agent in agents:
        analysis["agents"].append({
            "agent_name": agent["name"],
            "responsibility": agent["responsibility"],
            "requires_llm_estimation": True
        })

    return analysis
