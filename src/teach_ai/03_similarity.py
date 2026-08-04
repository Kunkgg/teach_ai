from openai import OpenAI

from teach_ai.envs import GLM_KEY

client = OpenAI(
    api_key=GLM_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)

# 四段测试文本 — 故意设计了两对"含义相近"的
texts = [
    "编码规范检查是对源代码进行静态分析的过程",       # A: 编码规范
    "代码审查用于发现代码中的质量问题和规范违规",       # B: 代码审查（和 A 相关）
    "可信构建确保软件构建过程的完整性和可追溯性",       # C: 可信构建
    "今天的天气真好，适合出去散步",                   # D: 无关内容
]

# 批量获取 Embedding（一次 API 调用搞定）
response = client.embeddings.create(
    model="embedding-3",
    input=texts,
)

# 提取向量列表
vectors = [item.embedding for item in response.data]


# 计算余弦相似度（不依赖外部库）
def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    return dot_product / (norm_a * norm_b)


# 打印相似度矩阵
labels = ["A:编码规范", "B:代码审查", "C:可信构建", "D:天气"]
print(f"{'':>12}", end="")
for label in labels:
    print(f"{label:>12}", end="")
print()

for i, row_label in enumerate(labels):
    print(f"{row_label:>12}", end="")
    for j in range(len(labels)):
        sim = cosine_similarity(vectors[i], vectors[j])
        print(f"{sim:>12.4f}", end="")
    print()
