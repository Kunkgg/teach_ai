import chromadb
from openai import OpenAI
from teach_ai.envs import GLM_KEY

# 智谱客户端（做 Embedding）
zhipu = OpenAI(api_key=GLM_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")

# ── Step 1: 建一个持久化客户端 + 集合 ──
# 数据会写到 ./chroma_db 文件夹，程序重启后还在
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="trust_basics",
    configuration={"hnsw": {"space": "cosine"}},   # 用 cosine 距离，和 Lesson 2 一致
)

# ── Step 2: 准备 3 段文本，用智谱转成向量 ──
texts = [
    "编码规范检查用静态分析工具扫描源代码，发现命名、格式等问题。",
    "可信构建在可追溯的环境中执行构建，防止供应链攻击。",
    "代码度量用圈复杂度、重复率等指标量化评估代码质量。",
]
emb_resp = zhipu.embeddings.create(model="embedding-3", input=texts)
vectors = [item.embedding for item in emb_resp.data]

# ── Step 3: 存入 ChromaDB（注意我们手动传了 embeddings）──
collection.upsert(
    ids=["b1", "b2", "b3"],
    documents=texts,
    embeddings=vectors,
    metadatas=[{"topic": t[:4]} for t in ["编码规范", "可信构建", "代码度量"]],
)
print(f"集合里有 {collection.count()} 条记录")

# ── Step 4: 提一个问题，检索最相似的 2 条 ──
query = "怎么衡量代码质量？"
query_vec = zhipu.embeddings.create(model="embedding-3", input=[query]).data[0].embedding

results = collection.query(query_embeddings=[query_vec], n_results=2)

# results["documents"] 是嵌套列表 —— [0] 取第一个查询的结果
print("\n最相关的 2 条:")
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"  [距离 {dist:.4f}] {doc}")
