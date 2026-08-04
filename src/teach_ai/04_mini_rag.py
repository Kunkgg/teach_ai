from openai import OpenAI
from teach_ai.envs import GLM_KEY, DS_KEY

# 两个客户端 — 不同厂商，同一个 SDK
zhipu = OpenAI(
    api_key=GLM_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)
deepseek = OpenAI(
    api_key=DS_KEY,
    base_url="https://api.deepseek.com",
)

# ── Step 1: 准备"知识库"（3 段文档） ──
documents = [
    "编码规范检查通过静态分析工具（如 ESLint、Pylint）自动扫描源代码，"
    "识别不符合团队编码规范的代码模式，包括命名规范、代码格式、复杂度等。",
    "可信构建是指在可控、可追溯的环境中执行软件构建，"
    "确保构建产物与源代码的对应关系可验证，防止供应链攻击。",
    "代码度量通过量化指标（如圈复杂度、代码行数、重复率）"
    "评估代码质量，帮助团队识别需要重构的高风险模块。",
]

# ── Step 2: 用智谱把文档 + 查询都变成向量 ──
query = "我们的代码规范检查具体检查哪些方面？"

# 批量 embedding：文档 + 查询一起发
all_texts = documents + [query]
emb_response = zhipu.embeddings.create(
    model="embedding-3",
    input=all_texts,
)
all_vectors = [item.embedding for item in emb_response.data]

doc_vectors = all_vectors[:3]  # 前 3 个是文档向量
query_vector = all_vectors[3]  # 最后一个是查询向量


# ── Step 3: 找到最相关的文档（余弦相似度） ──
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot / (norm_a * norm_b)


scores = []
for i, doc_vec in enumerate(doc_vectors):
    sim = cosine_similarity(query_vector, doc_vec)
    scores.append((sim, i))
    print(f"文档 {i+1} 相似度: {sim:.4f}")

# 取相似度最高的文档
scores.sort(reverse=True)
best_idx = scores[0][1]
best_doc = documents[best_idx]
print(f"\n最相关文档: 文档 {best_idx + 1}")
print(f"内容: {best_doc}\n")

# ── Step 4: 用 DeepSeek 基于文档回答问题 ──
chat_response = deepseek.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "你是一个可信工程助手。请仅基于提供的参考文档回答问题，"
            "不要编造信息。如果文档中没有相关信息，请明确说明。",
        },
        {"role": "user", "content": f"参考文档:\n{best_doc}\n\n问题: {query}"},
    ],
    temperature=0.2,
    max_tokens=300,
)

print("─" * 50)
print(f"问题: {query}")
print(f"回答: {chat_response.choices[0].message.content}")
