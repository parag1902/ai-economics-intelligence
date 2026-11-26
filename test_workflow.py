
from backend.data.sample_workflows import SAMPLE_WORKFLOWS

workflow_id = "banking_customer_service"

print("Available workflow IDs:")
print(list(SAMPLE_WORKFLOWS.keys()))

print("\nTesting workflow lookup:")

workflow = SAMPLE_WORKFLOWS.get(workflow_id)

if workflow:
    print("SUCCESS: Workflow found")
    print("Application:", workflow["application_name"])
else:
    print("FAILED: Workflow not found")
