"""Lesson 0007 — Document Loaders + RecursiveCharacterTextSplitter（填空版）。

Week 1 的 06_chunking.py 用 split("\n\n") 把硬编码的文档切分成段落。
本课用 LangChain 的标准组件替代：
  1. TextLoader 从真实的 .md 文件加载文档
  2. RecursiveCharacterTextSplitter 按层级智能切分

填三处空白（标 ①②③），跑通后打印出切分后的 chunks 及其 metadata。

运行（项目根目录）：
    uv run python src/teach_ai/11_doc_loader_splitter.py
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── 1. 加载文档 ──

# TODO(①): 用 TextLoader 加载可信编码规范文档
#   参数 1: 文件路径 "src/teach_ai/trust_spec.md"
#   参数 2: encoding="utf-8"
loader = ____

docs = loader.load()
print(f"✅ 加载了 {len(docs)} 个 Document 对象")
print(f"   page_content 长度: {len(docs[0].page_content)} 字符")
print(f"   metadata: {docs[0].metadata}")
print()

# ── 2. 切分文档 ──

# TODO(②): 创建 RecursiveCharacterTextSplitter
#   参数 1: chunk_size=200   （每块最多 200 字符）
#   参数 2: chunk_overlap=30  （相邻 chunk 重叠 30 字符，防断裂）
#   参数 3: separators=["\n\n", "\n", "。", " ", ""]
#            （先按段落、再按行、再按句号、再按空格、最后逐字符——这就是"递归"的含义）
splitter = ____

# TODO(③): 把 docs 切分成 chunks
#   提示：用 splitter 的哪个方法？split_text 接收 str，split_documents 接收 list[Document]
chunks = ____

# ── 3. 展示结果 ──
print(f"切分为 {len(chunks)} 个 chunks:\n")
for i, chunk in enumerate(chunks):
    print(f"── chunk {i} ({len(chunk.page_content)} 字符) ──")
    print(chunk.page_content)
    print(f"   metadata: {chunk.metadata}")
    print()

# ── 4. 对比 Week 1 的手写版 ──
print("=" * 50)
print("对比 Week 1 的 split('\\n\\n'):")
print(f"  手写版: 按空行分 → 只能切成 4 段，每段长度不可控")
print(f"  RCTS:   先按段落切，太长的段落继续往下切 → {len(chunks)} 段，每段 ≤200 字符")
print(f"  而且每段都有 metadata（来源文件路径），后续 RAG 可以展示出处！")
