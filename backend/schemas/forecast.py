from pydantic import BaseModel, Field


class ForecastRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model_name: str = "gpt-4o-mini"
    expected_output_tokens: int = Field(default=500, gt=0)


class ForecastResponse(BaseModel):
    prompt: str
    model: str
    estimated_input_tokens: int
    estimated_output_tokens: int
    forecasted_cost: float
    currency: str
    cost_breakdown: dict