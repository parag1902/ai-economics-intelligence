from backend.economics.token_estimator import (
    estimate_text_tokens
)

sample_text = """
You are a customer support AI assistant.
Understand the customer's question,
retrieve relevant information and generate
a helpful response.
"""

result = estimate_text_tokens(
    text=sample_text,
    model_name="gpt-4o-mini"
)

print("\nTOKENIZER TEST RESULT\n")

for key, value in result.items():
    print(f"{key}: {value}")