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

## Components (assets/)

- **style.css** — 共享样式（Tufte 风格、暗色模式、打印优化）
- **quiz.js / quiz.css** — 选择题组件
- **task.css** — 动手任务区块样式
- **copy-code.js** — 代码块一键复制（2026-08-05 新增）。新课程只需在 `</body>` 前加 `<script src="../assets/copy-code.js" defer></script>`。用户反馈：长代码手动拖拽复制浪费时间、打断节奏 —— 此组件解决该问题。
- **reveal（答案折叠）** — 暂以内联 `<style>` 存于 `exercise-0004-retrieve-cloze.html`（`details.reveal` 选择器）。Week 2 若多处复用，提升为 `assets/reveal.css` 共享组件。
