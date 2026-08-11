import numpy as np
from teach_ai.envs import GLM_KEY
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

zhipu = OpenAI(api_key=GLM_KEY, base_url="https://open.bigmodel.cn/api/paas/v4/")
text = "什么是编码规范检查？"
resp = zhipu.embeddings.create(model="embedding-3", input=[text])
vec1 = resp.data[0].embedding

embeddings = OpenAIEmbeddings(
    model="embedding-3", 
    api_key=GLM_KEY, 
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    check_embedding_ctx_length=False
)
vec2 = embeddings.embed_query(text)

print(f"Vec1 == Vec2: {np.allclose(vec1, vec2)}")
print(f"Dot product: {np.dot(vec1, vec2)}")
