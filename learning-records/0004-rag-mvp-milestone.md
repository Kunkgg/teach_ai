# 0004 — 可信文档问答 MVP：门控防幻觉 + 来源引用

## Date
2026-08-05

## Context
用户完成 Lesson 3（向量库 + chunking），有了一个能跑的 RAG 脚本 `07_rag_chromadb.py`。但它有三个缺口：① 不可复用（过程式脚本）② 不可交互 ③ **会瞎编**——问库外问题仍会从不相关 chunk 编出答案。Week 1 的目标是"可信文档问答 MVP"，必须补齐这些。

## Insight
**一个"可信"的 RAG 必须在生成之前就拦住"没答案"的问题，并且每条结论都能追溯来源。** 这节课把这套工程化做进去：

1. **封装**：把脚本重构成 `TrustRAG` 类，关注点分离——`index_documents()` 建索引一次，`ask()` 问答多次。对外只暴露 `ask(question)`。文件命名从编号脚本（`07_...`）升级为语义化模块（`rag.py`），标志从一次性脚本毕业到可复用模块。
2. **相似度门控（relevance threshold）= 防幻觉第一道防线**：把 ChromaDB 的 cosine distance 换算回 similarity（`sim = 1 - dist`），若最相关 chunk 的相似度 < `SIM_THRESHOLD`（起始 0.5）则**直接拒答、不调用 LLM**。在生成前拦截，比生成后判断更省、更可靠。
3. **阈值是经验值**：相关 ~0.6–0.85，无关 ~0.2–0.4。lesson 把相似度打印出来让用户观察、自己调——这是 RAG 工程最常调的参数。
4. **来源引用（citation）= 可追溯**：`ask()` 返回 `(answer, similarities)`，展示给用户即可验证。这正契合可信看板"每个结论可追溯到规范"的灵魂。

## Implications
- Week 2 LangChain 重写这套 RAG 时，要明确对照："LangChain 没做魔法，只是把 Week 1 手写的 retrieve→augment→generate 封装成可组合积木（retriever | prompt | llm | parser）"。手写版是理解框架的基础，**不要跳过**。
- 门控只是防幻觉起点；生产级还需 reranking、LLM-as-judge、引用精确匹配（Week 2–4 引入）。
- `SIM_THRESHOLD` 因 embedding 模型/语料而异，换模型要重调。
- Week 1 里程碑达成：可信文档问答 MVP。建议用户把 `rag.py` + `qa.py` 提交 git 作为阶段性成果。

## Status
Active — Week 1 收官里程碑。相关：[[0003-vector-db-and-chunking]]、[[0002-deepseek-zhipu-api-combo]]。
