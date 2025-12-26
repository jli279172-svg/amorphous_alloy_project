# 使用 vaspkit 生成 POTCAR 文件指南

## 概述

vaspkit 是一个强大的 VASP 计算辅助工具，可以自动生成 POTCAR 文件。本指南介绍如何使用 vaspkit 为 Fe80Si10B10 体系生成 POTCAR。

## 前提条件

1. **已安装 vaspkit**
   - 下载: https://github.com/huangwenshi/vaspkit
   - 文档: https://vaspkit.com/

2. **已配置 VASP 赝势库路径**
   - 需要有效的 VASP 许可证
   - 需要本地 VASP 赝势库（potpaw_PBE 等）

## 步骤 1: 安装和配置 vaspkit

### 1.1 下载 vaspkit

```bash
# 从 GitHub 下载
git clone https://github.com/huangwenshi/vaspkit.git
cd vaspkit

# 或下载压缩包
wget https://github.com/huangwenshi/vaspkit/releases/latest/download/vaspkit.x.x.x.tar.gz
tar -zxvf vaspkit.x.x.x.tar.gz
cd vaspkit.x.x.x
```

### 1.2 配置环境变量

```bash
# 复制配置文件模板
cp how_to_set_environment_variable ~/.vaspkit

# 编辑配置文件
nano ~/.vaspkit
# 或
vim ~/.vaspkit
```

### 1.3 设置赝势库路径

在 `~/.vaspkit` 文件中设置：

```bash
# PBE 赝势库路径（根据您的实际路径修改）
PBE_PATH       /path/to/potpaw_PBE

# 赝势类型
POTCAR_TYPE    PBE

# 其他设置（可选）
# LDA_PATH      /path/to/potpaw_LDA
# POTCAR_TYPE   LDA  # 如果使用 LDA
```

**重要**: 将 `/path/to/potpaw_PBE` 替换为您实际的 VASP 赝势库路径。

### 1.4 添加到 PATH（如果需要）

```bash
# 将 vaspkit 添加到 PATH
export PATH=$PATH:/path/to/vaspkit/bin

# 或创建符号链接
ln -s /path/to/vaspkit/vaspkit /usr/local/bin/vaspkit
```

## 步骤 2: 使用 vaspkit 生成 POTCAR

### 方法 A: 交互式方式（推荐）

#### 2.1 配置 vaspkit（首次使用）

```bash
# 复制配置文件模板（如果 vaspkit 已安装）
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

#### 2.2 准备 POSCAR 文件

确保您有 POSCAR 文件（可以使用我们生成的 `outputs/POSCAR_initial`）：

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project
mkdir -p data/temp_vaspkit
cp outputs/POSCAR_initial data/temp_vaspkit/POSCAR
cd data/temp_vaspkit
```

#### 2.3 运行 vaspkit

```bash
vaspkit
```

#### 2.4 选择功能（vaspkit 0.71+ 版本）

**注意**: vaspkit 0.71 以后的版本使用新的菜单结构。

在 vaspkit 主菜单中:
1. 输入 **1** 选择 `VASP Input Files Generator`
2. 然后选择:
   - **103** - 自动生成 POTCAR（推荐，使用 VASP 官方推荐的赝势）
   - **104** - 手动选择每个元素的赝势类型

#### 2.5 按照提示操作

**如果选择 103（自动生成）**:
- vaspkit 会自动读取 POSCAR 中的元素（Fe, Si, B）
- 自动选择 VASP 官方推荐的赝势版本
- 自动从赝势库中提取并连接 POTCAR 文件
- 显示提示信息: `Written POTCAR File with the Recommended Potential!`

**如果选择 104（手动选择）**:
- vaspkit 会提示为每个元素选择赝势版本
- 按照提示依次输入:
  - **Fe**: 输入 `Fe_pv`（推荐，包含 p 价电子，适合金属）
  - **Si**: 输入 `Si`（标准版本）
  - **B**: 输入 `B`（标准版本）
- 如果输入的赝势类型不存在，vaspkit 会提示重新输入

#### 2.6 复制生成的 POTCAR

```bash
# 生成的 POTCAR 在当前目录
cp POTCAR ../../outputs/melt_quench_simulation/POTCAR
```

### 方法 B: 使用我们的辅助脚本

我们提供了一个辅助脚本来简化流程：

```bash
# 检查 vaspkit 安装
python3 scripts/prepare_potcar_vaspkit.py --check-only

# 生成手动指南
python3 scripts/prepare_potcar_vaspkit.py --manual-guide

# 尝试自动生成（如果 vaspkit 支持非交互模式）
python3 scripts/prepare_potcar_vaspkit.py --elements Fe Si B
```

## 步骤 3: 验证 POTCAR 文件

生成后，验证文件：

