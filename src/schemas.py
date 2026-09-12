from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    intent: str
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)