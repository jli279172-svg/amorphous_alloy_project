# POTCAR 文件下载指南（中文版）

## ⚠️ 重要说明

POTCAR 文件是 VASP 的专有资源，**需要有效的 VASP 许可证**才能合法获取和使用。本指南提供合法的获取方法。

## 方法 1: 从 VASP 官方网站下载（推荐）

### 步骤 1: 登录 VASP 门户

1. 访问 [VASP 官方网站](https://www.vasp.at/)
2. 在页面右侧找到 "Portal" 部分
3. 使用您的 VASP 许可证用户名和密码登录

### 步骤 2: 下载赝势库

1. 登录后，导航至 **"Potentials"** 部分
2. 您将看到不同版本的赝势文件：
   - `potpaw_PBE` - PBE 泛函版本（推荐用于大多数计算）
   - `potpaw_PBE.54` - PBE 版本 5.4
   - `potpaw_LDA` - LDA 泛函版本
3. 点击相应的 **"Licensed"** 按钮下载
4. 文件通常是 `.tgz` 或 `.tar.gz` 格式

### 步骤 3: 解压缩赝势库

```bash
# 解压缩下载的文件（以 potpaw_PBE.tgz 为例）
tar -xvzf potpaw_PBE.tgz

# 解压后会得到一个目录，例如：
# potpaw_PBE/
#   ├── Fe/
#   │   └── POTCAR
#   ├── Si/
#   │   └── POTCAR
#   ├── B/
#   │   └── POTCAR
#   └── ...
```

### 步骤 4: 使用脚本准备 POTCAR

```bash
# 使用我们提供的脚本
cd /Users/lijunchen/coding/amorphous_alloy_project

# 指定解压后的赝势库路径
python3 scripts/prepare_potcar.py \
    --pp-path /path/to/potpaw_PBE \
    --elements Fe Si B
```

## 方法 2: 从机构计算中心获取

如果您在学术机构或研究单位：

1. **联系计算中心**：询问是否有共享的 VASP 赝势库
2. **常见位置**：
   - `/shared/vasp/potpaw_PBE/`
   - `/opt/vasp/potpaw_PBE/`
   - `/usr/local/vasp/potpaw_PBE/`
3. **使用脚本检查**：
   ```bash
   python3 scripts/download_potcar.py --check-vasp
   ```

## 方法 3: 手动准备 POTCAR 文件

如果您已经有单个元素的 POTCAR 文件：

### 步骤 1: 创建目录结构

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project
mkdir -p data/potcars/{Fe,Si,B}
```

### 步骤 2: 放置 POTCAR 文件

将各个元素的 POTCAR 文件放置到对应目录：

```bash
# 假设您有这些文件
cp /path/to/Fe_POTCAR data/potcars/Fe/POTCAR
cp /path/to/Si_POTCAR data/potcars/Si/POTCAR
cp /path/to/B_POTCAR data/potcars/B/POTCAR
```

### 步骤 3: 使用脚本连接

```bash
python3 scripts/prepare_potcar.py \
    --pp-path data/potcars \
    --elements Fe Si B
```

## 方法 4: 使用命令行手动连接

如果您知道赝势库的路径：

```bash
# 设置赝势库路径
export VASP_PP_PATH=/path/to/potpaw_PBE

# 验证文件存在
ls $VASP_PP_PATH/Fe/POTCAR
ls $VASP_PP_PATH/Si/POTCAR
ls $VASP_PP_PATH/B/POTCAR

# 连接 POTCAR 文件（顺序必须与 POSCAR 匹配！）
cat $VASP_PP_PATH/Fe/POTCAR \
    $VASP_PP_PATH/Si/POTCAR \
    $VASP_PP_PATH/B/POTCAR \
    > outputs/melt_quench_simulation/POTCAR

# 验证
grep "TITEL" outputs/melt_quench_simulation/POTCAR
# 应该显示 3 行，分别对应 Fe, Si, B
```

## 赝势版本选择建议

### 对于 Fe80Si10B10 体系：

| 元素 | 推荐版本 | 说明 |
|------|---------|------|
| **Fe** | `Fe` 或 `Fe_pv` | `Fe_pv` 包含 p 价电子，对金属体系更准确 |
| **Si** | `Si` | 标准版本通常足够 |
| **B** | `B` | 标准版本通常足够 |

### 高精度选项（如果需要）：

- `Fe_pv`: 包含 p 价电子的铁赝势
- `Si_sv`: 半芯硅赝势
- `B_sv`: 半芯硼赝势

## 验证 POTCAR 文件

准备完成后，请验证：

```bash
# 1. 检查元素数量
grep -c "TITEL" outputs/melt_quench_simulation/POTCAR
# 应该输出: 3

# 2. 检查元素顺序（必须与 POSCAR 匹配！）
grep "TITEL" outputs/melt_quench_simulation/POTCAR
# 应该显示:
# TITEL  = PAW Fe ...
# TITEL  = PAW Si ...
# TITEL  = PAW B ...

# 3. 检查 ENCUT 推荐值
grep "ENMAX" outputs/melt_quench_simulation/POTCAR
# 记录最大值，确保 INCAR 中的 ENCUT 足够高

# 4. 检查文件大小（应该 > 100 KB）
ls -lh outputs/melt_quench_simulation/POTCAR
```

## 常见问题

### Q1: 我没有 VASP 许可证怎么办？

**A**: POTCAR 文件是 VASP 的专有资源，必须通过合法途径获取：
- 购买 VASP 许可证
- 通过所在机构获取（如果机构有许可证）
- 联系 VASP 供应商

### Q2: 可以使用其他来源的赝势吗？

**A**: 理论上可以，但需要注意：
- 不同来源的赝势可能不兼容
- 计算结果可能不一致
- 建议使用 VASP 官方赝势库

### Q3: 元素顺序错误会怎样？

**A**: VASP 会报错并停止计算。**必须确保 POTCAR 中的元素顺序与 POSCAR 第 6 行完全一致**。

### Q4: 如何检查 ENCUT 是否足够？

```bash
# 检查 POTCAR 中的 ENMAX 值
grep "ENMAX" outputs/melt_quench_simulation/POTCAR

# 在 INCAR 中设置 ENCUT 为最大值（或更高）
# 例如，如果最大 ENMAX 是 350 eV，设置 ENCUT = 400 eV
```

## 快速检查清单

在运行 VASP 计算前，确认：

- [ ] 已获得合法的 VASP 许可证
- [ ] POTCAR 文件已下载/获取
- [ ] 元素顺序与 POSCAR 匹配（Fe Si B）
- [ ] 所有三个元素的 POTCAR 都存在
- [ ] ENCUT 值足够高（检查 ENMAX）
- [ ] POTCAR 文件已正确连接到 `outputs/melt_quench_simulation/POTCAR`

## 使用辅助脚本

我们提供了两个辅助脚本：

### 1. `download_potcar.py` - 检查和建议

```bash
# 检查 VASP 安装和现有文件
python3 scripts/download_potcar.py

# 只检查 VASP 安装
python3 scripts/download_potcar.py --check-vasp

# 只检查现有 POTCAR
python3 scripts/download_potcar.py --check-existing

# 创建目录结构
python3 scripts/download_potcar.py --setup-dirs
```

### 2. `prepare_potcar.py` - 准备最终 POTCAR

```bash
# 从 VASP 赝势库准备
python3 scripts/prepare_potcar.py \
    --pp-path /path/to/potpaw_PBE \
    --elements Fe Si B

# 从自定义文件准备
python3 scripts/prepare_potcar.py \
    --custom-pots Fe_POTCAR Si_POTCAR B_POTCAR \
    --elements Fe Si B
```

## 下一步

准备好 POTCAR 文件后：

1. 验证文件正确性（见上方验证步骤）
2. 检查 INCAR 中的 ENCUT 设置
3. 运行熔融-淬火模拟：
   ```bash
   cd outputs/melt_quench_simulation
   ./run_all_stages.sh
   ```

## 参考资料

- [VASP 官方网站](https://www.vasp.at/)
- [VASP 手册 - 赝势部分](https://www.vasp.at/wiki/index.php/Pseudopotentials)
- 您的 VASP 安装文档

---

**注意**: 本指南仅提供合法的 POTCAR 获取方法。请确保您有使用 VASP 和其资源的合法权限。

