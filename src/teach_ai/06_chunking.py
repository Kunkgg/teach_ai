# 一份（简化版）可信编码规范文档 —— 4 个主题段落，用空行分隔
TRUST_DOCS = """编码规范检查是可信工程的第一道防线。团队通过 ESLint、Pylint、SonarQube 等静态分析工具自动扫描源代码，识别不符合规范的命名、格式、复杂度等问题。检查结果同步到可信看板，按组件维度聚合，指导开发者逐项修复。

可信构建要求在可控、可追溯的环境中执行软件构建。每次构建的源码版本、依赖清单、构建参数都必须完整记录，确保产物与源码的对应关系可验证。这是防范供应链攻击、保证产物完整性的关键环节。

代码度量通过圈复杂度、代码行数、重复率、注释率等量化指标评估代码质量。可信看板将这些指标按模块可视化，帮助团队识别高风险、需重构的模块。通常圈复杂度超过 15 的函数会被标记为需要关注。

组件化是将复杂系统拆分为高内聚、低耦合的独立组件，每个组件有清晰的接口契约和版本管理。可信看板跟踪各组件的接口稳定性、依赖关系和变更频率，以此评估组件化成熟度。"""


def split_by_paragraph(text):
    """按空行（段落）切分，丢弃空白段落。最自然的切分方式。"""
    return [p.strip() for p in text.split("\n\n") if p.strip()]


chunks = split_by_paragraph(TRUST_DOCS)

print(f"文档总长 {len(TRUST_DOCS)} 字符，切成 {len(chunks)} 个 chunk:\n")
for i, chunk in enumerate(chunks):
    print(f"── chunk {i} ({len(chunk)} 字符) ──")
    print(chunk)
    print()
