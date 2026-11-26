MODEL_PRICING = {
    "gpt-4o": {
        "provider": "OpenAI",
        "input_cost_per_1m_tokens": 2.50,
        "output_cost_per_1m_tokens": 10.00,
        "currency": "USD"
    },
    "gpt-4o-mini": {
        "provider": "OpenAI",
        "input_cost_per_1m_tokens": 0.15,
        "output_cost_per_1m_tokens": 0.60,
        "currency": "USD"
    },
    "claude-3-5-sonnet": {
        "provider": "Anthropic",
        "input_cost_per_1m_tokens": 3.00,
        "output_cost_per_1m_tokens": 15.00,
        "currency": "USD"
    },
    "gemini-2.5-flash": {
        "provider": "Google",
        "input_cost_per_1m_tokens": 0.30,
        "output_cost_per_1m_tokens": 2.50,
        "currency": "USD"
    }
}


def get_model_pricing(model_name: str) -> dict:
    pricing = MODEL_PRICING.get(model_name)

    if pricing is None:
        raise ValueError(f"Pricing not available for model: {model_name}")

    return pricing