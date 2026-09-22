# Agent 检索策略

1. 先读取 manifest.json，确认知识库版本和来源。
2. 先用 query-lexicon.json 拆解自然语言，得到 concepts、keywords 和 identifiers。
3. PHREEQC 关键词、-identifier 或中文术语优先查 symbols 表。
4. 简单查询优先精确标题/关键词；复杂查询使用核心概念的混合检索，不要求所有原词同时出现。
5. 自然语言解释使用 chunks_fts，按 type 过滤并优先返回 keyword、phreeqc_input、explanation、note。
6. 需要完整上下文时，根据 doc_id、parent_id 和 section_path 扩展到同一页面。
7. 需要可执行输入时只返回 type=phreeqc_input 且 input 非空的块。
8. 表格优先查 tables 表或 tables.jsonl；反应式、计算式优先查 equations 表或 equations.jsonl。
9. 示例选择优先查 examples.jsonl 的 simulation_types，再取对应 example 页的输入块。
10. 最终回答必须携带 source_url；不要把 full.md 作为默认上下文。

推荐查询顺序：query plan → symbol lookup → hybrid search → input/example filter → small-to-big context expansion → 原始 HTML 核验。
