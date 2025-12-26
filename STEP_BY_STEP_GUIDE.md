# 生成 POTCAR 文件 - 逐步指南

## 当前状态检查

✅ POSCAR 文件已准备: `outputs/POSCAR_initial`

## 方案选择

由于 vaspkit 可能未安装，我们提供两种方案：

### 方案 A: 使用 vaspkit（如果已安装）

### 方案 B: 手动准备 POTCAR（如果有 VASP 赝势库）

---

## 方案 A: 使用 vaspkit

### 步骤 1: 检查 vaspkit 安装

```bash
which vaspkit
# 或
vaspkit -v
```

如果未找到，需要：
1. 下载 vaspkit: https://github.com/huangwenshi/vaspkit
2. 解压并添加到 PATH

### 步骤 2: 配置 vaspkit（首次使用）

```bash
# 如果 vaspkit 已安装，找到配置文件模板
find /path/to/vaspkit -name "how_to_set_environment_variable"

# 复制到用户目录
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

### 步骤 3: 运行 vaspkit

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project
./scripts/run_vaspkit_interactive.sh
```

或手动运行:

```bash
cd data/temp_vaspkit
vaspkit
```

### 步骤 4: 在 vaspkit 中选择

1. 输入 **1** → `VASP Input Files Generator`
2. 输入 **103** → 自动生成 POTCAR（推荐）
   - 或输入 **104** → 手动选择（如果选择 104，输入: Fe_pv, Si, B）

### 步骤 5: 验证和复制

```bash
# 检查生成的 POTCAR
cd data/temp_vaspkit
grep "TITEL" POTCAR
grep -c "TITEL" POTCAR  # 应该输出 3

# 复制到目标位置
cp POTCAR ../../outputs/melt_quench_simulation/POTCAR
```

---

## 方案 B: 手动准备 POTCAR（如果有 VASP 赝势库）

### 步骤 1: 找到 VASP 赝势库路径

```bash
# 常见位置
ls /opt/vasp/potpaw_PBE/
ls /usr/local/vasp/potpaw_PBE/
ls ~/vasp/potpaw_PBE/

# 或设置环境变量
export VASP_PP_PATH=/path/to/potpaw_PBE
```

### 步骤 2: 使用我们的脚本

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project

# 如果知道赝势库路径
python3 scripts/prepare_potcar.py \
    --pp-path /path/to/potpaw_PBE \
    --elements Fe Si B
```

### 步骤 3: 或手动连接

```bash
# 设置路径
export VASP_PP_PATH=/path/to/potpaw_PBE

# 连接 POTCAR 文件（顺序必须与 POSCAR 匹配！）
cat $VASP_PP_PATH/Fe/POTCAR \
    $VASP_PP_PATH/Si/POTCAR \
    $VASP_PP_PATH/B/POTCAR \
    > outputs/melt_quench_simulation/POTCAR
```

### 步骤 4: 验证

```bash
cd outputs/melt_quench_simulation

# 检查元素
grep "TITEL" POTCAR
# 应该显示:
# TITEL  = PAW Fe ...
# TITEL  = PAW Si ...
# TITEL  = PAW B ...

# 检查数量
grep -c "TITEL" POTCAR  # 应该输出 3

# 检查 ENCUT
grep "ENMAX" POTCAR
```

---

## 下一步

准备好 POTCAR 后，可以继续运行熔融-淬火模拟：

```bash
cd outputs/melt_quench_simulation
./run_all_stages.sh
```

---

## 需要帮助？

如果遇到问题，请检查：
1. vaspkit 是否正确安装
2. VASP 赝势库路径是否正确
3. POSCAR 文件格式是否正确
4. 元素顺序是否匹配（Fe Si B）

查看详细文档：
- `docs/VASPKIT_POTCAR_GUIDE_CN.md` - vaspkit 使用指南
- `docs/POTCAR_DOWNLOAD_GUIDE_CN.md` - 手动准备指南

