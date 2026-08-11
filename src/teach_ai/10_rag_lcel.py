"""Lesson 0006 — LCEL 重写 RAG（填空版）。

填两处空白（标 ② 和 ④），跑通后应该能像 Lesson 4 那样回答问题，且对域外问题能触发相似度拦截。

运行（项目根目录）：
    uv run python src/teach_ai/10_rag_lcel.py
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from teach_ai.envs import DS_KEY, GLM_KEY

# ── 1. 准备基础积木（和手写版一致，只是换成了 LangChain 的现成组件） ──

embeddings = OpenAIEmbeddings(
    model="embedding-3",
    api_key=GLM_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    check_embedding_ctx_length=False  # 防止 LangChain 用 OpenAI 的 tiktoken 预分词导致智谱识别成乱码
)
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=DS_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.2,
)

# 连上上一周已经建好的 ChromaDB 数据库（数据还在！）
vectorstore = Chroma(
    collection_name="trust_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是可信工程助手。仅基于参考文档回答，不要编造。如果文档中没有相关信息，请明确说明。",
        ),
        ("user", "参考文档:\n{context}\n\n问题: {question}"),
    ]
)
parser = StrOutputParser()

# ── 2. 核心：用 LCEL 替代手写的 retrieve 和 ask ──

# TODO(②): 把 vectorstore 变成 retriever，并加上相似度门控（相当于手写版的 SIM_THRESHOLD = 0.5）。
#   提示：调用 vectorstore.as_retriever(...)
#   参数 1：search_type="similarity_score_threshold"
#   参数 2：search_kwargs={"score_threshold": 0.5, "k": 3}
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.5, "k": 3},
)


def format_docs(docs):
    # 如果 retriever 因为低于阈值而没找到文档，docs 会是空列表，这里就返回空字符串 ""
    return "\n\n".join(doc.page_content for doc in docs)


# 把输入（一个查询字符串）分成两条路：
# "context" 走检索分支：查询词 -> retriever找文档 -> format_docs拼成文本
# "question" 走透传分支：RunnablePassthrough() 把查询词原样传递
setup_and_retrieval = {
    "context": retriever | format_docs,
    "question": RunnablePassthrough(),
}

# TODO(④): 用管道符 | 串联出完整的 RAG 链。
#   顺序：数据准备(setup_and_retrieval) → 模板(prompt) → 模型(llm) → 解析器(parser)
chain = setup_and_retrieval | prompt | llm | parser

# ── 3. 运行测试 ──
if __name__ == "__main__":
    print("测试 1（域内问题）：")
    ans1 = chain.invoke("什么是编码规范检查？")
    print(f"答：{ans1}")

    print("\n" + "=" * 40 + "\n")

    print("测试 2（域外问题，测试阈值拦截）：")
    # 注：因为设置了 threshold，retriever 会返回空列表，传给大模型的 context 是空的。
    # 配合 Prompt 里的系统指令，大模型会乖乖说不知道。
    ans2 = chain.invoke("李明的孩子叫什么？")
    print(f"答：{ans2}")
