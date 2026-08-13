# 0008 — Document Loaders + RecursiveCharacterTextSplitter：从硬编码到文件加载、从粗切到智能切分

## Date
2026-08-11

## Context
Lesson 0006 完成后，LCEL RAG 链的检索和生成都已迁移到 LangChain 组件，但文档加载（硬编码字符串）和切分（`split("\n\n")`）仍沿用 Week 1 手写方式。本课（Lesson 0007）是 RAG pipeline 最后两块手写逻辑的框架化：
- `TextLoader` 替代 `TRUST_DOCS = """..."""` 硬编码
- `RecursiveCharacterTextSplitter` 替代 `text.split("\n\n")`

新增 `langchain-text-splitters` 和 `langchain-community` 两个包（langchain-text-splitters 1.1.2, langchain-community 0.4.2）。

## Insight
**核心概念 1：Document = page_content + metadata**
LangChain 的 `Document` 对象封装了文本和元数据。`TextLoader` 自动将文件路径写入 `metadata["source"]`，后续 RAG 回答时可以展示信息出处。这在 Week 1 手写版中完全缺失——chunk 丢失了来源信息。

**核心概念 2：RecursiveCharacterTextSplitter 的"递归"含义**
名字里的"Recursive"不是指 Python 递归函数，而是指：按分隔符优先级列表从粗到细依次尝试切分。默认 `["\n\n", "\n", " ", ""]`，中文文档通常需要补上 `"。"` 等中文标点。算法：先按段落切，如果某段超过 `chunk_size`，就递归地用下一级分隔符继续切。

**核心概念 3：chunk_overlap 防止边界信息丢失**
`chunk_overlap=30` 让相邻 chunk 重叠 30 字符。解决的问题：当一句话恰好在 chunk_size 边界处被切断，重叠区域确保下一个 chunk 包含这句话的尾部，不丢失检索线索。

**核心概念 4：split_text() vs split_documents()**
- `split_text(str)` 接收纯字符串，返回 `list[str]`——丢失 metadata
- `split_documents(list[Document])` 接收 Document 列表，返回 `list[Document]`——保留 metadata

## Caveat
- `langchain-community` 正在被 sunset。`TextLoader` 功能极简（底层就是 `open().read()` + 包装 Document），未来可能改用 `langchain-core` 的 `Document` 直接构造。但作为 LangChain 生态的标准模式，面试和真实项目中仍大量出现。
- 中文文档的 separators 需要手动加入中文标点（`"。"` / `"，"`），否则 RCTS 会从段落直接跳到空格或逐字符，切出不自然的片段。

## Implications
- 至此，RAG pipeline 六步（加载→切分→向量化→存储→检索→生成）全部完成 LangChain 迁移。Week 2 的 RAG 基础部分收官。
- 下一步进入 **Tool Calling**——Week 2 后半核心，也是从 RAG 到 Agent 的跳板。
- `MarkdownHeaderTextSplitter`（按标题层级切分并自动提取标题到 metadata）值得在进阶课程中介绍，但本课先用 RCTS 建立基础认知。

## Status
Completed — 用户已验证通过（5 chunks, ≤200 字符）。用户主动将 separators 中的 `"。"` 替换为 `","` 并去掉了 `" "`，说明在改造任务中独立思考了中文分隔符选择。

**用户反思（2026-08-12）**：「RAG 实际效果的很大一部分由数据的解析和 chunk 切分影响。面试的时候可能也会重点问这部分如何处理真实环境的数据。」这个判断非常准确——生产级 RAG 中，文档解析（PDF 表格/多栏/公式）和切分策略（语义切分 vs 固定长度、chunk_size 调优、metadata 丰富度）是决定检索质量的关键环节，也是面试高频考点。RESOURCES.md 已收录 Docling/MinerU/Marker 等生产级解析引擎，可在进阶课程中展开。

相关：[[0007-lcel-rag-migration]]、[[0003-vector-db-and-chunking]]

