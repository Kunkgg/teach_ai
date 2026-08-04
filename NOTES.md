# Teaching Notes

## User Preferences

- 中英混合教学：技术术语用英文，解释用中文
- 偏好 Learn by doing，不喜欢纯理论学习
- 喜欢 Matt Pocock 的教学风格和 skills 框架
- 希望跳过数学基础部分，直接进入工程实践
- 已经在使用 AI 编程 agent（Claude Code / OpenCode / Antigravity CLI）
- 每天可投入 1-2 小时（工作日），周末 3-4 小时

## Working Notes

- 用户的 Python 水平是中级（OOP、装饰器、生成器、后端 API），这意味着 LangChain/LangGraph 的 Python 语法不会是障碍
- "可信看板"项目是一个工程质量管控系统，包含代码规范检查、度量、构建可信度等维度 — 这和 AI 的结合点非常自然（RAG 查文档 + Agent 分析数据 + LangGraph 编排流程）
- 用户在外包公司工作，意味着他需要的不是科研能力，而是能快速落地的工程能力
- 1 个月 50-60 小时的学习时间是紧凑的，必须极度聚焦，每个 lesson 都要直接服务于最终项目
- Matt Pocock 的 AI Hero 项目值得关注 — 他的方法论（TDD、PRD、task decomposition）和用户当前使用 agent 的方式一致

## API Keys

- 用户只有 **智谱** 和 **DeepSeek** 的 API key
- 教学策略：DeepSeek 做 Chat，智谱做 Embedding
- 两者都是 OpenAI 兼容，用 `openai` 包即可

## Session Log

- **2026-08-03**: 初始化教学工作区。完成 Mission 定义、Resources 收集。
- **2026-08-04**: 用户完成 Lesson 1 四道题，浏览了 roadmap.sh。创建 Lesson 2（LLM API 调用：DeepSeek Chat + 智谱 Embedding + 余弦相似度 + Mini RAG）。
