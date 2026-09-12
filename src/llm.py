from openai import OpenAI, APIError
from pydantic import ValidationError

from src.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)
from src.schemas import AgentResponse


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

def ask_llm(user_input: str) -> AgentResponse:
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": 
                            """
                            Return the result as JSON with exactly these fields:

                            {
                            "intent": "question",
                            "answer": "your answer",
                            "confidence": 0.95
                            }

                            confidence must be between 0 and 1.
                            """,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            response_format={"type": "json_object"},
            extra_body={
                "thinking": {
                    "type": "disabled"
                }
            },
        )
    except APIError as exc:
        raise RuntimeError("LLM API request failed") from exc

    raw_content = response.choices[0].message.content

    if raw_content is None:
        raise RuntimeError("LLM returned empty content")

    try:
        # 1.解析 json 字符串→dict；2.调用model_validate()校验 dict，一步到位。最终返回 Pydantic 模型对象
        return AgentResponse.model_validate_json(raw_content)
    except ValidationError as exc:
        raise RuntimeError("LLM returned invalid structured data") from exc 
