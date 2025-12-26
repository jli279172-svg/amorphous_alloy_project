# POTCAR 文件准备指南

## 概述

POTCAR（赝势）文件是 VASP 计算所必需的。这些文件包含系统中每个元素的赝势。对于 Fe80Si10B10，您需要 Fe、Si 和 B 的 POTCAR 文件。

## 获取 POTCAR 文件

### 方法 1：从 VASP 赝势库获取（推荐）

VASP 提供了赝势库，您需要访问这些库。它们通常位于：
- `/path/to/vasp/pseudopotentials/`（在您的 VASP 安装中）
- 或从 VASP 网站下载（如果您有访问权限）

**步骤：**

1. **定位您的 VASP 赝势目录**
   ```bash
   # 常见位置：
   # - /opt/vasp/potpaw_PBE/
   # - /usr/local/vasp/potpaw_PBE/
   # - $VASP_PP_PATH/potpaw_PBE/
   ```

2. **找到合适的赝势版本**
   - 对于 Fe：查找 `Fe`、`Fe_pv`、`Fe_sv` 等
   - 对于 Si：查找 `Si`、`Si_sv` 等
   - 对于 B：查找 `B`、`B_sv` 等

3. **选择赝势版本：**
   - **Fe**：`Fe` 或 `Fe_pv`（包含 p 价电子）- 推荐用于金属体系
   - **Si**：`Si`（标准）或 `Si_sv`（半芯）
   - **B**：`B`（标准）或 `B_sv`（半芯）

4. **按正确顺序连接 POTCAR 文件：**
   ```bash
   cd /path/to/vasp/potpaw_PBE/
   cat Fe/POTCAR Si/POTCAR B/POTCAR > /path/to/project/outputs/melt_quench_simulation/POTCAR
   ```

### 方法 2：使用辅助脚本

使用提供的辅助脚本来准备 POTCAR：

```bash
python3 scripts/prepare_potcar.py --pp-path /path/to/vasp/potpaw_PBE/ --elements Fe Si B
```

### 方法 3：手动准备

如果您有单独的 POTCAR 文件：

1. **创建临时目录：**
   ```bash
   mkdir -p data/potcars
   ```

2. **复制或下载 POTCAR 文件：**
   - 将 `Fe_POTCAR`、`Si_POTCAR`、`B_POTCAR` 放置在 `data/potcars/` 中

3. **连接它们：**
   ```bash
   cd data/potcars
   cat Fe_POTCAR Si_POTCAR B_POTCAR > ../../outputs/melt_quench_simulation/POTCAR
   ```

## 重要注意事项

### 元素顺序

**关键**：POTCAR 中的元素顺序必须与 POSCAR 中的顺序匹配！

对于 Fe80Si10B10：
- POSCAR 中为：`Fe Si B`（第 6 行）
- POTCAR 必须为：`Fe POTCAR + Si POTCAR + B POTCAR`

### 赝势选择

- **Fe**：对于金属铁，使用 `Fe` 或 `Fe_pv`
- **Si**：通常 `Si`（标准）就足够了
- **B**：通常 `B`（标准）就足够了

对于高精度计算，可考虑：
- `Fe_pv`：包含 p 价电子
- `Si_sv`：半芯版本
- `B_sv`：半芯版本

### 验证

创建 POTCAR 后，请验证：

```bash
# 检查原子数是否匹配
grep "TITEL" POTCAR  # 应显示 3 个元素
head -1 POTCAR       # 应显示 Fe
```

### 常见问题

1. **元素顺序错误**：POTCAR 顺序必须与 POSCAR 匹配
2. **缺少元素**：POSCAR 中的所有元素都必须在 POTCAR 中
3. **版本不匹配**：确保所有 POTCAR 都来自同一库（例如，都是 PBE）
4. **文件格式**：POTCAR 应该是单个连接的文件，而不是单独的文件

## 示例工作流程

