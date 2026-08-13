"""探针脚本 — 揭开 bind_tools + invoke 底下到底发了什么给 LLM API。

三种调试方法，从简单到深入：
  1. set_debug(True)      — LangChain 内置，打印所有中间步骤
  2. 手动查看 bind_tools 注入的 kwargs
  3. HTTP 抓包             — 看到发给 DeepSeek API 的原始 JSON body

运行：
    uv run python src/teach_ai/13_debug_tool_calling.py
"""

import json
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from teach_ai.envs import DS_KEY

# ── 复用 Lesson 0008 的工具定义 ──
VIOLATION_DATA = {"auth-service": 12, "user-service": 3, "payment-service": 27}

@tool
def count_violations(component: str) -> int:
    """查询指定组件的编码规范违规数量。当用户询问某个组件有多少违规时使用此工具。"""
    return VIOLATION_DATA.get(component, 0)

@tool
def get_trust_score(component: str) -> float:
    """查询指定组件的可信分数（0-100）。当用户询问某个组件的可信度或信任分数时使用此工具。"""
    return {"auth-service": 85.5}.get(component, 0.0)

tools = [count_violations, get_trust_score]

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=DS_KEY,
    base_url="https://api.deepseek.com",
    temperature=0,
)

# ═══════════════════════════════════════════════════════════════════════
# 方法 1：查看 @tool 生成的 JSON Schema
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("🔍 方法 1：@tool 生成的 JSON Schema（LLM 看到的工具描述）")
print("=" * 70)

for t in tools:
    print(f"\n── {t.name} ──")
    print(f"  description: {t.description}")
    print(f"  args_schema: {json.dumps(t.args_schema.model_json_schema(), indent=4, ensure_ascii=False)}")

# ═══════════════════════════════════════════════════════════════════════
# 方法 2：查看 bind_tools 注入了什么
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("🔍 方法 2：bind_tools() 注入的 kwargs（每次 API 调用都会附带这些）")
print("=" * 70)

llm_with_tools = llm.bind_tools(tools)

# bind_tools 返回的是 RunnableBinding，它的 kwargs 里存着注入的工具定义
# 这就是每次 invoke 时附加到 API 请求里的 "tools" 字段
bound_kwargs = llm_with_tools.kwargs
print(json.dumps(bound_kwargs, indent=2, ensure_ascii=False))

# ═══════════════════════════════════════════════════════════════════════
# 方法 3：set_debug(True) — 打印 LangChain 内部所有步骤
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("🔍 方法 3：set_debug(True) — LangChain 会打印所有内部步骤")
print("=" * 70)

from langchain_core.globals import set_debug
set_debug(True)   # 开启后，每次 invoke 都会打印输入/输出细节

question = "组件 auth-service 有多少条编码规范违规？"
messages = [HumanMessage(content=question)]

print(f"\n>>> 第一轮调用：发送问题 + 工具清单 <<<\n")
ai_msg = llm_with_tools.invoke(messages)

if ai_msg.tool_calls:
    messages.append(ai_msg)
    tc = ai_msg.tool_calls[0]
    selected_tool = {t.name: t for t in tools}[tc["name"]]
    result = selected_tool.invoke(tc)
    tool_msg = ToolMessage(content=str(result), tool_call_id=tc["id"])
    messages.append(tool_msg)

    print(f"\n>>> 第二轮调用：发送对话历史 + 工具执行结果 <<<\n")
    final = llm_with_tools.invoke(messages)
    print(f"\n🤖 最终回答: {final.content}")

set_debug(False)  # 关闭 debug，避免污染后续输出

# ═══════════════════════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("📋 总结：LangChain 在 Tool Calling 中到底注入了什么？")
print("=" * 70)
print("""
1. LangChain 没有注入额外的 system prompt！
   Tool Calling 走的是 OpenAI API 的原生协议——工具定义作为独立的
   "tools" 字段发送，和 messages 是平级的，不是拼进 prompt 里的。

2. API 请求的结构（简化版）：
   {
     "model": "deepseek-v4-flash",
     "messages": [
       {"role": "user", "content": "组件 auth-service 有多少条违规？"}
     ],
     "tools": [                              ← bind_tools 注入
       {
         "type": "function",
         "function": {
           "name": "count_violations",
           "description": "查询指定组件的...",  ← 来自 docstring
           "parameters": { ... }               ← 来自类型注解
         }
       },
       ...
     ],
     "temperature": 0
   }

3. 第二轮调用时，messages 变成：
   [
     {"role": "user",      "content": "组件 auth-service..."},
     {"role": "assistant", "content": null,
      "tool_calls": [{"id": "call_xxx", "function": {...}}]},
     {"role": "tool",      "content": "12",
      "tool_call_id": "call_xxx"}              ← ToolMessage
   ]

4. 关键区别：
   - 某些不支持原生 tool calling 的模型（如早期开源模型），
     框架会把工具描述拼进 system prompt 里模拟 tool calling
   - DeepSeek/OpenAI 等支持原生 tool calling 的 API，
     工具定义走独立的 "tools" 字段，不污染 prompt
""")
