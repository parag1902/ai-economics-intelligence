from fastapi import APIRouter, HTTPException
from backend.data.sample_workflows import SAMPLE_WORKFLOWS
from backend.agents.workflow_intelligence_agent import (
    analyze_workflow_with_ai
)

from backend.agents.token_forecasting_agent import (
    forecast_workflow_tokens
)

router = APIRouter()


@router.get("/workflows")
def get_workflows():
    return [
        {
            "workflow_id": workflow_id,
            "application_name": workflow["application_name"]
        }
        for workflow_id, workflow in SAMPLE_WORKFLOWS.items()
    ]
@router.post("/forecast/{workflow_id}")
def create_workflow_forecast(workflow_id: str):
    try:
        # Step 1: Analyse the workflow using Groq
        workflow_analysis = analyze_workflow_with_ai(
            workflow_id
        )

        # Step 2: Forecast token consumption and costs
        forecast = forecast_workflow_tokens(
            workflow_analysis=workflow_analysis,
            workflow_id=workflow_id
        )

        # Step 3: Return the combined result
        return {
            "workflow_id": workflow_id,
            "workflow_analysis": workflow_analysis,
            "forecast": forecast
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )