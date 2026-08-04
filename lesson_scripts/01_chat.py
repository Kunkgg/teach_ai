from openai import OpenAI

# 创建 DeepSeek 客户端 — 只需改 base_url 和 api_key
client = OpenAI(
    api_key="你的-DeepSeek-API-Key",     # ← 替换成你的 key
    base_url="https://api.deepseek.com",
)

# 发送 Chat Completion 请求
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {
            "role": "system",
            "content": "你是一个可信工程助手，帮助开发者理解编码规范和可信构建流程。"
        },
        {
            "role": "user",
            "content": "什么是编码规范检查？用一句话解释。"
        },
    ],
    temperature=0.3,    # 低温度 = 更确定性的回答
    max_tokens=200,     # 限制回复长度
)

# 提取回复内容
answer = response.choices[0].message.content
print(f"模型回复: {answer}")
print(f"消耗 tokens: {response.usage.total_tokens}")
