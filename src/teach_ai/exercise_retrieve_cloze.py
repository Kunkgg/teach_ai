"""练习（填空版）：补全 TrustRAG.retrieve()

新练习格式的 demo —— 骨架已搭好，你只需填 2 处「承载新概念」的空白。
boilerplate（import、client 初始化、ask 门控）都已提供；要填的是真正要学的那两行。

运行： uv run python src/teach_ai/exercise_retrieve_cloze.py

答案就在你自己的 src/teach_ai/rag.py 第 44–51 行 —— 先别看，卡住再瞄。
"""
import chromadb
from openai import OpenAI
from teach_ai.envs import GLM_KEY, DS_KEY

EMBED_MODEL = "embedding-3"
CHAT_MODEL = "deepseek-v4-flash"
SIM_THRESHOLD = 0.5


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
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    def _embed(self, texts):
        """用智谱把文本列表转成向量列表。"""
        resp = self.zhipu.embeddings.create(model=EMBED_MODEL, input=texts)
        return [item.embedding for item in resp.data]

    def index_documents(self, text):
        chunks = self._split(text)
        vectors = self._embed(chunks)
        self.collection.upsert(
            ids=[f"chunk-{i}" for i in range(len(chunks))],
            documents=chunks,
            embeddings=vectors,
            metadatas=[{"index": i} for i in range(len(chunks))],
        )
        return len(chunks)

    # ╔════════════════════════════════════════════════════════════╗
    # ║  👇 只有这个方法要你动手 —— 填完两处 ____ ，其余别改。       ║
    # ╚════════════════════════════════════════════════════════════╝
    def retrieve(self, query, k=3):
        """检索 top-k 相关 chunk，返回 (chunks, similarities)。"""
        # ① 把 query 转成向量（必须和文档用同一个 embedding 模型 → 复用 self._embed）。
        #    _embed 接受「列表」、返回「列表」，所以包一层 [query] 再取 [0]。
        query_vec = self._embed(query)[0]

        # ② 查 ChromaDB —— 这行直接给你：API 的 kwarg 名没必要死记，用到时查文档即可。
        results = self.collection.query(query_embeddings=[query_vec], n_results=k)

        # ChromaDB 把结果按「第几次查询」嵌套；这里只查了 1 次 → documents/distances 都取 [0]
        chunks = results["documents"][0]

        # ③ ⭐ 核心概念：把 cosine distance 换算回 cosine similarity。
        #    distance 越小 = 越相似，所以 相似度 = 1 − distance。
        sims = [1 - dist for dist in results["distances"][0]]

        return chunks, sims

    def ask(self, query, k=3):
        """问答 = 检索 + 门控 + 生成（已写好，不用动）。"""
        chunks, sims = self.retrieve(query, k=k)
        if not chunks or sims[0] < SIM_THRESHOLD:
            return "抱歉，文档里没有与该问题相关的信息。", sims
        context = "\n\n".join(chunks)
        chat = self.deepseek.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": "你是可信工程助手。仅基于参考文档回答，不要编造。文档中没有的信息请明确说明。"},
                {"role": "user", "content": f"参考文档:\n{context}\n\n问题: {query}"},
            ],
            temperature=0.2,
            max_tokens=400,
        )
        return chat.choices[0].message.content, sims


TRUST_DOCS = """编码规范检查是可信工程的第一道防线。团队通过 ESLint、Pylint、SonarQube 等静态分析工具自动扫描源代码，识别不符合规范的命名、格式、复杂度等问题。检查结果同步到可信看板，按组件维度聚合，指导开发者逐项修复。

可信构建要求在可控、可追溯的环境中执行软件构建。每次构建的源码版本、依赖清单、构建参数都必须完整记录，确保产物与源码的对应关系可验证。这是防范供应链攻击、保证产物完整性的关键环节。

代码度量通过圈复杂度、代码行数、重复率、注释率等量化指标评估代码质量。可信看板将这些指标按模块可视化，帮助团队识别高风险、需重构的模块。通常圈复杂度超过 15 的函数会被标记为需要关注。

组件化是将复杂系统拆分为高内聚、低耦合的独立组件，每个组件有清晰的接口契约和版本管理。可信看板跟踪各组件的接口稳定性、依赖关系和变更频率，以此评估组件化成熟度。"""


if __name__ == "__main__":
    rag = TrustRAG()
    n = rag.index_documents(TRUST_DOCS)
    print(f"已索引 {n} 个 chunk\n")

    q = "代码圈复杂度超过多少需要关注？"
    chunks, sims = rag.retrieve(q)
    print(f"问题: {q}")
    for i, (c, s) in enumerate(zip(chunks, sims)):
        preview = c.replace("\n", " ")[:42]
        print(f"  [{i}] sim={s:.2f}  {preview}…")
    print()
    print("✅ 自检：")
    print("   • top-1 的 sim ≈ 0.6–0.85  →  ③ 填对了，检索正常")
    print("   • 如果 sim ≈ 1.3+           →  ③ 填反了（应为 1 − dist，不是 1 + dist）")
    print("   • 如果 NameError: ____      →  还有空白没填")
