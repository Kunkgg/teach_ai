import chromadb
from openai import OpenAI
from teach_ai.envs import GLM_KEY, DS_KEY

EMBED_MODEL = "embedding-3"
CHAT_MODEL = "deepseek-v4-flash"
SIM_THRESHOLD = 0.5   # 低于这个相似度视为"文档里没有" —— 运行后根据观察调整


class TrustRAG:
    """可信文档问答：建索引一次，问答多次。"""

    def __init__(self, db_path="./chroma_db", collection="trust_docs"):
        self.zhipu = OpenAI(api_key=GLM_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")
        self.deepseek = OpenAI(api_key=DS_KEY, base_url="https://api.deepseek.com")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection,
            configuration={"hnsw": {"space": "cosine"}},
        )

    @staticmethod
    def _split(text):
        """按段落切分（复用 Lesson 3 的切分器）。"""
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    def _embed(self, texts):
        """用智谱把文本列表转成向量列表。"""
        resp = self.zhipu.embeddings.create(model=EMBED_MODEL, input=texts)
        return [item.embedding for item in resp.data]

    def index_documents(self, text):
        """切分 → 向量化 → 存入 ChromaDB。建索引，文档变更时调一次即可。"""
        chunks = self._split(text)
        vectors = self._embed(chunks)
        self.collection.upsert(
            ids=[f"chunk-{i}" for i in range(len(chunks))],
            documents=chunks,
            embeddings=vectors,
            metadatas=[{"index": i} for i in range(len(chunks))],
        )
        return len(chunks)

    def retrieve(self, query, k=3):
        """检索 top-k 相关 chunk，返回 (chunks, similarities)。"""
        query_vec = self._embed([query])[0]
        results = self.collection.query(query_embeddings=[query_vec], n_results=k)
        chunks = results["documents"][0]
        # cosine distance → cosine similarity（越大越相似）
        sims = [1 - dist for dist in results["distances"][0]]
        return chunks, sims

    def ask(self, query, k=3):
        """问答 = 检索 + 门控 + 生成。返回 (answer, similarities)。"""
        chunks, sims = self.retrieve(query, k=k)

        # ── 门控：最相关 chunk 的相似度太低 → 文档里没有，不瞎编 ──
        # sims 已按相似度从高到低排好，sims[0] 就是最相关的那条
        if not chunks or sims[0] < SIM_THRESHOLD:
            return "抱歉，文档里没有与该问题相关的信息。", sims

        # ── 通过门控：拼接上下文，调用 DeepSeek 生成 ──
        context = "\n\n".join(chunks)
        chat = self.deepseek.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是可信工程助手。仅基于参考文档回答，不要编造。"
                               "文档中没有的信息请明确说明。",
                },
                {"role": "user", "content": f"参考文档:\n{context}\n\n问题: {query}"},
            ],
            temperature=0.2,
            max_tokens=400,
        )
        return chat.choices[0].message.content, sims
