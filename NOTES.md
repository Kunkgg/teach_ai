# Teaching Notes

## User Preferences

- 中英混合教学：技术术语用英文，解释用中文
- 偏好 Learn by doing，不喜欢纯理论学习
- 喜欢 Matt Pocock 的教学风格和 skills 框架
- 希望跳过数学基础部分，直接进入工程实践
- 已经在使用 AI 编程 agent（Claude Code / OpenCode / Antigravity CLI）
- 每天可投入 1-2 小时（工作日），周末 3-4 小时
- **代码练习偏好（2026-08-06 确认）**：「填空（cloze）+ 改造」而非整段复制 —— 只挖空承载新概念的那几行，逼回忆而非认读；boilerplate/API 照给；完整答案作 fallback

## Working Notes

- 用户的 Python 水平是中级（OOP、装饰器、生成器、后端 API），这意味着 LangChain/LangGraph 的 Python 语法不会是障碍
- "可信看板"项目是一个工程质量管控系统，包含代码规范检查、度量、构建可信度等维度 — 这和 AI 的结合点非常自然（RAG 查文档 + Agent 分析数据 + LangGraph 编排流程）
- 用户在外包公司工作，意味着他需要的不是科研能力，而是能快速落地的工程能力
- 1 个月 50-60 小时的学习时间是紧凑的，必须极度聚焦，每个 lesson 都要直接服务于最终项目
- Matt Pocock 的 AI Hero 项目值得关注 — 他的方法论（TDD、PRD、task decomposition）和用户当前使用 agent 的方式一致

## API Keys

- 用户只有 **智谱** 和 **DeepSeek** 的 API key
- 教学策略：DeepSeek 做 Chat，智谱做 Embedding
- 两者都是 OpenAI 兼容，用 `openai` 包即可

## Session Log

