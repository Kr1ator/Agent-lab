import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    intent:str
    answer:str
    confidence:float = Field(ge=0.0, le=1.0)

# ge = greater than or equal
# le = less than or equal
# 0 ≤ confidence ≤ 1

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL")
model = os.getenv("DEEPSEEK_MODEL")

if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY is not configured")

if not base_url:
    raise RuntimeError("DEEPSEEK_BASE_URL is not configured")

if not model:
    raise RuntimeError("DEEPSEEK_MODEL is not configured")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

messages = [
    {
        "role": "system",
        "content": """
You are an intent classification assistant.

Return your result in JSON format exactly like this:

{
  "intent": "question",
  "answer": "your answer",
  "confidence": 0.95
}

confidence must be a number between 0 and 1.
""",
    },
    {
        "role": "user",
        "content": "请用一句话解释什么是 AI Agent。",
    },
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format={
        "type": "json_object",  # LLM will return a JSON object
    },
    extra_body={
        "thinking": {
            "type": "disabled"  
        }
    },
)

raw_content = response.choices[0].message.content
print("--- Raw content ---")
print(raw_content)
print(type(raw_content))

data = json.loads(raw_content)
print("\n--- Parsed JSON ---")  # deserialization / 反序列化(JSON string -> json.loads() -> Python dict)
print(data)
print(type(data))             
  
result = AgentResponse.model_validate(data)  # validation / 验证
print("\n--- Validated Result ---")
print(result)
print(type(result))

print("\n--- Access fields ---")
print("Intent:", result.intent)
print("Answer:", result.answer)
print("Confidence:", result.confidence)