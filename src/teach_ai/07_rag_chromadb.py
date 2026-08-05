import chromadb
from openai import OpenAI
from teach_ai.envs import GLM_KEY, DS_KEY

# 两个客户端：智谱做 Embedding，DeepSeek 做 Chat
zhipu = OpenAI(api_key=GLM_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")
deepseek = OpenAI(api_key=DS_KEY, base_url="https://api.deepseek.com")

# ── Step 1: 文档 + 切分（复用 Task ② 的切分器）──
TRUST_DOCS = """编码规范检查是可信工程的第一道防线。团队通过 ESLint、Pylint、SonarQube 等静态分析工具自动扫描源代码，识别不符合规范的命名、格式、复杂度等问题。检查结果同步到可信看板，按组件维度聚合，指导开发者逐项修复。

可信构建要求在可控、可追溯的环境中执行软件构建。每次构建的源码版本、依赖清单、构建参数都必须完整记录，确保产物与源码的对应关系可验证。这是防范供应链攻击、保证产物完整性的关键环节。

代码度量通过圈复杂度、代码行数、重复率、注释率等量化指标评估代码质量。可信看板将这些指标按模块可视化，帮助团队识别高风险、需重构的模块。通常圈复杂度超过5 的函数会被标记为需要关注。

组件化是将复杂系统拆分为高内聚、低耦合的独立组件，每个组件有清晰的接口契约和版本管理。可信看板跟踪各组件的接口稳定性、依赖关系和变更频率，以此评估组件化成熟度。"""


def split_by_paragraph(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


chunks = split_by_paragraph(TRUST_DOCS)

# ── Step 2: 用智谱把每个 chunk 向量化 ──
emb_resp = zhipu.embeddings.create(model="embedding-3", input=chunks)
chunk_vectors = [item.embedding for item in emb_resp.data]

# ── Step 3: 存入 ChromaDB（持久化）──
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="trust_docs",
    configuration={"hnsw": {"space": "cosine"}},
)
collection.upsert(
    ids=[f"chunk-{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=chunk_vectors,
    metadatas=[{"source": "可信编码规范", "index": i} for i in range(len(chunks))],
)
print(f"已存入 {collection.count()} 条 chunk 到 ChromaDB")

# ── Step 4: 提问 → 向量化 → 检索 top-k ──
query = "代码圈复杂度超过多少需要关注？"
query_vec = zhipu.embeddings.create(model="embedding-3", input=[query]).data[0].embedding

results = collection.query(query_embeddings=[query_vec], n_results=2)
top_chunks = results["documents"][0]   # 嵌套结构，[0] 取第一个查询的结果

print(f"\n检索到 {len(top_chunks)} 条相关片段:")
for i, doc in enumerate(top_chunks):
    print(f"  [{i + 1}] {doc[:40]}...")

# ── Step 5: 拼接上下文 → DeepSeek 生成回答 ──
context = "\n\n".join(top_chunks)
chat = deepseek.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "你是可信工程助手。仅基于参考文档回答，不要编造。"
                       "文档中没有的信息请明确说明。",
        },
        {"role": "user", "content": f"参考文档:\n{context}\n\n问题: {query}"},
    ],
    temperature=0.2,
    max_tokens=300,
)

print("\n" + "─" * 50)
print(f"问题: {query}")
print(f"回答: {chat.choices[0].message.content}")


# ── Step 4: 提问 → 向量化 → 检索 top-k ──
query = "构建过程不可追溯, 违反了哪种可信要求?"
query_vec = zhipu.embeddings.create(model="embedding-3", input=[query]).data[0].embedding

results = collection.query(query_embeddings=[query_vec], n_results=2)
top_chunks = results["documents"][0]   # 嵌套结构，[0] 取第一个查询的结果

print(f"\n检索到 {len(top_chunks)} 条相关片段:")
for i, doc in enumerate(top_chunks):
    print(f"  [{i + 1}] {doc[:40]}...")

# ── Step 5: 拼接上下文 → DeepSeek 生成回答 ──
context = "\n\n".join(top_chunks)
chat = deepseek.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "你是可信工程助手。仅基于参考文档回答，不要编造。"
                       "文档中没有的信息请明确说明。",
        },
        {"role": "user", "content": f"参考文档:\n{context}\n\n问题: {query}"},
    ],
    temperature=0.2,
    max_tokens=300,
)

print("\n" + "─" * 50)
print(f"问题: {query}")
print(f"回答: {chat.choices[0].message.content}")


# ── Step 4: 提问 → 向量化 → 检索 top-k ──
query = "李明的孩子叫什么?"
query_vec = zhipu.embeddings.create(model="embedding-3", input=[query]).data[0].embedding

results = collection.query(query_embeddings=[query_vec], n_results=2)
top_chunks = results["documents"][0]   # 嵌套结构，[0] 取第一个查询的结果

print(f"\n检索到 {len(top_chunks)} 条相关片段:")
for i, doc in enumerate(top_chunks):
    print(f"  [{i + 1}] {doc[:40]}...")

# ── Step 5: 拼接上下文 → DeepSeek 生成回答 ──
context = "\n\n".join(top_chunks)
chat = deepseek.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "你是可信工程助手。仅基于参考文档回答，不要编造。"
                       "文档中没有的信息请明确说明。",
        },
        {"role": "user", "content": f"参考文档:\n{context}\n\n问题: {query}"},
    ],
    temperature=0.2,
    max_tokens=300,
)

print("\n" + "─" * 50)
print(f"问题: {query}")
print(f"回答: {chat.choices[0].message.content}")
