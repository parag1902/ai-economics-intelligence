from backend.economics.token_estimator import estimate_tokens
from backend.economics.cost_calculator import calculate_cost


def forecast_cost(
    prompt: str,
    model_name: str,
    expected_output_tokens: int = 500
) -> dict:

    input_tokens = estimate_tokens(prompt)

    cost_details = calculate_cost(
        model_name=model_name,
        input_tokens=input_tokens,
        output_tokens=expected_output_tokens
    )

    return {
        "prompt": prompt,
        "model": model_name,
        "estimated_input_tokens": input_tokens,
        "estimated_output_tokens": expected_output_tokens,
        "forecasted_cost": cost_details["total_cost"],
        "currency": cost_details["currency"],
        "cost_breakdown": cost_details
    }