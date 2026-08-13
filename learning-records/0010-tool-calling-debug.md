# 0010 — Tool Calling 调试：LangChain 在 bind_tools 中不注入 system prompt

## Date
2026-08-13

## Context
用户完成 Lesson 0008 Tool Calling 填空后，追问了一个高质量问题：「有没有调试方法可以打印所有发给 LLM 的最终 prompt？LangChain 在 tool calling 过程中会注入默认提示词吗？」

## Insight
**核心发现：LangChain 在原生 Tool Calling 中不注入额外的 system prompt。**

工具定义走的是 OpenAI API 的原生协议——`tools` 作为 API 请求体的独立字段，和 `messages` 平级，不是拼进 prompt 里的。API 请求结构如下：
```json
{
  "model": "deepseek-v4-flash",
  "messages": [{"role": "user", "content": "..."}],
  "tools": [{"type": "function", "function": {"name": "...", "description": "...", "parameters": {...}}}],
  "temperature": 0
}
```

**三种调试方法：**
1. **查看 `@tool` 生成的 JSON Schema**：`tool.args_schema.model_json_schema()` 直接打印 LLM 看到的工具描述
2. **查看 `bind_tools()` 注入的 kwargs**：`llm_with_tools.kwargs` 返回 `{"tools": [...]}`，这就是每次 API 调用附加的 `tools` 字段
3. **`set_debug(True)`**：`from langchain_core.globals import set_debug` 开启后，每次 `invoke` 都会打印完整的输入（prompts）、输出（generations）和 token 用量

**关键区分（面试可用）：**
- 支持原生 tool calling 的模型（DeepSeek/OpenAI/Anthropic）：工具定义走 `tools` 字段，不污染 prompt
- 不支持原生 tool calling 的模型（部分早期开源模型）：框架需要把工具描述拼进 system prompt 模拟 tool calling，此时才会注入提示词

## Caveat
- `set_debug(True)` 输出极其冗长，生产环境不要开。更推荐 LangSmith（Week 4 会学）做可观测性。
- `llm_with_tools.kwargs` 展示的是 OpenAI 格式的 tools payload，但不同模型提供商可能有细微差异。

## Implications
- 用户开始主动追问框架底层机制，说明已跨过"能跑通"进入"理解为什么"阶段。
- 这个调试习惯（查看实际 API 请求）在后续 LangGraph Agent 调试中会反复用到。
- 探针脚本 `13_debug_tool_calling.py` 可作为后续调试的模板。

## Status
Completed — 用户提出问题后，通过探针脚本 `13_debug_tool_calling.py` 用三种方法验证了 LangChain 的 tool calling 行为。相关：[[0009-tool-calling]]
