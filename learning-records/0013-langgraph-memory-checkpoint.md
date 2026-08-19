# 0013 — 给 Agent 装上记忆：Checkpointer 与 thread_id

## Date
2026-08-19

## Context
用户完成 Lesson 0009（Hello, LangGraph）+ 0010（源码三问）后进入 Week 3 中段。此前 Agent 每次 `invoke()` 都从空白 State 开始（金鱼记忆），用户在 Week 1 的 `qa.py` 里曾用全局 messages 列表手写过多轮记忆。本课引入 LangGraph 的生产级方案，也是 HITL（下一课）的前提。

## Insight
**记忆不是模型的超能力，是工程上的存取问题。** 两个新名词解决全部：

1. **Checkpointer**：`compile(checkpointer=InMemorySaver())`——每个超步后把整个 State 存一份快照。与 reducer 的分工：reducer 决定「新消息怎么合并」，checkpointer 决定「合并后的 State 怎么保存」。呼应 [0012](0012-langgraph-source-qa.md)：checkpoint 存的正是用户追问过的那个 `Annotated[list, add_messages]` 管理的 State——忘了 reducer，checkpointer 也救不了（存的是被覆盖的残缺历史）。
2. **thread_id = 会话的钥匙**：checkpointer 按 thread_id 分格子（`defaultdict`）。同 key 取回历史、新 key 空白开局——多会话隔离。对照后端经验：thread_id ≈ 会话 ID，checkpointer ≈ 会话存储。
3. **第二轮 invoke 只传一条新消息**——历史不在输入里，在 checkpoint 里。实测 DeepSeek 正确把「它的可信分数」中的"它"解析为 auth-service（消息数 4→8 累积），新 thread 则答"没有之前的对话记录"。

**关键设计（面试点）**：checkpointer 在 compile 时注入，graph 不关心存储位置——InMemorySaver 换 PostgresSaver 图代码零改动。

## Caveat
- `thread_id` 必须嵌在 config 的 `"configurable"` 里（双层 dict），不能放顶层。不传报 `ValueError: Checkpointer requires one or more of the following 'configurable' keys: thread_id, ...`（实测原文）。
- langgraph 1.2.10：正式类名 `InMemorySaver`，`MemorySaver` 仅是兼容别名（`checkpoint/memory/__init__.py:631`）。老教程的名字要能对上。
- `invoke` 后 `config["configurable"]` 会被自动追加 `checkpoint_id`（指向最新快照）——打印 config 时不要惊讶。
- 两轮对话（各含一次工具调用）产生 10 个 checkpoint，不是 8——每超步一份，不止每消息一份。

## Implications
- 下一课：`interrupt()` + human-in-the-loop（版本发布报告人工审核场景），中断/恢复完全建立在 checkpoint 之上
- `get_state_history` 是 time travel 的原料，暂只提及不展开
- 改造任务：15 变 `while True: input()` CLI = Week 1 `qa.py` 的 LangGraph 版（可信看板助手雏形）——用户可直观对比删掉了多少手动 messages 管理

## Status
Created — Lesson 0011 已创建，练习 `15_memory_saver.py` 已端到端验证（DeepSeek 真实返回：记忆 + 隔离均符合预期）
