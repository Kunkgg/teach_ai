# 0009 — Tool Calling：LLM 不执行代码，只产出调用请求

**Date**: 2026-08-12

**Context**: 
RAG pipeline 六步全部完成 LangChain 迁移后，进入 Week 2 后半核心：Tool Calling。这是从 RAG（读文档）到 Agent（做动作）的关键跳板。

**Insight**: 
4 key concepts:
1. **核心心智模型**：LLM 不执行函数，只生成 JSON 结构化请求。
2. **@tool 装饰器**：将函数的 docstring + 类型注解转换为 JSON Schema。
3. **4-step loop**：
   - define 工具
   - bind 工具到模型
   - invoke 获取 tool_calls
   - execute 代码执行，通过 ToolMessage 发回结果
4. **Agent 雏形**：Agent = 这个 4-step 循环持续运行，直到 LLM 不再返回 tool_calls 为止。

**Caveat**: 
- DeepSeek deepseek-chat 及其它标准模型大多支持 tool calling，但 deepseek-reasoner 并不一定完美支持该标准。
- `ToolMessage` 返回时必须带有与原本调用请求严格一致的 `tool_call_id`。

**Implications**: 
下一步引入 LangGraph。LangGraph 将接管这个过程，用状态图来更安全可靠地管理这个带有 `while` 行为的循环，从而构建一个健壮的有状态 Agent。

**Status**: 
Verified — 用户已完成 Lesson 0008
