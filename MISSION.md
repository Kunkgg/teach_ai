# Mission: 从 Python 全栈工程师转型为 AI 工程师

## Who

37 岁的 Python 全栈工程师，在中国软件外包公司从事前后端开发。Python 中级水平（熟悉 OOP、装饰器、生成器，能独立开发后端 API）。已经在使用 Claude Code / OpenCode / Antigravity CLI 等 AI 编程 agent 辅助日常开发工作。

## Why

- **职业转型**：从外包开发转向 AI 工程方向，获得 AI 相关岗位的面试机会
- **技能升级**：系统掌握 RAG、Agent、LangGraph 等企业招聘中高频出现的 AI 工程技术栈
- **项目驱动**：将 AI 能力与当前正在做的"可信看板"项目结合，构建一个可在面试中展示的 AI 项目

## What (Target Skills)

1. **RAG（检索增强生成）**：Document loading → Chunking → Embedding → Vector DB → Retrieval → Generation
2. **LangChain / LCEL**：Prompt templates、Output parsers、Tool calling、Chain composition
3. **LangGraph**：Stateful graphs、Nodes/Edges、Conditional routing、Checkpointing、Human-in-the-loop
4. **AI Agent 模式**：ReAct、Multi-agent orchestration、Tool use
5. **生产化能力**：FastAPI 部署、LangSmith 观测、评估 (Evaluation)

## The Project: AI 增强可信看板

将 AI 能力嵌入到现有的"可信看板"系统中：

**可信看板现有功能：**
- 日常看护：获取各软件组件编码规范检查、代码度量、可信构建和组件化等可信领域的工程扫描数据，可视化结果，指导各组件处理可信问题
- 版本发布检查：启动待发布版本各可信领域工程，获取工程结果，执行自动化白盒测试用例，输出评估报告

**AI 增强方向（待细化）：**
- 用 RAG 让用户能自然语言查询可信规范文档和历史扫描数据
- 用 Agent 自动分析扫描结果，给出智能修复建议
- 用 LangGraph 编排多步骤的版本发布评估流程

## Constraints

- **时间**：1 个月（工作日 1-2 小时，周末 3-4 小时，约 50-60 小时总学习时间）
- **方法**：Learn by doing，每个知识点通过动手项目来掌握
- **语言**：中英混合教学（技术术语用英文，解释用中文）
- **数学**：跳过深度数学推导，聚焦工程实践
- **工具**：充分利用 AI 编程 agent 加速学习和开发

## Timeline

| 周 | 主题 | 产出 |
|---|------|------|
| Week 1 | RAG 基础 + 向量数据库 | 可信文档问答 MVP |
| Week 2 | LangChain/LCEL + Tool Calling | 可信数据分析 Chain |
| Week 3 | LangGraph + Agent 模式 | 可信评估 Agent |
| Week 4 | 系统集成 + 生产化 | 完整 AI 可信看板 Demo |

## Success Criteria

- [ ] 能独立设计和实现一个 RAG pipeline
- [ ] 能用 LangGraph 构建有状态的 AI agent
- [ ] 有一个可展示的"AI 可信看板"项目
- [ ] 能在面试中清晰讲解 RAG / Agent / LangGraph 的核心概念和实现细节
- [ ] 能回答"为什么选择 LangGraph 而不是其他方案"这类设计决策问题
