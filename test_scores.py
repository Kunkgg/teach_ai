from teach_ai.envs import GLM_KEY
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings(
    model="embedding-3", 
    api_key=GLM_KEY, 
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    check_embedding_ctx_length=False
)

vectorstore = Chroma(
    collection_name="trust_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
docs = vectorstore.similarity_search_with_relevance_scores("什么是编码规范检查？", k=3)
print("Without collection_metadata:")
for doc, score in docs:
    print(f"Score: {score}")

vectorstore_cosine = Chroma(
    collection_name="trust_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
    collection_metadata={"hnsw:space": "cosine"}
)
docs2 = vectorstore_cosine.similarity_search_with_relevance_scores("什么是编码规范检查？", k=3)
print("\nWith collection_metadata:")
for doc, score in docs2:
    print(f"Score: {score}")
