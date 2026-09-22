# Agent 检索策略

1. 先读取 manifest.json，确认知识库版本和来源。
2. PHREEQC 关键词、-identifier 或中文术语优先查 symbols 表。
3. 自然语言解释使用 chunks_fts，按 type 过滤并优先返回 keyword、explanation、note。
4. 需要完整上下文时，根据 doc_id、parent_id 和 section_path 扩展到同一页面。
5. 需要可执行输入时只返回 type=phreeqc_input 且 input 非空的块。
6. 表格优先查 tables 表或 tables.jsonl；反应式、计算式优先查 equations 表或 equations.jsonl。
7. 示例选择优先查 examples.jsonl 的 simulation_types，再取对应 example 页的输入块。
8. 最终回答必须携带 source_url；不要把 full.md 作为默认上下文。

推荐查询顺序：symbol lookup → query_phreeqc_guide.py → small-to-big context expansion → 原始 HTML 核验。
