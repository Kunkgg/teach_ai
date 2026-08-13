"""Lesson 0008 — Tool Calling：让 LLM 调用你的 Python 函数（填空版）。

填三处空白（标 ①②③），跑通后你将看到：
  1. LLM 选择调用哪个工具
  2. 你的代码执行工具并返回结果
  3. LLM 根据结果生成自然语言回答

运行（项目根目录）：
    uv run python src/teach_ai/12_tool_calling.py
"""

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from teach_ai.envs import DS_KEY

# ── 模拟数据（假装这是从数据库查出来的） ──
VIOLATION_DATA = {
    "auth-service": 12,
    "user-service": 3,
    "payment-service": 27,
}

TRUST_SCORE_DATA = {
    "auth-service": 85.5,
    "user-service": 96.2,
    "payment-service": 72.1,
}

# ── 1. 定义工具 ──

# TODO(①): 给这个函数加上 @tool 装饰器
#   提示：from langchain_core.tools import tool（已在上面 import）
#   加了 @tool 后，LangChain 会用 docstring 和类型注解自动生成 JSON Schema
____                              # ← 填这里
def count_violations(component: str) -> int:
    """查询指定组件的编码规范违规数量。当用户询问某个组件有多少违规时使用此工具。"""
    return VIOLATION_DATA.get(component, 0)

@tool
def get_trust_score(component: str) -> float:
    """查询指定组件的可信分数（0-100）。当用户询问某个组件的可信度或信任分数时使用此工具。"""
    return TRUST_SCORE_DATA.get(component, 0.0)

tools = [count_violations, get_trust_score]
tools_by_name = {t.name: t for t in tools}

# ── 2. 初始化 LLM 并绑定工具 ──
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=DS_KEY,
    base_url="https://api.deepseek.com",
    temperature=0,
)

# TODO(②): 用 bind_tools 把工具列表绑定到 LLM
#   提示：llm.bind_tools(____)
llm_with_tools = ____             # ← 填这里

# ── 3. 发送问题，观察 LLM 的工具调用决策 ──
question = "组件 auth-service 有多少条编码规范违规？"
messages = [HumanMessage(content=question)]

print(f"🧑 问题: {question}")
print()

ai_msg = llm_with_tools.invoke(messages)
print(f"🤖 LLM 返回的 tool_calls: {ai_msg.tool_calls}")
print()

# ── 4. 执行工具调用，把结果返回给 LLM ──
if ai_msg.tool_calls:
    messages.append(ai_msg)  # 把 LLM 的回复（含 tool_calls）加入对话历史

    for tc in ai_msg.tool_calls:
        print(f"🔧 执行工具: {tc['name']}({tc['args']})")
        
        # TODO(③): 执行工具调用，并把结果包装成 ToolMessage
        #   a. 用 tools_by_name[tc["name"]] 找到对应的工具
        #   b. 用 .invoke(tc) 执行工具
        #   c. 创建 ToolMessage(content=str(result), tool_call_id=tc["id"])
        selected_tool = tools_by_name[tc["name"]]
        result = selected_tool.invoke(tc)
        tool_msg = ____               # ← 填这里
        
        print(f"   结果: {result}")
        messages.append(tool_msg)

    # 把工具结果送回 LLM，让它生成最终的自然语言回答
    final = llm_with_tools.invoke(messages)
    print(f"\n🤖 最终回答: {final.content}")
else:
    print(f"🤖 直接回答（没有调用工具）: {ai_msg.content}")
