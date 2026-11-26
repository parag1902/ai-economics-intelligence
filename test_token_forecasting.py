
import json

from backend.agents.workflow_intelligence_agent import (
    analyze_workflow_with_ai
)

from backend.agents.token_forecasting_agent import (
    forecast_workflow_tokens
)


try:
    # First analyse the workflow using Groq.
    workflow_analysis = analyze_workflow_with_ai(
        "customer_support"
    )

    # Then estimate token consumption.
    forecast = forecast_workflow_tokens(
        workflow_analysis=workflow_analysis,workflow_id="customer_support"
    )

    print("\nTOKEN CONSUMPTION FORECAST\n")
    print(json.dumps(forecast, indent=4))

except Exception as error:
    print("Forecasting failed:", error)
