# 0003 — 向量数据库与 Chunking：从手动 list 到 ChromaDB

## Date
2026-08-05

## Context
用户已完成 Lesson 2 的 Mini RAG（Python list 存向量 + 手动遍历算余弦相似度 + 取最高分喂给 DeepSeek）。这个方案能跑通，但有两个硬伤：检索是 O(n) 暴力搜索无法扩展，且程序退出数据即丢失。Week 1 的目标是"可信文档问答 MVP"，必须引入向量数据库和文档切分。

## Insight
**ChromaDB 存的是你给它的向量 —— 只要显式传入 `embeddings=`，它就不会触发默认 embedding 模型的下载。** 这个认知让教学设计可以保持一致性：

1. Lesson 3 继续用智谱 `embedding-3` 手动算向量，再传给 ChromaDB —— 和 Lesson 2 完全同一套 embedding，无缝衔接
2. "embedding function 自动 embedding"这个抽象留到 Week 2（LangChain）再引入，避免在基础课里同时讲两件新事
3. 配置 `metadata={"hnsw:space": "cosine"}` 让 ChromaDB 的 distance 和 Lesson 2 的余弦相似度心智模型对齐（distance ≈ 1 − cosine_sim，越小越相似）

第二个核心认知：**Chunking 是 RAG 检索质量的命脉。** 理想 chunk 主题单一且语义完整 —— 太大则混杂多主题检索不精准，太小则上下文碎片化。本课用最自然的"按段落切分"，递归切分（RecursiveCharacterTextSplitter）留到 Week 2。

## Implications
- 后续 LangChain 课程引入 `OpenAIEmbeddings` / ChromaDB embedding function 时，要明确指出"这就是 Lesson 3 手动 embedding 的自动化版本"，建立概念桥梁
- API key 正式改为 `.env` + `dotenv`（`GLM_KEY` / `DS_KEY`），告别硬编码 —— 这是 LangChain 等框架的标准做法
- ChromaDB `query()` 返回嵌套列表（`results["documents"][0]`），且结果已按相似度排好，无需手动 sort —— 与 Lesson 2 的手动 sort 形成对比
- Week 1 收官（Lesson 4）：把这套 RAG 封装成可复用模块 + 交互式问答 demo

## Status
Active — 决定了向量数据库的教学路径和 embedding 处理方式。相关：[[0002-deepseek-zhipu-api-combo]]。
