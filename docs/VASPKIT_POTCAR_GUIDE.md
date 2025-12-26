
# 使用 vaspkit 生成 POTCAR 文件 - 手动指南

## 前提条件

1. **配置 vaspkit 环境变量**
   ```bash
   # 如果还没有配置，复制配置文件模板
   cp /path/to/vaspkit/how_to_set_environment_variable ~/.vaspkit
   
   # 编辑配置文件
   vi ~/.vaspkit
   ```
   
   在 `~/.vaspkit` 中设置:
   ```
   PBE_PATH       /path/to/potpaw_PBE    # 您的 PBE 赝势库路径
   POTCAR_TYPE    PBE                    # 赝势类型
   RECOMMENDED_POTCAR  .TRUE.            # 使用推荐赝势
   ```

## 步骤 1: 准备 POSCAR 文件

vaspkit 需要一个 POSCAR 文件来生成 POTCAR。

已创建临时 POSCAR 文件在: data/temp_vaspkit/POSCAR

## 步骤 2: 运行 vaspkit

```bash
cd data/temp_vaspkit
vaspkit
```

## 步骤 3: 选择功能（vaspkit 0.71+ 版本）

在 vaspkit 主菜单中:
1. 输入 **1** 选择 `VASP Input Files Generator`
2. 然后选择:
   - **103** - 自动生成 POTCAR（推荐，使用推荐赝势）
   - **104** - 手动选择每个元素的赝势类型

## 步骤 4: 自动生成（功能 103）

如果选择 103:
- vaspkit 会自动读取 POSCAR 中的元素: Fe Si B
- 自动选择推荐的赝势版本
- 自动生成 POTCAR 文件

## 步骤 5: 手动选择（功能 104）

如果选择 104，需要为每个元素选择赝势版本:

按照提示依次输入:
- **Fe**: 输入 `Fe_pv`（推荐，包含 p 价电子，适合金属）
- **Si**: 输入 `Si`（标准版本）
- **B**: 输入 `B`（标准版本）

**注意**: 如果输入的赝势类型不存在，vaspkit 会提示重新输入。

## 步骤 6: 复制 POTCAR

生成后，复制到目标位置:

```bash
cp POTCAR outputs/melt_quench_simulation/POTCAR
```

## 验证

```bash
# 检查元素数量
grep -c "TITEL" outputs/melt_quench_simulation/POTCAR
# 应该输出: 3

# 检查元素顺序（必须与 POSCAR 匹配！）
grep "TITEL" outputs/melt_quench_simulation/POTCAR
# 应该显示:
# TITEL  = PAW Fe ...
# TITEL  = PAW Si ...
# TITEL  = PAW B ...

# 检查 ENCUT 推荐值
grep "ENMAX" outputs/melt_quench_simulation/POTCAR
```

## 赝势版本选择建议

| 元素 | 推荐版本 | 说明 |
|------|---------|------|
| **Fe** | `Fe_pv` | 包含 p 价电子，适合金属体系 |
| **Si** | `Si` | 标准版本，通常足够 |
| **B** | `B` | 标准版本，通常足够 |

## 常见问题

### Q: vaspkit 找不到赝势库

**A**: 检查 `~/.vaspkit` 文件中的 `PBE_PATH` 设置是否正确。

### Q: 元素顺序错误

**A**: vaspkit 会自动按照 POSCAR 中的元素顺序生成 POTCAR，确保 POSCAR 第 6 行是: Fe Si B

### Q: 生成的 POTCAR 缺少元素

**A**: 检查 POSCAR 文件格式，确保所有元素都在赝势库中存在。
