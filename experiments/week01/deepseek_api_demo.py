import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL")
model = os.getenv("DEEPSEEK_MODEL")

if api_key is None:
    raise RuntimeError("DEEPSEEK_API_KEY is not configured")

if base_url is None:
    raise RuntimeError("DEEPSEEK_BASE_URL is not configured")

if model is None:
    raise RuntimeError("DEEPSEEK_MODEL is not configured")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    )

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "你是什么模型？",
        }
    ],
    extra_body={
        "thinking": {
            "type": "disabled"  # "disabled" or "enabled" to control whether the agent should think before responding
        }
    },
)

print("Response from DeepSeek API:")
print(response)
print()
print("Message content:")
print(response.choices[0].message.content)

print(type(response))
print(type(response.choices))
print(type(response.choices[0]))
print(type(response.choices[0].message))
print(type(response.choices[0].message.content))