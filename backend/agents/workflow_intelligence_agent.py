
import json

from backend.data.sample_workflows import SAMPLE_WORKFLOWS
from backend.llm.groq_client import get_groq_client, GROQ_MODEL


def analyze_workflow_with_ai(workflow_id: str) -> dict:
    """
    Uses Groq to analyse workflow execution behaviour
    and identify potential LLM calls.
    """

    workflow = SAMPLE_WORKFLOWS.get(workflow_id)

    if workflow is None:
        raise ValueError(f"Workflow not found: {workflow_id}")

    client = get_groq_client()

    workflow_information = {
        "application_name": workflow["application_name"],
        "business_use_case": workflow["business_use_case"],
        "workflow_description": workflow["workflow_description"],
        "model_name": workflow["model_name"],
        "agents": workflow["agents"],
        "tools": workflow["tools"],
        "execution_flow": workflow["execution_flow"]
    }

    system_prompt = """
You are an AI Workflow Intelligence Analyst.

Your task is to analyse Agentic AI workflows for token
consumption forecasting.

Identify which workflow stages are likely to call an LLM.
Do not assume that every agent requires an LLM call.

For each stage, identify:
1. Step name.
2. Whether an LLM call is likely.
3. Minimum and maximum likely LLM calls per execution.
4. Information supplied to the LLM.
5. Expected type of LLM output.
6. Whether retries or additional calls may occur.
7. Explanation for your assessment.

Important rules:
- A vector database search does not automatically require an LLM.
- Tool execution alone does not count as an LLM call.
- Do not invent exact token counts.
- Clearly identify assumptions and missing information.
- Treat call counts as estimates, not actual measurements.

Return valid JSON only, using this structure:

{
  "application_name": "string",
  "model_name": "string",
  "workflow_summary": "string",
  "execution_steps": [
    {
      "step_name": "string",
      "likely_uses_llm": true,
      "min_llm_calls": 0,
      "max_llm_calls": 1,
      "input_components": ["string"],
      "expected_output": "string",
      "retry_possible": false,
      "reasoning": "string"
    }
  ],
  "assumptions": ["string"],
  "missing_information": ["string"],
  "confidence": "low, medium, or high"
}
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": (
                    "Analyse this workflow:\n"
                    + json.dumps(workflow_information, indent=2)
                )
            }
        ],
        response_format={"type": "json_object"},
        max_completion_tokens=3000,
        temperature=0.1
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("Groq returned an empty response.")

    try:
        analysis = json.loads(result)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Groq returned invalid JSON."
        ) from error

    if "execution_steps" not in analysis:
        raise ValueError(
            "Groq response is missing execution_steps."
        )

    return analysis
