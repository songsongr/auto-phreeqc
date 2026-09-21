# 常用输入与输出模式

本参考只说明公开运行库生成或检查输入时最常见的结构。具体热力学参数和物种名称以所选数据库为准。

## 单一溶液

```phreeqc
SOLUTION 1
    units mmol/kgw
    temp 25
    pH 7 charge
    pe 4
    Ca 1
    C(4) 2
END
```

在给定元素浓度时要同时记录单位。`pH 7 charge` 表示以 pH 调整电荷平衡；只有在这一假设符合问题时才使用它。

## 平衡相

```phreeqc
EQUILIBRIUM_PHASES 1
    Calcite 0 10
```

每一行依次为相名、目标饱和指数和可反应量。相名必须存在于数据库中。将相加入模型前，要确认它代表允许沉淀、允许溶解，还是两者都允许的边界条件。

## SELECTED_OUTPUT

```phreeqc
SELECTED_OUTPUT 1
    -file selected_output.txt
    -pH true
    -pe true
    -totals Ca C(4)
    -si Calcite
```

`SELECTED_OUTPUT` 用于生成便于解析的表格。只请求能回答当前问题的字段；参数扫描和运移计算还应加入步骤或距离相关的列，以便绘制趋势。

## 检查清单

运行前确认：

1. 数据库路径和相名、元素名称一致。
2. 浓度单位与输入数值一致。
3. pH、pe、温度及电荷平衡假设已说明。
4. 反应、动力学或运移的步长、总时长和单元数已明确。
5. 输出同时保留原始 `.qpo` 与可解析的 SELECTED_OUTPUT 表格。
