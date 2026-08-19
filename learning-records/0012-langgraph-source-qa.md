# 0012 — LangGraph 源码三问：Annotated、sys.intern、path_map

## Date
2026-08-19

## Context
用户完成 Lesson 0009（Hello, LangGraph）后主动读了 langgraph 源码（1.2.10），提出三个问题：① `Annotated[list, add_messages]` 里的 `add_messages` 是类型还是函数？② `START`/`END` 为什么用 `sys.intern`？③ `tools_condition` 路由的 `"tools"` 节点名是固定的吗？多 tool node 怎么办？——**这是用户第一次主动读框架源码提问**，从"跟着教程写"进入"读实现验证"的学习阶段。

## Insight
三个问题的共同答案是「框架没有魔法，都是标准 Python」：
1. **Annotated 误解**：用户原以为是「列表元素是 add_messages 类型」。纠正：`Annotated[T, meta]` 只有第一个参数是类型，`add_messages` 是元数据（reducer 函数）。框架在 compile 时用 `get_type_hints(cls, include_extras=True)` 读出来（默认 `get_type_hints` 会剥掉 Annotated——实测验证）。同一 idiom：FastAPI `Query()`、Pydantic `Field(gt=0)`。
2. **sys.intern**：哨兵常量 micro-optimization + 语义声明。实测诚实结论：8 字符串 200 万次比较差异是噪声级（~0.027s vs 0.027s）——不要向用户夸大性能收益。反模式：intern 用户输入（immortal，永不释放）。冷知识：标识符风格字面量编译期自动 intern，`'__'+'start__'` 会被常量折叠，真正逃逸要用 join。
3. **tools_condition 返回字符串，不知道节点**：`"tools"` 是约定（`create_react_agent` 内部命名），映射靠 `add_conditional_edges` 的 `path_map`。实测验证：改名后 `ValueError: ... found unknown target 'tools'`，`{"tools": "my_tools", "__end__": END}` 修复。

## Caveat
- langgraph 1.2.10 的 `add_messages` 实际是 `_add_messages_wrapper` 闭包包装（`repr` 可见），教学按导出名讲即可。
- path_map 方向：key = 路由函数返回值（逻辑目的地），value = 图里真实节点名。写反了报 unknown target。

## Implications
- 用户进入「读源码验证」阶段 → 后续 lesson 可以更多引用 venv 源码路径（`langgraph/constants.py:28` 这种），鼓励此习惯
- Annotated 是高频面试题（State 实现原理），满分回答已写入 Lesson 0010
- 下一步：MemorySaver + thread_id（多轮记忆），checkpoint 保存的正是 reducer 管理的 State——衔接今天讲的 add_messages 按 ID 合并
- MemorySaver lesson 编号从 0010 顺延为 0011（0010 被本答疑课占用）

## Status
Created — Lesson 0010 已创建并交给用户
