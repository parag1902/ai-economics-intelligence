
import math

from backend.data.sample_workflows import SAMPLE_WORKFLOWS
from backend.economics.token_estimator import estimate_tokens
from backend.economics.cost_calculator import calculate_cost


def get_step_samples(step_name: str, workflow: dict) -> tuple[str, str]:
    """Find representative input and output for an execution step."""

    for agent in workflow.get("agents", []):
        if agent.get("workflow_step", "").strip().lower() != step_name.strip().lower():
            continue

        representative_input = agent.get("representative_input", "")
        representative_output = (
            agent.get("representative_output")
            or agent.get("representative_context")
            or ""
        )

        # Use workflow-level input when agent-level input is absent.
        if not representative_input:
            inputs = workflow.get("representative_inputs", [])
            if inputs:
                first_input = inputs[0]
                if isinstance(first_input, dict):
                    representative_input = "\n".join(
                        str(value) for value in first_input.values()
                    )
                else:
                    representative_input = str(first_input)

        system_prompt = agent.get("system_prompt", "")

        input_text = "\n".join(
            part for part in [system_prompt, str(representative_input)] if part
        )

        return input_text, str(representative_output)

    return "", ""


def estimate_step_tokens(
    step: dict,
    workflow: dict,
    model_name: str
) -> dict:

    step_name = step["step_name"]

    if not step.get("likely_uses_llm", False):
        return {
            "step_name": step_name,
            "uses_llm": False,
            "minimum_total_tokens": 0,
            "maximum_total_tokens": 0,
            "minimum_input_tokens": 0,
            "maximum_input_tokens": 0,
            "minimum_output_tokens": 0,
            "maximum_output_tokens": 0
        }

    input_text, output_text = get_step_samples(step_name, workflow)

    if not input_text or not output_text:
        raise ValueError(
            f"Representative text missing for {step_name}. "
            "Check the agent's workflow_step, representative_input "
            "and representative_output in sample_workflows.py."
        )

    input_tokens = estimate_tokens(input_text, model_name)
    output_tokens = estimate_tokens(output_text, model_name)

    min_calls = step.get("min_llm_calls", 1)
    max_calls = step.get("max_llm_calls", 1)

    minimum_input_tokens = input_tokens * min_calls
    maximum_input_tokens = input_tokens * max_calls

    minimum_output_tokens = output_tokens * min_calls
    maximum_output_tokens = output_tokens * max_calls

    return {
        "step_name": step_name,
        "uses_llm": True,
        "min_llm_calls": min_calls,
        "max_llm_calls": max_calls,
        "input_tokens_per_call": input_tokens,
        "output_tokens_per_call": output_tokens,
        "minimum_input_tokens": minimum_input_tokens,
        "maximum_input_tokens": maximum_input_tokens,
        "minimum_output_tokens": minimum_output_tokens,
        "maximum_output_tokens": maximum_output_tokens,
        "minimum_total_tokens": (
            minimum_input_tokens + minimum_output_tokens
        ),
        "maximum_total_tokens": (
            maximum_input_tokens + maximum_output_tokens
        ),
        "token_count_method": "tiktoken"
    }


def forecast_workflow_tokens(
    workflow_analysis: dict,
    workflow_id: str
) -> dict:

    workflow = SAMPLE_WORKFLOWS.get(workflow_id)

    if workflow is None:
        raise ValueError(f"Workflow not found: {workflow_id}")

    model_name = workflow["model_name"]
    monthly_executions = workflow["expected_monthly_executions"]
    scenarios = workflow["forecast_scenarios"]

    base_steps = []

    for step in workflow_analysis["execution_steps"]:
        result = estimate_step_tokens(
            step=step,
            workflow=workflow,
            model_name=model_name
        )
        base_steps.append(result)

    scenario_results = {}

    for scenario_name, assumptions in scenarios.items():

        input_multiplier = assumptions["input_multiplier"]
        output_multiplier = assumptions["output_multiplier"]
        calls_multiplier = assumptions["calls_multiplier"]

        total_input_tokens = 0
        total_output_tokens = 0
        scenario_steps = []

        for step in base_steps:

            if not step["uses_llm"]:
                scenario_steps.append({
                    "step_name": step["step_name"],
                    "uses_llm": False,
                    "total_tokens": 0
                })
                continue

            input_per_call = round(
                step["input_tokens_per_call"] * input_multiplier
            )

            output_per_call = round(
                step["output_tokens_per_call"] * output_multiplier
            )

            min_calls = step["min_llm_calls"]

            max_calls = max(
                min_calls,
                math.ceil(
                    step["max_llm_calls"] * calls_multiplier
                )
            )

            calls = max_calls

            step_input = input_per_call * calls
            step_output = output_per_call * calls
            step_total = step_input + step_output

            total_input_tokens += step_input
            total_output_tokens += step_output

            step_cost = calculate_cost(
                model_name=model_name,
                input_tokens=step_input,
                output_tokens=step_output
            )

            scenario_steps.append({
                "step_name": step["step_name"],
                "uses_llm": True,
                "calls_per_execution": calls,
                "input_tokens_per_call": input_per_call,
                "output_tokens_per_call": output_per_call,
                "total_input_tokens": step_input,
                "total_output_tokens": step_output,
                "total_tokens": step_total,
                "cost_per_execution": step_cost["total_cost"]
            })

        total_tokens = total_input_tokens + total_output_tokens

        execution_cost = calculate_cost(
            model_name=model_name,
            input_tokens=total_input_tokens,
            output_tokens=total_output_tokens
        )

        monthly_input_tokens = total_input_tokens * monthly_executions
        monthly_output_tokens = total_output_tokens * monthly_executions

        monthly_cost_details = calculate_cost(
            model_name=model_name,
            input_tokens=monthly_input_tokens,
            output_tokens=monthly_output_tokens
        )

        scenario_results[scenario_name] = {
            "per_execution": {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "total_tokens": total_tokens,
                "estimated_cost": execution_cost["total_cost"]
            },
            "monthly": {
                "executions": monthly_executions,
                "input_tokens": monthly_input_tokens,
                "output_tokens": monthly_output_tokens,
                "total_tokens": (
                    monthly_input_tokens + monthly_output_tokens
                ),
                "estimated_cost": monthly_cost_details["total_cost"]
            },
            "step_forecasts": scenario_steps
        }

    return {
        "application_name": workflow["application_name"],
        "model_name": model_name,
        "currency": "USD",
        "scenario_forecasts": scenario_results,
        "pricing_source": "Local illustrative pricing registry",
        "estimation_method": (
            "Representative text tokenization with "
            "configurable scenario multipliers"
        ),
        "warning": (
            "Scenario projections are based on configurable "
            "assumptions, not measured production usage. "
            "Actual costs may differ."
        )
    }
