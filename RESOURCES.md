# Resources

学习资源按信任等级和实用性排序。标记 `✅ 已验证` 表示内容已审查，`🔍 待审查` 表示尚未深入检查。

---

## Tier 1: 官方文档与一手资源（最高信任度）

### LangChain / LangGraph

- **LangChain Python Docs** ✅ 已验证
  - URL: https://python.langchain.com/docs/introduction/（已迁移到新域名 https://docs.langchain.com/oss/python/，旧链接会 308 跳转）
  - 备注: LCEL、Prompt Templates、Output Parsers 的权威参考
  - 适用: Week 2

- **LangChain — LLM Chain 教程** ✅ 已验证
  - URL: https://python.langchain.com/docs/tutorials/llm_chain/
  - 备注: 从 `ChatPromptTemplate` 一路搭到 `prompt | llm | parser` 的官方手把手教程。Lesson 0005 的主源——和用户写的代码几乎逐行对应
  - 适用: Week 2（Lesson 0005）

- **langchain-openai 集成文档** ✅ 已验证
  - URL: https://python.langchain.com/docs/integrations/chat/openai/
  - 备注: `ChatOpenAI` 的 `api_key=` / `base_url=` 用法（指向 DeepSeek 等 OpenAI 兼容端点）。注意官方说明 ChatOpenAI 只针对 OpenAI 标准——标准 chat 没问题，厂商私有扩展字段不保留
  - 适用: Week 2

- **LangGraph Docs** ✅ 已验证
  - URL: https://langchain-ai.github.io/langgraph/
  - 备注: StateGraph、Nodes/Edges、Checkpointing 的官方教程
  - 适用: Week 3

- **LangSmith Docs** 🔍 待审查
  - URL: https://docs.smith.langchain.com/
  - 备注: 可观测性和评估的官方文档
  - 适用: Week 4

### 向量数据库

- **ChromaDB Docs** 🔍 待审查
  - URL: https://docs.trychroma.com/
  - 备注: 轻量级向量数据库，适合入门和原型开发
  - 适用: Week 1

- **FAISS Wiki** 🔍 待审查
  - URL: https://github.com/facebookresearch/faiss/wiki
  - 备注: Facebook 出品的高性能向量搜索库
  - 适用: Week 1（了解原理）

### LLM API

- **OpenAI API Reference** ✅ 已验证
  - URL: https://platform.openai.com/docs/api-reference
  - 备注: Chat Completions、Embeddings API 参考
  - 适用: Week 1

- **Anthropic API Docs** ✅ 已验证
  - URL: https://docs.anthropic.com/
  - 备注: Claude API，Tool Use 的参考实现
  - 适用: Week 2

---

## Tier 2: 高质量课程与教程

### DeepLearning.AI 短课程（免费）

- **AI Agents in LangGraph** ✅ 已验证
  - URL: https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
  - 讲师: Harrison Chase (LangChain CEO)
  - 时长: ~1-2 小时
  - 备注: 官方出品，LangGraph agent 最权威的入门
  - 适用: Week 3

- **Retrieval Augmented Generation (RAG)** 🔍 待审查
  - URL: https://www.deeplearning.ai/short-courses/
  - 备注: 搜索 RAG 相关短课程
  - 适用: Week 1

- **Long-Term Agentic Memory with LangGraph** 🔍 待审查
  - URL: https://www.deeplearning.ai/short-courses/
  - 备注: Agent 的高级主题
  - 适用: Week 3-4

### LangChain Academy（官方课程）

- **LangChain Academy** 🔍 待审查
  - URL: https://academy.langchain.com/
  - 备注: 官方出品的项目制课程，包含 Deep Research with LangGraph 等
  - 适用: 全程参考

---

## Tier 3: 社区资源与路线图

### 路线图

- **roadmap.sh/ai-engineer** ✅ 已验证
  - URL: https://roadmap.sh/ai-engineer
  - 备注: 全面的 AI 工程师路线图，用于查漏补缺，但不适合线性学习
  - 用法: 作为知识地图参考，不作为学习主线

- **rohitg00/ai-engineering-from-scratch** ✅ 已验证
  - URL: https://github.com/rohitg00/ai-engineering-from-scratch
  - 备注: 500+ 课时、20 阶段、~320 小时。过于全面，不适合 1 个月周期。但可挑选 Phase 08-16 的部分课程参考
  - 用法: 选择性参考 RAG 和 Agent 相关章节

### AI Hero (Matt Pocock)

- **AI Hero** 🔍 待审查
  - URL: https://aihero.dev
  - 备注: Matt Pocock 创建的帮助 Web 开发者转型 AI 工程的平台
  - 适用: 了解工程化 AI 的方法论

---

## Tier 4: 中文社区与招聘参考

- **BOSS 直聘** — 搜索 "AI 工程师" 岗位，了解市场需求
- **脉脉** — AI 工程师社区交流
- **掘金 / 知乎** — RAG、LangChain 中文教程（需辨别质量）

---

## Tier 1.5: 文档解析引擎（生产级 RAG 核心）

### Docling (IBM)

- **Docling** ✅ 已验证
  - URL: https://github.com/DS4SD/docling
  - GitHub Stars: ~37K+（2026 年中）
  - 备注: IBM 开源的 AI 文档解析引擎。基于 DocLayNet 布局检测 + TableFormer 表格提取。PDF/DOCX/PPTX → 结构化 Markdown/JSON。有 LangChain 集成包 `langchain-docling`
  - 适用: 生产级文档解析，复杂 PDF（表格、多栏）

### MinerU / Magic-PDF (OpenDataLab)

- **MinerU** ✅ 已验证
  - URL: https://github.com/opendatalab/MinerU
  - GitHub Stars: ~76K+（2026 年中）
  - 备注: 上海 AI Lab 开源。**中文 PDF 解析最强**。公式→LaTeX、表格识别、多栏检测。`pip install magic-pdf`
  - 适用: 中文文档、学术论文、技术规范

### Marker (VikParuchuri)

- **Marker** 🔍 待审查
  - URL: https://github.com/VikParuchuri/marker
  - GitHub Stars: ~38K+
  - 备注: 深度学习 PDF→Markdown 转换。速度快（GPU）、多语言。`pip install marker-pdf`
  - 适用: 批量 PDF→Markdown 转换

### Unstructured.io

- **Unstructured** 🔍 待审查
  - URL: https://github.com/Unstructured-IO/unstructured
  - GitHub Stars: ~15K+
  - 备注: 支持 60+ 文档格式。开源库 + SaaS API。依赖链长，安装复杂
  - 适用: 多格式混合文档摄入

---

## 待添加

随着学习推进，持续补充优质资源。
