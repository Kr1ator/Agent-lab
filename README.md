# Agent Lab

一个用于学习 LLM 与 Agent 基础开发的 Python 小项目。项目演示了如何调用 DeepSeek API，并将模型回复校验为固定的数据结构。

## 项目结构

```text
src/
├── main.py      # 程序入口：读取终端问题并打印结果
├── llm.py       # 调用 LLM、处理接口和格式错误
├── schemas.py   # 定义 AgentResponse 数据结构
└── config.py    # 读取环境变量配置
```

## 安装依赖

建议使用项目的 Python 虚拟环境，然后安装依赖：

```bash
pip install -e .
```

## 配置 API

复制 `.env.example` 为 `.env`，并填入自己的 API Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

不要将 `.env` 或真实 API Key 提交到 Git 仓库。

## 运行

```bash
python -m src.main
```

终端会显示 `You:`。输入问题并按回车后，程序会请求模型，并输出：

- `intent`：意图
- `answer`：回答内容
- `confidence`：模型置信度（0 到 1）

模型返回的 JSON 会通过 Pydantic 校验；接口调用失败或数据格式不符合要求时，程序会显示相应错误信息。
