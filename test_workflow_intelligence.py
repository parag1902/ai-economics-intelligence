
import json

from backend.agents.workflow_intelligence_agent import (
    analyze_workflow_with_ai
)

try:
    result = analyze_workflow_with_ai("customer_support")

    print("\nWORKFLOW INTELLIGENCE ANALYSIS\n")
    print(json.dumps(result, indent=4))

except Exception as error:
    print("Analysis failed:", error)