```bash
cd outputs/melt_quench_simulation

# 1. 检查元素数量
grep -c "TITEL" POTCAR
# 应该输出: 3

# 2. 检查元素顺序（必须与 POSCAR 匹配！）
grep "TITEL" POTCAR
# 应该显示:
# TITEL  = PAW Fe ...
# TITEL  = PAW Si ...
# TITEL  = PAW B ...

# 3. 检查 ENCUT 推荐值
grep "ENMAX" POTCAR
# 记录最大值，确保 INCAR 中的 ENCUT 足够高

# 4. 检查文件大小
ls -lh POTCAR
# 应该 > 100 KB
```

## 使用我们的自动化脚本

### 快速开始

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project

# 1. 检查 vaspkit 和 VASP 赝势库
python3 scripts/prepare_potcar_vaspkit.py --check-only

# 2. 如果检查通过，可以尝试自动生成
python3 scripts/prepare_potcar_vaspkit.py --elements Fe Si B

# 3. 如果自动生成失败，查看手动指南
python3 scripts/prepare_potcar_vaspkit.py --manual-guide
```

## 常见问题

### Q1: vaspkit 找不到命令

**解决方案**:
```bash
# 检查 vaspkit 是否在 PATH 中
which vaspkit

# 如果不在，添加到 PATH
export PATH=$PATH:/path/to/vaspkit/bin

# 或创建符号链接
ln -s /path/to/vaspkit/vaspkit /usr/local/bin/vaspkit
```

### Q2: vaspkit 找不到赝势库

**解决方案**:
1. 检查 `~/.vaspkit` 配置文件
2. 确认 `PBE_PATH` 设置正确
3. 确认路径存在且可访问：
   ```bash
   ls /path/to/potpaw_PBE/Fe/
   ```

### Q3: 元素顺序错误

**解决方案**:
- vaspkit 会自动按照 POSCAR 中的元素顺序生成 POTCAR
- 确保 POSCAR 第 6 行是: `Fe Si B`
- 如果顺序不对，修改 POSCAR 或手动调整

### Q4: 生成的 POTCAR 缺少元素

**解决方案**:
- 检查 POSCAR 文件格式是否正确
- 确认所有元素在赝势库中都存在
- 检查 vaspkit 的输出信息

## vaspkit 其他有用功能

vaspkit 还提供其他有用的功能：

- **功能 1**: 结构分析
- **功能 2**: 生成输入文件
  - **子功能 4**: 生成 POTCAR（我们使用的）
  - **子功能 5**: 生成 KPOINTS
  - **子功能 6**: 生成 INCAR
- **功能 3**: 后处理分析

## 完整工作流程示例

```bash
# 1. 配置 vaspkit（首次使用，只需一次）
cp /path/to/vaspkit/how_to_set_environment_variable ~/.vaspkit
vi ~/.vaspkit  # 设置 PBE_PATH 等

# 2. 进入项目目录
cd /Users/lijunchen/coding/amorphous_alloy_project

# 3. 创建临时目录
mkdir -p data/temp_vaspkit
cd data/temp_vaspkit

# 4. 复制 POSCAR
cp ../../outputs/POSCAR_initial POSCAR

# 5. 运行 vaspkit
vaspkit

# 6. 在菜单中选择:
#    1 -> 103 (自动生成，推荐)
#    或 1 -> 104 (手动选择)

# 7. 如果选择 104，按照提示输入:
#    Fe: Fe_pv
#    Si: Si
#    B: B

# 8. 复制生成的 POTCAR
cp POTCAR ../../outputs/melt_quench_simulation/POTCAR

# 9. 验证
cd ../../outputs/melt_quench_simulation
grep "TITEL" POTCAR
grep -c "TITEL" POTCAR  # 应该输出 3
```

## 与手动方法的对比

| 方法 | 优点 | 缺点 |
|------|------|------|
| **vaspkit** | 自动化、错误少、交互式选择赝势版本 | 需要安装和配置 |
| **手动连接** | 简单直接、完全控制 | 容易出错、需要知道路径 |
| **我们的脚本** | 结合两者优点、提供验证 | 仍需要 vaspkit 或手动文件 |

## 下一步

准备好 POTCAR 文件后：

1. ✅ 验证文件正确性
2. ✅ 检查 INCAR 中的 ENCUT 设置
3. ✅ 运行熔融-淬火模拟：
   ```bash
   cd outputs/melt_quench_simulation
   ./run_all_stages.sh
   ```

## 参考资料

- [vaspkit GitHub](https://github.com/huangwenshi/vaspkit)
- [vaspkit 官方文档](https://vaspkit.com/)
- [vaspkit 安装指南](https://vaspkit.com/installation.html)
- [VASP 官方网站](https://www.vasp.at/)

---

**提示**: 如果 vaspkit 未安装或配置有问题，您也可以使用我们提供的其他方法：
- `scripts/prepare_potcar.py` - 从 VASP 赝势库直接连接
- `scripts/download_potcar.py` - 检查和准备工具

