# 0005 — Hello, LangChain：手写的 prompt→llm→extract 打包成可组合积木

## Date
2026-08-06

## Context
Week 1 收官（Lesson 0004）后，用户有了一个手写的可信文档问答 MVP（`rag.py` + `qa.py`）。Week 2 引入 LangChain / LCEL。Learning record 0004 定下的基调：**"Week 2 LangChain 重写这套 RAG 时，要明确对照'LangChain 没做魔法，只是把 Week 1 手写的步骤封装成可组合的积木'。手写版是理解框架的基础，不要跳过。"** 本课是 Week 2 开篇，必须建立这个对照。

同一日（2026-08-06）用户确认从 Week 2 起代码练习改用**填空（cloze）格式**（见记忆 `cloze-exercise-format`）。本课是**第一个正式采用 cloze 的 lesson**（之前的 `exercise-0004-retrieve-cloze.html` 只是 demo）。

## Insight
**LangChain 的"Hello World"= 把 `01_chat.py` 的三件事各拆成一块可组合积木，再用 `|` 串起来。** 一一对照：

| Week 1 手写（`01_chat.py`） | LangChain 积木 | 角色 |
|---|---|---|
| `messages=[{"role":"system",...},{"role":"user",...}]` | `ChatPromptTemplate.from_messages([...])` | **prompt** |
| `client.chat.completions.create(...)` + `OpenAI` 客户端 | `ChatOpenAI(...)` | **llm** |
| `response.choices[0].message.content` | `StrOutputParser()` | **parser** |
| 上面三步手动串 | `prompt \| llm \| parser` → `RunnableSequence` | **chain** |
| 手动调用 + 手动提取 | `chain.invoke({"question": ...})` | 触发 |

三个关键概念：
1. **Prompt Template > f-string**：占位符（`{question}`）与内容分离 → 同一模板可用不同输入复用、可校验、可塞进链里。这正是把它从"一次性脚本变量"提升为"可组合组件"的关键。
2. **LCEL 管道（`|`）**：声明式地表达数据流——上一个组件的输出自动喂给下一个。`prompt | llm | parser` 产出 `RunnableSequence`。
3. **统一 `invoke` 接口**：每块积木（prompt / llm / parser / chain）都是 `Runnable`，都有 `.invoke()`。这是为什么能随便用 `|` 串联——接口统一，输出即下一个的输入。

环境：`uv add langchain langchain-openai`（得到 langchain 1.3.14 / langchain-core 1.5.3 / langchain-openai 1.4.1；langgraph 1.2.10 作为依赖一并装好，Week 3 直接可用）。

## Caveat（已记入 lesson callout）
- `langchain-openai.ChatOpenAI` 官方说明"只针对 OpenAI 标准"——DeepSeek 的标准 chat 完全可用（已端到端验证），但厂商私有扩展字段（如 reasoning_content）不会被保留。需要那些扩展时考虑厂商专用集成包。
- `StrOutputParser()` 在 langchain-core 1.x 返回 `TextAccessor` 而非裸 `str`——但它是 `str` 子类（`isinstance(x, str)` 为 True），所有字符串操作照常。已在 lesson 注明，免得用户 `print(type(answer))` 时困惑。

## Implications
- 下一步（Lesson 0006）把 Week 1 **整条 RAG** 用 LCEL 重写：`retriever | prompt | llm | parser`，并引入 `Runnable` 链里的相似度门控。要持续做"手写 → 框架"对照。
- Document Loaders + `RecursiveCharacterTextSplitter` 替换手写的 `split("\n\n")`（Lesson 0007 左右）。
- Tool Calling 是 Week 2 后半，Agent 的入口。
- Cloze 格式首次落地：本课留 2 处空白（template 构造 + 管道串联），粒度与 demo 一致；若用户反馈太易/太难，按 `cloze-exercise-format` 记忆调粒度。

## Status
Active — Week 2 开篇。相关：[[0004-rag-mvp-milestone]]、[[cloze-exercise-format]]（记忆）。
