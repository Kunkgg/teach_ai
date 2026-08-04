# 0002 — DeepSeek + 智谱的 API 组合策略

## Date
2026-08-04

## Context
用户只有智谱和 DeepSeek 的 API key，没有 OpenAI 或 Anthropic 的 key。需要确定教学中使用哪个 API 做什么。

## Insight
**不同厂商的模型可以（而且经常会）混用。** 这不是凑合，而是 AI 工程的正常实践：

1. **DeepSeek** 只提供 Chat 模型（`deepseek-v4-flash`），没有 Embedding API
2. **智谱** 同时提供 Chat（GLM 系列）和 Embedding（`embedding-3`）
3. 最佳组合：**智谱做 Embedding + DeepSeek 做 Chat**
4. 两者都是 OpenAI 兼容的 API，只需 `openai` 一个 Python 包

## Implications
- 后续所有 RAG 课程都用这个组合：智谱 Embedding + DeepSeek Chat
- LangChain 集成时，使用 `ChatOpenAI` 和 `OpenAIEmbeddings` 配合自定义 `base_url`
- 如果将来需要换模型（比如公司提供 OpenAI key），只需改 `base_url` 和 `model` 名

## Status
Active — 决定了整个课程的 API 选型。
