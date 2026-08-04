from openai import OpenAI

from teach_ai.envs import GLM_KEY
from teach_ai.utils import dump_response

print(GLM_KEY)
# 创建智谱客户端 — 同样的 openai 包，不同的 base_url
client = OpenAI(
    api_key=GLM_KEY,                          # ← 替换
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)

# 调用 Embedding API
response = client.embeddings.create(
    model="embedding-3",
    input="什么是编码规范检查？",
)

fn_o = "tests/02_embedding_response.json"
dump_response(response, fn_o)

# 提取向量
vector = response.data[0].embedding

print(f"向量维度: {len(vector)}")
print(f"前 10 个数值: {vector[:10]}")
print(f"消耗 tokens: {response.usage.total_tokens}")