- **2026-08-03**: 初始化教学工作区。完成 Mission 定义、Resources 收集。
- **2026-08-04**: 用户完成 Lesson 1 四道题，浏览了 roadmap.sh。创建 Lesson 2（LLM API 调用：DeepSeek Chat + 智谱 Embedding + 余弦相似度 + Mini RAG）。
- **2026-08-05**: 用户完成 Lesson 2，理解了 Mini RAG 流程。新增 `assets/copy-code.js` 组件（所有 `<pre><code>` 代码块一键"复制"按钮，自包含、支持 file://，已应用到 Lesson 1/2/3）。创建 Lesson 3（向量数据库 ChromaDB + 文档切分 Chunking + 端到端 RAG）。API key 从硬编码升级为 `.env` 环境变量（`GLM_KEY` / `DS_KEY`，用户已有 `envs.py`）。Glossary 新增 ANN 词条、丰富 Chunking 词条。
- **2026-08-05 (续)**: 用户完成 Lesson 3（已验证：`src/teach_ai/05-07.py` 已建、`chroma_db/` 已持久化、git 干净）。ChromaDB distance 配置更正为官方推荐的 `configuration={"hnsw": {"space": ...}}`（旧版 `metadata={"hnsw:space":...}` 已弃用、曾有 bug）。创建 Lesson 4（Week 1 收官）：封装 `rag.py` 模块 + `TrustRAG` 类（`index_documents` / `retrieve` / `ask`）+ 相似度门控防幻觉（`SIM_THRESHOLD` 起始 0.5）+ 来源引用 + 交互式 `qa.py` CLI。**可信文档问答 MVP 达成，Week 1 里程碑完成**。
- **2026-08-06**: 用户完成 Lesson 4 后反思学习方法 —— 发现「复制→运行→读懂」建立的是 recognition（认读）而非 production（产出），存在「能力的错觉（illusion of competence）」。Mission 的成功标准（独立实现 + 面试讲清）要的是 production。**决定：从 Week 2 起代码练习改用「填空 + 改造」格式** —— 只挖空承载新概念的那 1–3 行、boilerplate/API-churn 照给、完整答案折叠在 `<details>` 里（用户已有文件即答案钥匙）。做了 demo：`lessons/exercise-0004-retrieve-cloze.html` + `src/teach_ai/exercise_retrieve_cloze.py`（补全 `retrieve()` 的 2 处空白）。用户试用后认可（"有一些效果"），正式采用。**此为影响后续所有 lesson 的教学法决策**，已存入记忆 `cloze-exercise-format`。
- **2026-08-06（续）**: 开始 **Week 2：LangChain / LCEL**。`uv add langchain langchain-openai` 装好（langchain 1.3.14 / langchain-core 1.5.3 / langchain-openai 1.4.1；langgraph 1.2.10 作为依赖一并装好，Week 3 直接可用）。创建 **Lesson 0005「Hello, LangChain」**——**第一个正式采用 cloze 格式的 lesson**（之前的 retrieve-cloze 是 demo）。核心教学：一张「Week 1 手写 → LangChain 积木」对照表（messages→prompt、create→llm、.choices[0].message.content→parser、手动串→`prompt | llm | parser`、手动调→`.invoke()`），落实 learning-record 0004「明确对照、框架没做魔法」的基调。cloze 留 2 处空白（template 构造 ② + 管道串联 ④），boilerplate/import 全给，完整答案在折叠 `<details>`。改造任务：加 `{tone}` 占位符逼整段理解。**端到端验证通过**（DeepSeek 经 LCEL 返回正常；`StrOutputParser` 在 1.x 返回 `TextAccessor`，确认是 `str` 子类，lesson 已加注）。新增 `assets/reveal.css` 共享组件（从 exercise-0004 的内联样式提升），含 `.reveal`（折叠答案）+ `.blank`（空格高亮）两块。Glossary：LangChain/LCEL/Prompt Template 标 首见 Lesson 0005 并充实；新增 Output Parser、Runnable 词条。
- **2026-08-07**: 用户对 embedding 做深度反思（4 个疑问：有损？词序/上下文怎么进向量？维度可解释吗？取值范围？单 token/乱码 embed 出什么？）。用用户自己的 embedding-3 实测回答（`/tmp/probe_embeddings.py`）。关键发现：① 向量 L2 归一化（norm=1.0000，含乱码），单分量 ~[-0.25,+0.27]、典型 0.016；② '狗咬人'vs'人咬狗' cos=0.897 → 词序被捕捉但仍很近（有损，弱于精细句法/否定）；③ 乱码 vs 有意义 ≈0.50–0.53，而真无关 0.307 → **乱码可骗过 SIM_THRESHOLD=0.5**，印证门控只是第一道防线。**正式落盘**：探针脚本搬到 `src/teach_ai/09_embedding_probe.py`；新增 learning-record 0006（embedding 内部结构与局限，**note：learning-record 编号自此与 lesson 编号解耦**）；glossary 的 Embedding 词条大幅充实（统计代理/分布式/归一化/局限）+ ANN 词条补"再近似一层"。这些是面试区分"调包 vs 理解"的关键认知。
- **2026-08-11**: 开始 **Lesson 0007（Document Loaders + RecursiveCharacterTextSplitter）**。`uv add langchain-text-splitters langchain-community`（langchain-text-splitters 1.1.2 / langchain-community 0.4.2）。核心教学：① `TextLoader` 替代硬编码文档字符串——自动带上 `metadata["source"]` 来源追踪；② `RecursiveCharacterTextSplitter` 替代 `split("\n\n")`——"Recursive"= 按分隔符优先级列表从粗到细递归切分，`chunk_size` / `chunk_overlap` / `separators` 三参数；③ `split_documents()` vs `split_text()` 的区别（保留 metadata vs 丢失）。新增 `trust_spec.md`（增强版可信规范文档，8 段 ~739 字符），验证切出 5 chunks、每段 ≤200。cloze 填空 3 处。**注意**：`langchain-community` 已被 sunset，lesson 中加了 callout 提示替代方案。Glossary 新增 Document / Document Loader / RecursiveCharacterTextSplitter 三个词条。**至此，RAG pipeline 六步（加载→切分→向量化→存储→检索→生成）全部完成 LangChain 迁移。**
- **2026-08-12**: 用户确认完成 Lesson 0007，反思：「RAG 实际效果的很大一部分由数据的解析和 chunk 切分影响。面试的时候可能也会重点问这部分如何处理真实环境的数据。」——判断精准，已记录到 learning-record 0008。开始 **Lesson 0008（Tool Calling）**——Week 2 后半核心，从 RAG 走向 Agent 的关键跳板。
- **2026-08-13**: 用户完成 Lesson 0008，做了 Week 2 整体回顾后进入 **Week 3: LangGraph + Agent 模式**。创建 **Lesson 0009「从 while 循环到状态图 — Hello, LangGraph」**——核心教学：① 对照 Lesson 8 手写 while 循环和 LangGraph StateGraph 的一一映射；② 四个新概念（State + add_messages reducer / Node / Edge + Conditional Edge / Compile）；③ `ToolNode` 和 `tools_condition` 预置组件替代手写循环；④ `create_react_agent` 一行封装。cloze 留 3 处空白（State 定义 + 条件边 + graph.invoke 调用）。LangGraph 版本 1.2.10（Week 2 初已安装）。
- **2026-08-19**: 用户完成 Lesson 0009，**首次主动读框架源码**并提出三个深入问题（Annotated 语义 / sys.intern 作用 / tools_condition 的节点名绑定）。全部经 venv 源码 + 实验验证后回答（发现用户对 Annotated 有「add_messages 是元素类型」的误解；sys.intern 实测性能差异为噪声级，如实告知；path_map 改名实验实测跑通）。创建 **Lesson 0010「源码三问」**（答疑课格式：Q&A + 触发 "unknown target" 报错再修复的 Task + 3 题 quiz）。Glossary 新增 Annotated / sys.intern 词条、tools_condition 词条补 path_map。**教学法信号：用户进入「读源码验证」阶段，后续 lesson 可引用 venv 源码路径。** MemorySaver 课顺延为 Lesson 0011。
- **2026-08-19 (续)**: 用户完成 Lesson 0010（源码三问），继续 Week 3。创建 **Lesson 0011「给 Agent 装上记忆：Checkpointer 与 thread_id」**（`15_memory_saver.py`，cloze 三空：① compile 挂 checkpointer、② config 双层嵌套、③ 第二轮 invoke 只传新消息）。核心教学：记忆 = 工程存取问题（对照 Week 1 qa.py 手写全局 messages）；reducer 管合并 / checkpointer 管保存的分工（直接衔接 LR 0012 的 add_messages）；thread_id ≈ 会话 ID 的后端类比；`InMemorySaver` 正式名 vs `MemorySaver` 兼容别名（源码 line 631，喂给读源码习惯）；compile 注入式设计 → 换 PostgresSaver 图代码零改动（面试点）；`get_state` 三件套 + `get_state_history` 留作 time travel 钩子。**端到端验证通过**（DeepSeek：第二轮"它"→get_trust_score("auth-service")=85.5 记忆生效；thread-2 答"没有之前的对话记录"隔离生效；两轮共 10 个 checkpoint）。实测不传 thread_id 的 ValueError 原文写入 quiz。Glossary 新增 Checkpoint / thread_id / StateSnapshot 词条。改造任务：15 改 `while True: input()` = qa.py 的 LangGraph 版（看板助手雏形）。下一课：interrupt() + HITL。


## Components (assets/)

- **style.css** — 共享样式（Tufte 风格、暗色模式、打印优化）
- **quiz.js / quiz.css** — 选择题组件
- **task.css** — 动手任务区块样式
- **copy-code.js** — 代码块一键复制（2026-08-05 新增）。新课程只需在 `</body>` 前加 `<script src="../assets/copy-code.js" defer></script>`。用户反馈：长代码手动拖拽复制浪费时间、打断节奏 —— 此组件解决该问题。
- **reveal.css** — cloze 课程的共享样式（2026-08-06 提升）。两块：`.reveal`（`<details>` 折叠答案）+ `.blank`（代码/正文里的空格高亮）。用法：`<link rel="stylesheet" href="../assets/reveal.css">`。从 `exercise-0004` 的内联样式提炼而来，Lesson 0005 起所有 cloze 课程复用。
