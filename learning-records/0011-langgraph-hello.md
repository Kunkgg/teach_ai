# 0011 — Hello, LangGraph：从 while 循环到 StateGraph

## Date
2026-08-13

## Context
Week 2 收官（Lesson 0008 Tool Calling）后，用户已理解 Tool Calling 四步循环和 Agent 雏形（`while True` + tool_calls 检查）。Week 3 开篇引入 LangGraph，用 StateGraph 替代手写 while 循环。用户已安装 langgraph 1.2.10（Week 2 初 `uv add langchain langchain-openai` 时作为依赖一并安装）。

## Insight
**LangGraph 没做新的事——它把 Lesson 8 的 while 循环放进结构化画布。** 四个核心概念一一对应：

| Lesson 8 手写 | LangGraph |
|---|---|
| `messages = []` + 手动 `append` | `State(TypedDict)` + `Annotated[list, add_messages]` |
| `llm_with_tools.invoke(messages)` | `chatbot` node 函数 |
| `for tc in tool_calls: execute...` | `ToolNode(tools)` 预置节点 |
| `if not tool_calls: break` | `tools_condition` 条件路由 → END |
| `while True:` | Graph 的 `tools → chatbot` 回边自动循环 |

**关键新概念：**
1. **State**：`TypedDict` + reducer（`add_messages`）管理共享状态
2. **Node**：Python 函数，接收 state，返回 partial state update
3. **Edge**：Normal edge（固定路径）vs Conditional edge（动态路由）
4. **Compile**：`graph_builder.compile()` → 可执行的 CompiledGraph

**#1 Gotcha**：`Annotated[list, add_messages]` —— 没有 reducer，node 返回的消息会**覆盖**而非追加，对话历史丢失。

## Caveat
- `tools_condition` 预设路由到名为 `"tools"` 的节点。如果 tool node 取了别的名字，需要传 `path_map` 参数。
- `create_react_agent` 一行封装了所有上述步骤，但面试会问内部实现，所以先手动搭建。

## Implications
- 下一步：加入 `MemorySaver` + `thread_id` 实现多轮对话记忆（Lesson 0010）
- 然后：`interrupt_before` 实现 human-in-the-loop（Lesson 0011）
- 最终：用 LangGraph 构建可信评估 Agent（Week 3 收官项目）

## Status
Created — 等待用户验证
