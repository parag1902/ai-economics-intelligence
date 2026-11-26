from backend.economics.pricing_registry import get_model_pricing


def calculate_cost(
    model_name: str,
    input_tokens: int,
    output_tokens: int
) -> dict:
    pricing = get_model_pricing(model_name)

    input_cost = (
        input_tokens / 1_000_000
    ) * pricing["input_cost_per_1m_tokens"]

    output_cost = (
        output_tokens / 1_000_000
    ) * pricing["output_cost_per_1m_tokens"]

    total_cost = input_cost + output_cost

    return {
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total_cost, 6),
        "currency": pricing["currency"]
    }