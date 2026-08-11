# 0007 — LCEL 重写 RAG：从手写到框架，RunnablePassthrough 的使用

## Date
2026-08-07

## Context
在 Lesson 0004 中，用户手写了 60 行代码的 RAG，包括自行计算相似度、处理 `Chroma` 向量库的原始结果、并利用 `SIM_THRESHOLD` 实现基于分数的门控。在 Lesson 0005 中，用户了解了 LangChain 的基础 LCEL `prompt | llm | parser`。
本课（Lesson 0006）的目标是：将两者结合，用 LangChain 的推荐组件（`langchain-chroma`）替代 Week 1 的手写检索逻辑，并使用字典 `RunnablePassthrough` 来构建输入上下文，将手写版缩减至 6 行左右。

## Insight
**核心概念 1：VectorStore as Retriever 与内置门控**
原先手写的 1 - distance 计算被 `langchain_chroma.Chroma` 封装。调用 `vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5, "k": 3})` 时，Chroma 返回低于阈值的文档将被自动滤除，返回空列表。

**核心概念 2：并行数据准备与 RunnablePassthrough**
为了满足 Prompt 需要的 `{context}` 和 `{question}` 两个占位符，我们将用户的单字符串输入（Query）“兵分两路”：
```python
setup_and_retrieval = {
    "context": retriever | format_docs,   # 检索文本流
    "question": RunnablePassthrough()     # 原样透传查询
}
```
此时 `chain.invoke("查询内容")` 可以将字符串同时派发给两条分支，完美组装成含有双 Key 的字典送入 prompt。

**Week 1 门控 vs Week 2 门控**
- Week 1: 在 Python 层执行 `if sims[0] < threshold:` 提前 `return`，完全不调用 LLM（省 token）。
- Week 2: Retriever 返回空列表 `[]`，经 `format_docs` 转换为 `""`。大模型依然会被调用，但在空上下文和系统提示词（“文档中没有的信息请明确说明”）的约束下产生拒答。这是标准 LCEL 管道的做法，与手写版存在微小区别（已在任务中说明）。

## Caveat
- 使用了现代 LangChain 推荐包 `langchain-chroma` (而不是废弃的 `langchain-community` chroma)，符合业界当前最佳实践。
- 在 1.x 中，遇到低于阈值的结果返回空，如果不加处理直接传给模型并无大碍，但复杂的应用可以通过自定义 `RunnableLambda` 彻底抛出异常中断调用，为了避免学习曲线过陡，本课采用了“放任 LLM 拒答”策略。

## Implications
- 检索部分已经完成 LCEL 迁移。下一个步骤是解决 Chunking，引入 `Document Loaders` 和 `RecursiveCharacterTextSplitter` 替代手写的 `split("\n\n")`。
- “透传”思想是 LangChain Graph (LangGraph) 的预演，数据的 State 流转在后面会更加明显。

## Status
Active — Week 2 核心重构完成。相关：[[0004-rag-mvp-milestone]]
