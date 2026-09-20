# Week 1 - Structured LLM App

## Goals

- 建立可运行的 Python 项目结构和环境配置。
- 调用 DeepSeek API，并将回复约束为可校验的结构化数据。
- 理解 LLM 应用中请求、JSON 解析、数据校验和错误处理的基本流程。

## What I Learned

- LLM 负责生成结果，Tool 负责执行外部能力，Agent 则负责根据目标组织 LLM 与 Tool；Week 1 还不是完整 Agent。
- 单次 API 调用本身没有记忆；如果需要上下文，应用必须在新请求中重新传入历史信息。
- JSON 是文本格式，Python `dict` 是内存中的数据结构；两者可以通过序列化和反序列化转换。
- Structured Output 让模型按约定的 JSON 字段返回结果，方便程序继续处理。
- Pydantic 会解析和校验数据，成功时返回 `AgentResponse` 实例，失败时抛出校验异常。
- API 是服务接口，SDK 提供 Python 调用方式，Base URL 指向服务地址，client 封装配置并发送请求。

## What I Implemented

- 用 `.env` 和 `src/config.py` 加载 DeepSeek API Key、Base URL 和模型名称。
- 在 `src/llm.py` 中创建 OpenAI 兼容 client，发送单次 DeepSeek 请求并要求 JSON Object 输出。
- 在 `src/schemas.py` 中定义 `AgentResponse`，校验 `intent`、`answer` 和 0–1 范围的 `confidence`。
- 在 `src/main.py` 中读取终端输入、调用 LLM，并打印结构化结果。
- 对 API 请求失败、空内容和 Pydantic 校验失败进行基本异常处理。

## Experiments

- `env_demo.py`：练习从 `.env` 加载并检查环境变量。
- `deepseek_api_demo.py`：练习创建 client、调用 DeepSeek API 和观察 SDK 返回对象。
- `structured_output_demo.py`：练习 JSON Structured Output、`dict` 解析和 Pydantic 校验。

## Architecture

```text
User
 ↓
main.py
 ↓
llm.py
 ↓
DeepSeek API
 ↓
Structured JSON
 ↓
Pydantic AgentResponse
```

## Current Limitations

- 没有 Tool Calling。
- 没有 Agent Loop。
- 没有 Memory。
- 没有 RAG。
- 以单次 LLM 调用为主。
