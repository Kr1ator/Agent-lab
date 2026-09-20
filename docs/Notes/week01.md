# Week 1 — Structured LLM App

本周完成：从终端接收问题，调用 DeepSeek，将 JSON 回复校验为 `AgentResponse`，并处理基本异常。

## 1. LLM、Tool 与 Agent

- **LLM** 根据输入生成内容；**Tool** 执行查询、计算等外部操作；**Agent** 围绕目标组织模型决策、工具执行与结果反馈。
- 当前请求只包含 system 指令和本次问题，没有自动保存历史；需要上下文时，程序必须主动传入。
- W1 是单次调用的 LLM 应用，尚未实现 Tool Calling、Agent Loop、Memory 或 RAG。

## 2. 项目结构与配置

| 文件 / 目录 | 职责 |
| --- | --- |
| `src/main.py` | 接收输入、调用 LLM、显示结果或错误 |
| `src/llm.py` | 请求 DeepSeek、提取回复、校验数据 |
| `src/config.py` | 读取并检查必需的环境变量 |
| `src/schemas.py` | 定义 AgentResponse 字段与约束 |
| `experiments/week01/` | W1 独立实验 |
| `docs/Notes/` | 每周笔记 |
| `tests/` | 正式测试 |

`.env` 保存真实配置，不提交 Git；`.env.example` 是可提交的配置模板。

```python
load_dotenv()  # 将 .env 配置加载到当前进程的环境变量
api_key = os.getenv("DEEPSEEK_API_KEY")
```

`config.py` 统一检查 API Key、Base URL 和模型名称，缺少配置时抛出 `RuntimeError`。

在项目根目录运行 `python -m src.main`：按模块启动，支持代码中的 `from src... import...`。

## 3. API 调用：谁负责什么

- **API** 是服务接口，**HTTP** 是客户端与服务器通信的协议。
- **SDK** 封装认证、请求发送和响应解析；本项目使用 OpenAI Python SDK 访问 DeepSeek 兼容接口。
- **Base URL** 指定服务基础地址；**client** 是本地通信对象，真正的 LLM 运行在服务端。

```python
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
response = client.chat.completions.create(
    model=DEEPSEEK_MODEL,
    messages=[...],  # system 指令 + user 问题，示意
    response_format={"type": "json_object"},
)
raw_content = response.choices[0].message.content
```

`response` 是 SDK 对象，`message.content` 才是模型回复文本。`usage` 记录输入、输出与总 Token 数，多次调用会累积用量和延迟。

## 4. JSON、dict 与 Pydantic

**JSON 是文本格式，dict 是 Python 对象**。JSON 的 `true / false / null` 对应 Python 的 `True / False / None`。

```python
text = json.dumps(data)  # 序列化：dict → JSON 字符串
data = json.loads(text)  # 反序列化：JSON 字符串 → dict
```

Structured Output 让回复便于程序处理。本项目用三层约束：**Prompt 指定字段 → JSON Mode 约束 JSON 格式 → Pydantic 校验字段、类型和范围**。合法 JSON 不等于符合业务结构，也不代表回答事实正确。

```python
class AgentResponse(BaseModel):
    intent: str
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)

result = AgentResponse.model_validate_json(raw_content)
```

`model_validate_json()` 一步完成解析和校验，成功返回模型实例，失败抛出 `ValidationError`，并非返回 True/False。已有 dict 时，用 `AgentResponse.model_validate(data)`。

- `data["intent"]` 访问字典；`result.intent` 访问模型实例字段。
- `confidence=12` 可以出现在合法 JSON 中，但不满足 0–1 的约束。
- `confidence` 是模型给出的数值，不是经过验证的正确率。

## 5. 数据流与异常处理

```text
User input → Python dict → main.py → llm.py → serialization 得到 JSON text → 通过 HTTP 发送给 DeepSeek API
                                                                                            ↓
result.xxx ← AgentResponse object ← Pydantic validation ← Python dict ← json.loads() ← JSON string

```

`llm.py` 将 API 请求失败、空回复、数据校验失败转为 `RuntimeError`；`main.py` 捕获后显示错误。`raise ... from exc` 保留原始异常链，方便定位原因。

配置在模块导入时加载，因此配置缺失发生在 `main()` 的异常捕获之前。

## 6. 三个实验

- `env_demo.py`：练习加载环境变量；该实验检查 `LLM_API_KEY`，主程序使用 `DEEPSEEK_API_KEY`。
- `deepseek_api_demo.py`：发送请求，观察 SDK 响应结构和各层对象类型。
- `structured_output_demo.py`：观察 JSON 文本 → dict → Pydantic 实例的转换。