```bash
# 1. 找到 VASP 赝势路径
export VASP_PP_PATH=/path/to/vasp/potpaw_PBE

# 2. 验证元素是否存在
ls $VASP_PP_PATH/Fe/
ls $VASP_PP_PATH/Si/
ls $VASP_PP_PATH/B/

# 3. 创建 POTCAR
cat $VASP_PP_PATH/Fe/POTCAR \
    $VASP_PP_PATH/Si/POTCAR \
    $VASP_PP_PATH/B/POTCAR \
    > outputs/melt_quench_simulation/POTCAR

# 4. 验证
head -5 outputs/melt_quench_simulation/POTCAR
grep "TITEL" outputs/melt_quench_simulation/POTCAR
```

## 检查 POTCAR 兼容性

在运行 VASP 之前，请验证：

1. **元素数量与 POSCAR 匹配：**
   ```bash
   # 统计 POSCAR 中的元素（第 6 行）
   head -6 POSCAR | tail -1
   # 应显示：Fe Si B
   
   # 统计 POTCAR 中的元素
   grep -c "TITEL" POTCAR
   # 应显示：3
   ```

2. **ENCUT 兼容性：**
   - 检查 POTCAR 中推荐的 ENCUT：`grep ENMAX POTCAR`
   - 在 INCAR 中使用最大值（或更高）
   - 当前 INCAR 使用 ENCUT = 400 eV

## 使用辅助脚本的详细说明

### 基本用法

```bash
# 使用 VASP 赝势库
python3 scripts/prepare_potcar.py \
    --pp-path /path/to/vasp/potpaw_PBE \
    --elements Fe Si B

# 使用自定义 POTCAR 文件
python3 scripts/prepare_potcar.py \
    --custom-pots /path/to/Fe_POTCAR /path/to/Si_POTCAR /path/to/B_POTCAR \
    --elements Fe Si B

# 指定输出位置
python3 scripts/prepare_potcar.py \
    --pp-path /path/to/vasp/potpaw_PBE \
    --elements Fe Si B \
    --output outputs/melt_quench_simulation/POTCAR
```

### 脚本功能

- **自动查找赝势**：脚本会自动尝试常见的赝势变体（如 `Fe_pv`、`Si_sv` 等）
- **验证输出**：自动检查生成的 POTCAR 文件
- **错误提示**：如果找不到文件，会提供有用的错误信息和建议

## 故障排除

### 问题 1：找不到 POTCAR 文件

**症状**：脚本报告找不到某个元素的 POTCAR

**解决方案**：
1. 检查 VASP 赝势路径是否正确
2. 检查元素目录是否存在
3. 尝试手动指定不同的赝势变体（如 `Fe_pv` 而不是 `Fe`）

### 问题 2：元素顺序错误

**症状**：VASP 报错元素不匹配

**解决方案**：
1. 确保 POTCAR 中的元素顺序与 POSCAR 第 6 行完全一致
2. 使用 `grep "TITEL" POTCAR` 检查顺序
3. 使用 `head -6 POSCAR | tail -1` 检查 POSCAR 顺序

### 问题 3：ENCUT 警告

**症状**：VASP 警告 ENCUT 太低

**解决方案**：
1. 检查 POTCAR 中的 ENMAX 值：`grep ENMAX POTCAR`
2. 在 INCAR 中将 ENCUT 设置为所有 ENMAX 值中的最大值（或更高）
3. 建议使用最大值 × 1.3 作为安全余量

## 参考资料

- VASP 手册：赝势部分
- VASP Wiki：POTCAR 准备
- 您的 VASP 安装文档

## 快速检查清单

在运行 VASP 计算之前，请确认：

- [ ] POTCAR 文件已创建
- [ ] 元素顺序与 POSCAR 匹配
- [ ] 所有元素都存在（使用 `grep "TITEL" POTCAR` 检查）
- [ ] ENCUT 值足够高（检查 `grep ENMAX POTCAR`）
- [ ] POTCAR 文件格式正确（单个连接的文件）
- [ ] 所有 POTCAR 来自同一库（例如，都是 PBE）

完成这些检查后，您就可以开始运行 VASP 计算了！

