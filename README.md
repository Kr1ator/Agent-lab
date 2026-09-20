# Agent Lab

一个按周持续迭代、用于学习 LLM 与 Agent 工程的 Python 项目。

当前已完成 Week 1：Structured LLM App。程序会调用 DeepSeek API，并将模型回复校验为固定的数据结构。

## 项目结构

```text
src/                   # 持续演进的当前程序
experiments/week01/    # Week 1 实验代码
experiments/week02/    # Week 2 实验代码
docs/progress/         # 每周学习记录
tests/                 # 正式测试
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

## Weekly Progress

每周的学习目标、实现和局限记录在 [`docs/progress/`](docs/progress/) 中。

## Versions / Milestones

- `v0.1` — Week 1 — Structured LLM App
- `v0.2` — Week 2 — Raw Tool-Calling Agent（未开始）
