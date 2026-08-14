"""Lesson 0009 — Hello, LangGraph：从 while 循环到状态图（填空版）。

填三处空白（标 ①②③），跑通后你将看到：
  - LangGraph 自动管理 Tool Calling 循环
  - 和 Lesson 8 相同的最终结果，但代码更结构化
  - 图的 Mermaid 可视化描述

运行（项目根目录）：
    uv run python src/teach_ai/14_langgraph_hello.py
"""

from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from teach_ai.envs import DS_KEY

# ── 1. 定义工具（和 Lesson 8 完全一样） ──

VIOLATION_DATA = {"auth-service": 12, "user-service": 3, "payment-service": 27}
TRUST_SCORE_DATA = {"auth-service": 85.5, "user-service": 96.2, "payment-service": 72.1}


@tool
def count_violations(component: str) -> int:
    """查询指定组件的编码规范违规数量。当用户询问某个组件有多少违规时使用此工具。"""
    return VIOLATION_DATA.get(component, 0)


@tool
def get_trust_score(component: str) -> float:
    """查询指定组件的可信分数（0-100）。当用户询问某个组件的可信度或信任分数时使用此工具。"""
    return TRUST_SCORE_DATA.get(component, 0.0)


tools = [count_violations, get_trust_score]

# ── 2. 初始化 LLM（和 Lesson 8 完全一样） ──

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=DS_KEY,
    base_url="https://api.deepseek.com",
    temperature=0,
)
llm_with_tools = llm.bind_tools(tools)


# ── 3. 定义 State —— Graph 的共享记忆 ──

# TODO(①): 补全 State 的 messages 字段
#   提示：需要用 Annotated 和 add_messages 让消息列表自动追加而非覆盖
#   格式：messages: Annotated[____, ____]
class State(TypedDict):
    messages: ____  # ← 填这里


# ── 4. 定义 Node —— 和 Lesson 8 的「调用 LLM」一样 ──

def chatbot(state: State):
    """调用 LLM，返回回复。LangGraph 会通过 add_messages 自动追加到 state['messages']。"""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# ── 5. 搭建 Graph ──

graph_builder = StateGraph(State)

# 添加节点
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))  # 替代 Lesson 8 手动 for 循环

# 添加边
graph_builder.add_edge(START, "chatbot")  # 入口 → chatbot

# TODO(②): 添加条件边 —— chatbot 之后，根据是否有 tool_calls 决定去向
#   提示：用 add_conditional_edges，第一个参数是源节点名，第二个参数是路由函数
#   tools_condition 会在有 tool_calls 时返回 "tools"，否则返回 END
____  # ← 填这里

graph_builder.add_edge("tools", "chatbot")  # 工具执行完 → 回到 chatbot

# 编译
graph = graph_builder.compile()


# ── 6. 运行 ──

question = "组件 auth-service 有多少条编码规范违规？"
print(f"🧑 问题: {question}")
print()

# TODO(③): 调用 graph，传入正确格式的输入
#   提示：graph.invoke() 接收一个字典，key 是 state 的字段名
#   messages 字段需要是一个消息列表
result = ____  # ← 填这里

# 打印对话过程
for msg in result["messages"]:
    role = msg.__class__.__name__
    content = msg.content
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        print(f"🤖 [{role}] tool_calls: {msg.tool_calls}")
    elif content:
        prefix = "🧑" if role == "HumanMessage" else "🤖"
        print(f"{prefix} [{role}]: {content}")

print()
print("📊 Graph Mermaid 描述（可粘贴到 mermaid.live 查看）:")
print(graph.get_graph().draw_mermaid())
