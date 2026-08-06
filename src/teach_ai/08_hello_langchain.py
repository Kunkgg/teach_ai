"""Lesson 0005 — Hello, LangChain：Prompt Template + 最简 LCEL 链（填空版）。

填两处空白（标 ② 和 ④），跑通后你应该得到和 Lesson 1 的 `01_chat.py` 一样的回答。
先别看 `lessons/0005-langchain-lcel.html` 最下面的折叠答案，自己填 —— 卡住再瞄。

运行（项目根目录）：
    uv run python src/teach_ai/08_hello_langchain.py
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from teach_ai.envs import DS_KEY

# ── 三块积木之一：LLM（和 Lesson 1 的 OpenAI 客户端对照，只是换了层包装）────
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=DS_KEY,
    base_url="https://api.deepseek.com",
    temperature=0,
    max_tokens=100,
)

# ── 三块积木之二：Prompt Template（占位符 {question} 在 invoke 时才填入）──────
# TODO(②): 用 ChatPromptTemplate.from_messages([...]) 构造。
#   传一个「列表」，两条消息（顺序就是 system → user）：
#     ("system", "你是可信工程助手，帮助开发者理解编码规范和可信构建流程。")
#     ("user", "{question}")
prompt = None

# ── 三块积木之三：输出解析器（把 LLM 返回的 AIMessage 里的文本抠出来）────────
parser = StrOutputParser()

# ── ⭐ 核心一行：LCEL 管道，用 | 把三块积木按顺序串起来 ───────────────────────
# TODO(④): 用管道符 | 把 prompt → llm → parser 这个顺序串起来，赋值给 chain。
chain = None

# ── 触发：填入占位符 {question}，跑通整条链（answer 就是一段纯文本字符串）────
answer = chain.invoke({"question": "什么是编码规范检查？用一句话解释。"})
print(answer)


# ════════════════════════════════════════════════════════════════════════════
# 🧪 改造任务（上面的填空跑通后再做）——让模板多一个「风格」占位符
#   1. 把 user 那条消息改成："用{tone}的方式回答：{question}"
#   2. invoke 时同时传两个字段：
#        chain.invoke({"question": "什么是编码规范检查？", "tone": "简洁"})
#        chain.invoke({"question": "什么是编码规范检查？", "tone": "详细举例"})
#      各跑一次，对比两份答案。
#   这正是 Prompt Template 比 f-string 强的地方：同一套模板、不同输入，复用同一条 chain。
# ════════════════════════════════════════════════════════════════════════════
