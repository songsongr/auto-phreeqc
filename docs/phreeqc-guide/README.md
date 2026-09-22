# PHREEQC Version 3 HTML User's Guide

本目录由 [USGS 官方 HTML 手册](https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3.htm) 自动整理生成，抓取日期为 2026-09-22。

## 知识层布局

- source/html/：官方 HTML 原文，作为可追溯源文件。
- parsed/pages/：逐页 Markdown，保留原章节、输入示例和说明。
- parsed/full.md：按官方页序合并的完整 Markdown。
- knowledge/keywords/：按 PHREEQC 关键词组织的可直接检索文档。
- knowledge/concepts/：介绍、计算类型、模型和附录等概念文档。
- knowledge/examples/：示例章节索引；示例正文按来源页保存在 parsed/pages/。
- knowledge/equations/：公式相关章节索引；原始内容保留在对应页。
- knowledge/chunks.jsonl：按章节切分的结构化记录，供 FTS/Embedding 索引使用。
- knowledge/terms.json：关键词到来源页的符号映射。

共整理 110 个页面，生成 774 个章节记录。失败页面记录在 parsed/failures.json。

## 页面索引

| 类别 | 页面 | 原始 HTML | Markdown |
|---|---|---|---|
| keyword | GAS_BINARY_PARAMETERS | [gas_binary_parameters.htm](source/html/gas_binary_parameters.htm) | [打开](parsed/pages/gas_binary_parameters.md) |
| keyword | MEAN_GAMMAS | [mean_gammas.htm](source/html/mean_gammas.htm) | [打开](parsed/pages/mean_gammas.md) |
| concept | Abstract | [phreeqc3-1.htm](source/html/phreeqc3-1.htm) | [打开](parsed/pages/phreeqc3-1.md) |
| keyword | DELETE | [phreeqc3-10.htm](source/html/phreeqc3-10.htm) | [打开](parsed/pages/phreeqc3-10.md) |
| keyword | SOLID_SOLUTIONS_RAW | [phreeqc3-100.htm](source/html/phreeqc3-100.htm) | [打开](parsed/pages/phreeqc3-100.md) |
| keyword | SOLUTION_MODIFY | [phreeqc3-101.htm](source/html/phreeqc3-101.htm) | [打开](parsed/pages/phreeqc3-101.md) |
| keyword | SOLUTION_RAW | [phreeqc3-102.htm](source/html/phreeqc3-102.htm) | [打开](parsed/pages/phreeqc3-102.md) |
| keyword | SURFACE_MODIFY | [phreeqc3-103.htm](source/html/phreeqc3-103.htm) | [打开](parsed/pages/phreeqc3-103.md) |
| keyword | SURFACE_RAW | [phreeqc3-104.htm](source/html/phreeqc3-104.htm) | [打开](parsed/pages/phreeqc3-104.md) |
| keyword | DUMP | [phreeqc3-11.htm](source/html/phreeqc3-11.htm) | [打开](parsed/pages/phreeqc3-11.md) |
| keyword | END | [phreeqc3-12.htm](source/html/phreeqc3-12.htm) | [打开](parsed/pages/phreeqc3-12.md) |
| keyword | EQUILIBRIUM_PHASES | [phreeqc3-13.htm](source/html/phreeqc3-13.htm) | [打开](parsed/pages/phreeqc3-13.md) |
| keyword | EXCHANGE | [phreeqc3-14.htm](source/html/phreeqc3-14.htm) | [打开](parsed/pages/phreeqc3-14.md) |
| keyword | EXCHANGE_MASTER_SPECIES | [phreeqc3-15.htm](source/html/phreeqc3-15.htm) | [打开](parsed/pages/phreeqc3-15.md) |
| keyword | EXCHANGE_SPECIES | [phreeqc3-16.htm](source/html/phreeqc3-16.htm) | [打开](parsed/pages/phreeqc3-16.md) |
| keyword | GAS_PHASE | [phreeqc3-17.htm](source/html/phreeqc3-17.htm) | [打开](parsed/pages/phreeqc3-17.md) |
| keyword | INCLUDE$ | [phreeqc3-18.htm](source/html/phreeqc3-18.htm) | [打开](parsed/pages/phreeqc3-18.md) |
| keyword | INCREMENTAL_REACTIONS | [phreeqc3-19.htm](source/html/phreeqc3-19.htm) | [打开](parsed/pages/phreeqc3-19.md) |
| concept | Introduction | [phreeqc3-2.htm](source/html/phreeqc3-2.htm) | [打开](parsed/pages/phreeqc3-2.md) |
| keyword | INVERSE_MODELING | [phreeqc3-20.htm](source/html/phreeqc3-20.htm) | [打开](parsed/pages/phreeqc3-20.md) |
| keyword | ISOTOPES | [phreeqc3-21.htm](source/html/phreeqc3-21.htm) | [打开](parsed/pages/phreeqc3-21.md) |
| keyword | ISOTOPE_ALPHAS | [phreeqc3-22.htm](source/html/phreeqc3-22.htm) | [打开](parsed/pages/phreeqc3-22.md) |
| keyword | ISOTOPE_RATIOS | [phreeqc3-23.htm](source/html/phreeqc3-23.htm) | [打开](parsed/pages/phreeqc3-23.md) |
| keyword | KINETICS | [phreeqc3-24.htm](source/html/phreeqc3-24.htm) | [打开](parsed/pages/phreeqc3-24.md) |
| keyword | KNOBS | [phreeqc3-25.htm](source/html/phreeqc3-25.htm) | [打开](parsed/pages/phreeqc3-25.md) |
| keyword | LLNL_AQUEOUS_MODEL_PARAMETERS | [phreeqc3-26.htm](source/html/phreeqc3-26.htm) | [打开](parsed/pages/phreeqc3-26.md) |
| keyword | MIX | [phreeqc3-27.htm](source/html/phreeqc3-27.htm) | [打开](parsed/pages/phreeqc3-27.md) |
| keyword | MIX_EQUILIBRIUM_PHASES | [phreeqc3-28.htm](source/html/phreeqc3-28.htm) | [打开](parsed/pages/phreeqc3-28.md) |
| keyword | MIX_EXCHANGE | [phreeqc3-29.htm](source/html/phreeqc3-29.htm) | [打开](parsed/pages/phreeqc3-29.md) |
| concept | Versions of PHREEQC | [phreeqc3-3.htm](source/html/phreeqc3-3.htm) | [打开](parsed/pages/phreeqc3-3.md) |
| keyword | MIX_GAS_PHASE | [phreeqc3-30.htm](source/html/phreeqc3-30.htm) | [打开](parsed/pages/phreeqc3-30.md) |
| keyword | MIX_KINETICS | [phreeqc3-31.htm](source/html/phreeqc3-31.htm) | [打开](parsed/pages/phreeqc3-31.md) |
| keyword | MIX_SOLID_SOLUTION | [phreeqc3-32.htm](source/html/phreeqc3-32.htm) | [打开](parsed/pages/phreeqc3-32.md) |
| keyword | MIX_SOLUTION | [phreeqc3-33.htm](source/html/phreeqc3-33.htm) | [打开](parsed/pages/phreeqc3-33.md) |
| keyword | MIX_SURFACE | [phreeqc3-34.htm](source/html/phreeqc3-34.htm) | [打开](parsed/pages/phreeqc3-34.md) |
| keyword | NAMED_EXPRESSIONS | [phreeqc3-35.htm](source/html/phreeqc3-35.htm) | [打开](parsed/pages/phreeqc3-35.md) |
| keyword | PHASES | [phreeqc3-36.htm](source/html/phreeqc3-36.htm) | [打开](parsed/pages/phreeqc3-36.md) |
| keyword | PITZER | [phreeqc3-37.htm](source/html/phreeqc3-37.htm) | [打开](parsed/pages/phreeqc3-37.md) |
| keyword | PRINT | [phreeqc3-38.htm](source/html/phreeqc3-38.htm) | [打开](parsed/pages/phreeqc3-38.md) |
| keyword | RATES | [phreeqc3-39.htm](source/html/phreeqc3-39.htm) | [打开](parsed/pages/phreeqc3-39.md) |
| concept | Types and Sequence of Calculations | [phreeqc3-4.htm](source/html/phreeqc3-4.htm) | [打开](parsed/pages/phreeqc3-4.md) |
| keyword | REACTION | [phreeqc3-40.htm](source/html/phreeqc3-40.htm) | [打开](parsed/pages/phreeqc3-40.md) |
| keyword | REACTION_PRESSURE | [phreeqc3-41.htm](source/html/phreeqc3-41.htm) | [打开](parsed/pages/phreeqc3-41.md) |
| keyword | REACTION_TEMPERATURE | [phreeqc3-42.htm](source/html/phreeqc3-42.htm) | [打开](parsed/pages/phreeqc3-42.md) |
| keyword | RUN_CELLS | [phreeqc3-43.htm](source/html/phreeqc3-43.htm) | [打开](parsed/pages/phreeqc3-43.md) |
| keyword | SAVE | [phreeqc3-44.htm](source/html/phreeqc3-44.htm) | [打开](parsed/pages/phreeqc3-44.md) |
| keyword | SELECTED_OUTPUT | [phreeqc3-45.htm](source/html/phreeqc3-45.htm) | [打开](parsed/pages/phreeqc3-45.md) |
| keyword | SIT | [phreeqc3-46.htm](source/html/phreeqc3-46.htm) | [打开](parsed/pages/phreeqc3-46.md) |
| keyword | SOLID_SOLUTIONS | [phreeqc3-47.htm](source/html/phreeqc3-47.htm) | [打开](parsed/pages/phreeqc3-47.md) |
| keyword | SOLUTION | [phreeqc3-48.htm](source/html/phreeqc3-48.htm) | [打开](parsed/pages/phreeqc3-48.md) |
| keyword | SOLUTION_MASTER_SPECIES | [phreeqc3-49.htm](source/html/phreeqc3-49.htm) | [打开](parsed/pages/phreeqc3-49.md) |
| concept | Description of Data Input | [phreeqc3-5.htm](source/html/phreeqc3-5.htm) | [打开](parsed/pages/phreeqc3-5.md) |
| keyword | SOLUTION_SPECIES | [phreeqc3-50.htm](source/html/phreeqc3-50.htm) | [打开](parsed/pages/phreeqc3-50.md) |
| keyword | SOLUTION_SPREAD | [phreeqc3-51.htm](source/html/phreeqc3-51.htm) | [打开](parsed/pages/phreeqc3-51.md) |
| keyword | SURFACE | [phreeqc3-52.htm](source/html/phreeqc3-52.htm) | [打开](parsed/pages/phreeqc3-52.md) |
| keyword | SURFACE_MASTER_SPECIES | [phreeqc3-53.htm](source/html/phreeqc3-53.htm) | [打开](parsed/pages/phreeqc3-53.md) |
| keyword | SURFACE_SPECIES | [phreeqc3-54.htm](source/html/phreeqc3-54.htm) | [打开](parsed/pages/phreeqc3-54.md) |
| keyword | TITLE | [phreeqc3-55.htm](source/html/phreeqc3-55.htm) | [打开](parsed/pages/phreeqc3-55.md) |
| keyword | TRANSPORT | [phreeqc3-56.htm](source/html/phreeqc3-56.htm) | [打开](parsed/pages/phreeqc3-56.md) |
| keyword | USE | [phreeqc3-57.htm](source/html/phreeqc3-57.htm) | [打开](parsed/pages/phreeqc3-57.md) |
| keyword | USER_GRAPH | [phreeqc3-58.htm](source/html/phreeqc3-58.htm) | [打开](parsed/pages/phreeqc3-58.md) |
| keyword | USER_PRINT | [phreeqc3-59.htm](source/html/phreeqc3-59.htm) | [打开](parsed/pages/phreeqc3-59.md) |
| keyword | ADVECTION | [phreeqc3-6.htm](source/html/phreeqc3-6.htm) | [打开](parsed/pages/phreeqc3-6.md) |
| keyword | USER_PUNCH | [phreeqc3-60.htm](source/html/phreeqc3-60.htm) | [打开](parsed/pages/phreeqc3-60.md) |
| concept | The Basic Interpreter | [phreeqc3-61.htm](source/html/phreeqc3-61.htm) | [打开](parsed/pages/phreeqc3-61.md) |
| navigation | Examples | [phreeqc3-62.htm](source/html/phreeqc3-62.htm) | [打开](parsed/pages/phreeqc3-62.md) |
| example | Example 1--Speciation Calculation | [phreeqc3-63.htm](source/html/phreeqc3-63.htm) | [打开](parsed/pages/phreeqc3-63.md) |
| example | Example 2--Equilibration With Pure Phases | [phreeqc3-64.htm](source/html/phreeqc3-64.htm) | [打开](parsed/pages/phreeqc3-64.md) |
| example | Example 3--Mixing | [phreeqc3-65.htm](source/html/phreeqc3-65.htm) | [打开](parsed/pages/phreeqc3-65.md) |
| example | Example 4--Evaporation and Homogeneous Redox Reactions | [phreeqc3-66.htm](source/html/phreeqc3-66.htm) | [打开](parsed/pages/phreeqc3-66.md) |
| example | Example 5--Irreversible Reactions | [phreeqc3-67.htm](source/html/phreeqc3-67.htm) | [打开](parsed/pages/phreeqc3-67.md) |
| example | Example 6--Reaction-Path Calculations | [phreeqc3-68.htm](source/html/phreeqc3-68.htm) | [打开](parsed/pages/phreeqc3-68.md) |
| example | Example 7--Gas-Phase Calculations | [phreeqc3-69.htm](source/html/phreeqc3-69.htm) | [打开](parsed/pages/phreeqc3-69.md) |
| keyword | CALCULATE_VALUES | [phreeqc3-7.htm](source/html/phreeqc3-7.htm) | [打开](parsed/pages/phreeqc3-7.md) |
| example | Example 8--Surface Complexation | [phreeqc3-70.htm](source/html/phreeqc3-70.htm) | [打开](parsed/pages/phreeqc3-70.md) |
| example | Example 9--Kinetic Oxidation of Dissolved Ferrous Iron With Oxygen | [phreeqc3-71.htm](source/html/phreeqc3-71.htm) | [打开](parsed/pages/phreeqc3-71.md) |
| example | Example 10--Aragonite-Strontianite Solid Solution | [phreeqc3-72.htm](source/html/phreeqc3-72.htm) | [打开](parsed/pages/phreeqc3-72.md) |
| example | Example 11--Transport and Cation Exchange | [phreeqc3-73.htm](source/html/phreeqc3-73.htm) | [打开](parsed/pages/phreeqc3-73.md) |
| example | Example 12--Advective and Diffusive Flux of Heat and Solutes | [phreeqc3-74.htm](source/html/phreeqc3-74.htm) | [打开](parsed/pages/phreeqc3-74.md) |
| example | Example 13--1D Transport in a Dual Porosity Column With Cation Exchange | [phreeqc3-75.htm](source/html/phreeqc3-75.htm) | [打开](parsed/pages/phreeqc3-75.md) |
| example | Example 14--Advective Transport, Cation Exchange, Surface Complexation, and Mineral Equilibria | [phreeqc3-76.htm](source/html/phreeqc3-76.htm) | [打开](parsed/pages/phreeqc3-76.md) |
| example | Example 15--1D Transport: Kinetic Biodegradation, Cell Growth, and Sorption | [phreeqc3-77.htm](source/html/phreeqc3-77.htm) | [打开](parsed/pages/phreeqc3-77.md) |
| example | Example 16--Inverse Modeling of Sierra Spring Waters | [phreeqc3-78.htm](source/html/phreeqc3-78.htm) | [打开](parsed/pages/phreeqc3-78.md) |
| example | Example 17--Inverse Modeling With Evaporation | [phreeqc3-79.htm](source/html/phreeqc3-79.htm) | [打开](parsed/pages/phreeqc3-79.md) |
| keyword | COPY | [phreeqc3-8.htm](source/html/phreeqc3-8.htm) | [打开](parsed/pages/phreeqc3-8.md) |
| example | Example 18--Inverse Modeling of the Madison Aquifer | [phreeqc3-80.htm](source/html/phreeqc3-80.htm) | [打开](parsed/pages/phreeqc3-80.md) |
| example | Example 19--Modeling Cd+2 Sorption With Linear, Freundlich, and Langmuir Isotherms, and With a Deterministic Distribution of Sorption Sites for Organic Matter, Clay Minerals, and Iron Oxyhydroxides | [phreeqc3-81.htm](source/html/phreeqc3-81.htm) | [打开](parsed/pages/phreeqc3-81.md) |
| example | Example 20--Distribution of Isotopes Between Water and Calcite | [phreeqc3-82.htm](source/html/phreeqc3-82.htm) | [打开](parsed/pages/phreeqc3-82.md) |
| example | Example 21--Modeling Diffusion of HTO, 36Cl-, 22Na+, and Cs+ in a Radial Diffusion Cell | [phreeqc3-83.htm](source/html/phreeqc3-83.htm) | [打开](parsed/pages/phreeqc3-83.md) |
| example | Example 22--Modeling Gas Solubilities: CO2 at High Pressures | [phreeqc3-84.htm](source/html/phreeqc3-84.htm) | [打开](parsed/pages/phreeqc3-84.md) |
| concept | References Cited | [phreeqc3-85.htm](source/html/phreeqc3-85.htm) | [打开](parsed/pages/phreeqc3-85.md) |
| concept | Appendix A. Keyword Data Blocks for Programmers | [phreeqc3-86.htm](source/html/phreeqc3-86.htm) | [打开](parsed/pages/phreeqc3-86.md) |
| keyword | EQUILIBRIUM_PHASES_MODIFY | [phreeqc3-87.htm](source/html/phreeqc3-87.htm) | [打开](parsed/pages/phreeqc3-87.md) |
| keyword | EQUILIBRIUM_PHASES_RAW | [phreeqc3-88.htm](source/html/phreeqc3-88.htm) | [打开](parsed/pages/phreeqc3-88.md) |
| keyword | EXCHANGE_MODIFY | [phreeqc3-89.htm](source/html/phreeqc3-89.htm) | [打开](parsed/pages/phreeqc3-89.md) |
| keyword | DATABASE | [phreeqc3-9.htm](source/html/phreeqc3-9.htm) | [打开](parsed/pages/phreeqc3-9.md) |
| keyword | EXCHANGE_RAW | [phreeqc3-90.htm](source/html/phreeqc3-90.htm) | [打开](parsed/pages/phreeqc3-90.md) |
| keyword | GAS_PHASE_MODIFY | [phreeqc3-91.htm](source/html/phreeqc3-91.htm) | [打开](parsed/pages/phreeqc3-91.md) |
| keyword | GAS_PHASE_RAW | [phreeqc3-92.htm](source/html/phreeqc3-92.htm) | [打开](parsed/pages/phreeqc3-92.md) |
| keyword | KINETICS_MODIFY | [phreeqc3-93.htm](source/html/phreeqc3-93.htm) | [打开](parsed/pages/phreeqc3-93.md) |
| keyword | KINETICS_RAW | [phreeqc3-94.htm](source/html/phreeqc3-94.htm) | [打开](parsed/pages/phreeqc3-94.md) |
| keyword | REACTION_MODIFY | [phreeqc3-95.htm](source/html/phreeqc3-95.htm) | [打开](parsed/pages/phreeqc3-95.md) |
| keyword | REACTION_RAW | [phreeqc3-96.htm](source/html/phreeqc3-96.htm) | [打开](parsed/pages/phreeqc3-96.md) |
| keyword | REACTION_PRESSURE_RAW | [phreeqc3-97.htm](source/html/phreeqc3-97.htm) | [打开](parsed/pages/phreeqc3-97.md) |
| keyword | REACTION_TEMPERATURE_RAW | [phreeqc3-98.htm](source/html/phreeqc3-98.htm) | [打开](parsed/pages/phreeqc3-98.md) |
| keyword | SOLID_SOLUTIONS_MODIFY | [phreeqc3-99.htm](source/html/phreeqc3-99.htm) | [打开](parsed/pages/phreeqc3-99.md) |
| navigation | PHREEQC3 HTML | [phreeqc3.htm](source/html/phreeqc3.htm) | [打开](parsed/pages/phreeqc3.md) |
| keyword | RATE_PARAMETERS_HERMANSKA | [rate-parameters_hermanska.htm](source/html/rate-parameters_hermanska.htm) | [打开](parsed/pages/rate-parameters_hermanska.md) |
| keyword | RATE_PARAMETERS_PK | [rate-parameters_pk.htm](source/html/rate-parameters_pk.htm) | [打开](parsed/pages/rate-parameters_pk.md) |
| keyword | RATE_PARAMETERS_SVD | [rate-parameters_svd.htm](source/html/rate-parameters_svd.htm) | [打开](parsed/pages/rate-parameters_svd.md) |
