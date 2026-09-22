# PHREEQC 知识层

本目录面向后续 Agent 检索，原始来源与逐页解析结果见上级目录。

- chunks.jsonl：章节级 JSONL 记录，字段包括 type、keyword、content 和 source_url。
- terms.json：关键词到来源页的符号映射。
- symbols.json：关键词、-identifier 和中文别名的精确查找表。
- query-lexicon.json：自然语言概念到 PHREEQC 关键词和 identifier 的查询映射。
- index.sqlite：Agent 默认入口，包含 documents、chunks、symbols、relations 和 chunks_fts。
- relations.jsonl：关键词之间的 related_to 关系。
- tables.jsonl：从官方 HTML 表格抽取的行列数据；SQLite 中对应 tables 表。
- equations.jsonl：从章节和输入块抽取的反应式/计算式；SQLite 中对应 equations 表。
- examples.jsonl：示例编号、模拟类型、表格数和可执行输入块数。
- benchmark-latest.json：最近一次检索准确性、覆盖率和延迟评测结果。
- benchmark-advanced-latest.json：复杂查询和答案级覆盖评测结果。
- 高级基准可用 `python doctor/benchmark_advanced_retrieval.py --check` 执行回归门禁。
- manifest.json：知识库版本、统计和来源清单。
- retrieval-policy.md：Agent 检索和上下文扩展规则。
- keywords/：关键词数据块。
- concepts/：概念、计算流程和附录。
- examples/：示例页及示例章节索引。
- equations/：公式章节索引。

Agent 查询入口：python doctor/query_phreeqc_guide.py --symbol SOLUTION；也可使用 --search、--input、--related、--context 和 --examples。

