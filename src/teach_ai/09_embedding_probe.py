"""Embedding 内部结构探针 —— 用你自己的智谱 embedding-3 实测。

回答四个疑问（详解见 learning-records/0006-embedding-internals-deep-dive.md）：
  - Q2   每个维度的取值范围？向量是否归一化？
  - 核心  词序/上下文怎么被压进一个定长向量？
  - Q3   单个 token / 无意义组合，embed 出来是什么？

运行（项目根目录）：
    uv run python src/teach_ai/09_embedding_probe.py

实测要点（embedding-3, 2048 维，输出稳定）：
  - 所有向量 L2 norm = 1.0000（归一化到单位超球面）
  - 单分量约 [-0.25, +0.27]，典型 ~0.016
  - '狗咬人' vs '人咬狗' cos ≈ 0.90 → 顺序被捕捉，但仍很近（有损）
  - 近义 ≈ 0.74（高）、无关 ≈ 0.31（低）
  - 乱码 vs 有意义 ≈ 0.50–0.53 → 可能骗过 0.5 的相似度门控
"""
import math

from openai import OpenAI

from teach_ai.envs import GLM_KEY

client = OpenAI(api_key=GLM_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")

# 实验文本：每组对应一个要回答的问题
TEXTS = [
    "狗咬人",                          # 0  ─┐ 词序对照
    "人咬狗",                          # 1  ─┘
    "the dog bit the man",            # 2  ─┐ 英文词序翻转
    "the man bit the dog",            # 3  ─┘
    "编码规范检查是第一道防线",        # 4  ─┐ 近义
    "代码规范扫描自动识别问题",        # 5  ─┘
    "红烧肉怎么做",                    # 6    无关
    "我",                              # 7  ─┐ 单 token
    "的",                              # 8  ─┤
    "for",                             # 9  ─┤
    "a",                               # 10 ─┘
    "的afor我xyzqwer",                 # 11   无意义组合
    "asdf jkl; qwer zxcv",            # 12   纯乱码
]

resp = client.embeddings.create(model="embedding-3", input=TEXTS)
VECS = [d.embedding for d in resp.data]
DIM = len(VECS[0])


def stats(i):
    """打印某个文本向量的维度、范数、分量范围。"""
    v = VECS[i]
    norm = math.sqrt(sum(x * x for x in v))
    mean_abs = sum(abs(x) for x in v) / len(v)
    print(f"    '{TEXTS[i]}'")
    print(f"      dim={DIM}  L2 norm={norm:.4f}  "
          f"min={min(v):+.4f}  max={max(v):+.4f}  mean|comp|={mean_abs:.4f}")


def cos(i, j):
    a, b = VECS[i], VECS[j]
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)


def show(i, j):
    print(f"    cos({TEXTS[i]!r:22} , {TEXTS[j]!r:22}) = {cos(i, j):+.3f}")


print(f"=== Q2：取值范围 & 是否归一化（embedding-3, dim={DIM}） ===")
stats(4)   # 有意义句子
stats(7)   # 单 token
stats(12)  # 纯乱码
print("    → 全部 norm≈1：返回前 L2 归一化，向量落在单位超球面；")
print("      单分量 ~[-0.25, +0.27]，典型 ~0.016；故 cosine ∈ [-1, 1]。")

print("\n=== 核心疑问：词序/上下文如何进向量？ ===")
show(0, 1)
show(2, 3)
print("    → 顺序确实改变向量（≈0.90，不是 1.0）；但 0.90 仍很高")
print("      → embedding 擅长【主题相似】，弱于【精细句法 / 逻辑方向 / 否定】。有损。")

print("\n=== 近义该近、无关该远 ===")
show(4, 5)
show(4, 6)
print("    → 近义 ≈0.74（高），无关 ≈0.31（低）—— 相似度门控的有效区间。")

print("\n=== Q3：单 token / 无意义组合 ===")
show(7, 8)
show(9, 10)
show(11, 4)
show(12, 4)
show(11, 12)
print("    → 任何字符串都有向量；常见单字 / 功能词聚成一块（≈0.68–0.75）；")
print("      乱码 vs 有意义 ≈0.50–0.53 → 可能骗过 0.5 的相似度门控。")
print("      结论：门控只是防幻觉【第一道】防线，后面还需 rerank / LLM-as-judge。")
