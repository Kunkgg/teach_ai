"""Lesson 0011 — Memory：给 Agent 装上多轮记忆（填空版）。

填三处空白（标 ①②③），跑通后你将看到：
  - 第二轮只传新问题（不传历史！），Agent 却记得第一轮聊过的组件
  - 换一个 thread_id，Agent 立刻"失忆" —— 会话之间互相隔离
  - graph.get_state() 亲眼看见 checkpoint 里存的 State

运行（项目根目录）：
    uv run python src/teach_ai/15_memory_saver.py
"""

from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# 新面孔：checkpointer 的家。InMemorySaver 是 1.x 的正式名，
# 老教程里的 MemorySaver 只是它的向后兼容别名（源码 line 631: MemorySaver = InMemorySaver）
from langgraph.checkpoint.memory import InMemorySaver

from teach_ai.envs import DS_KEY

# ── 1. 工具 + LLM + State + chatbot node（和 Lesson 14 完全一样，零新东西） ──

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

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=DS_KEY,
    base_url="https://api.deepseek.com",
    temperature=0,
)
llm_with_tools = llm.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

# ── 2. 本课新东西 ①：checkpointer ──

checkpointer = InMemorySaver()

# TODO(①): 编译时挂上 checkpointer
#   提示：compile() 有一个和 checkpointer 同名的关键字参数
graph = graph_builder.compile(checkpointer=____)

# ── 3. 本课新东西 ②：thread_id —— 会话的钥匙 ──

# TODO(②): 构造 config，把 thread_id 传给 graph
#   提示：graph.invoke() 的第二个参数是 config（RunnableConfig，就是个 dict）。
#   thread_id 不能放在顶层 —— 它必须嵌在 "configurable" 这个 key 里面：
#       config = {"____": {"____": "thread-1"}}
config = ____________

# ── 4. 第一轮：正常问答（会触发一次工具调用） ──

q1 = "组件 auth-service 有多少条编码规范违规？"
print(f"\n{'='*60}\n🧑 [第 1 轮 / thread-1]: {q1}\n{'='*60}")
graph.invoke({"messages": [HumanMessage(content=q1)]}, config)

snapshot = graph.get_state(config)
print(f"📊 checkpoint 里的消息数: {len(snapshot.values['messages'])}  (下个待执行节点: {snapshot.next or '无，已空闲'})")

# ── 5. 本课新东西 ③：第二轮只传新问题 ──

q2 = "那它的可信分数是多少？"   # 注意："它" = auth-service，答案在上一轮的对话历史里

# TODO(③): 再 invoke 一次 —— 只传 q2 这一条新消息，不传任何历史
#   提示：和上面第一次调用完全同构：{"messages": [HumanMessage(...)]} + config
result = graph.invoke(________)

snapshot = graph.get_state(config)
print(f"📊 checkpoint 里的消息数: {len(snapshot.values['messages'])}  (第 1 轮结束后是 4，涨了说明历史在累积)")

print(f"\n🤖 [第 2 轮回答]: {result['messages'][-1].content}")

# ── 6. 失忆演示：换一个 thread_id，同样的 Agent，空白历史 ──

config2 = {"configurable": {"thread_id": "thread-2"}}
q3 = "我刚才问的是哪个组件？"
print(f"\n{'='*60}\n🧑 [第 1 轮 / thread-2]: {q3}   ← 新线程，没听过上文\n{'='*60}")
result2 = graph.invoke({"messages": [HumanMessage(content=q3)]}, config2)
print(f"\n🤖 [thread-2 回答]: {result2['messages'][-1].content}")
print("\n💡 同一个 graph 对象，thread-1 记得，thread-2 不知道 —— 记忆按 thread_id 隔离。")

# ── 7. 亲眼看看 checkpoint：StateSnapshot ──

snap1 = graph.get_state(config)
print(f"\n{'='*60}\n🔍 get_state(thread-1)\n{'='*60}")
print(f"  .values['messages'] 类型: {type(snap1.values['messages']).__name__}，长度 {len(snap1.values['messages'])}")
print(f"  .next  : {snap1.next}   ← 空元组 = 图跑完了，在等下一轮输入")
print(f"  .config: {snap1.config['configurable']}")

hist = list(graph.get_state_history(config))
print(f"\n🕐 该 thread 一共 {len(hist)} 个 checkpoint（每个超步存一份）——时间旅行的基础，之后的课细讲")
