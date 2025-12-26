
# POTCAR 文件获取指南

## 方法 1: 使用 VASP 官方赝势库（需要 VASP 许可证）

如果您有 VASP 许可证：

1. 从 VASP 官方网站或您的 VASP 供应商获取赝势库
2. 赝势库通常包含在 VASP 安装包中
3. 解压到本地目录，例如：`/opt/vasp/potpaw_PBE/`

## 方法 2: 从学术机构获取

许多大学和研究机构提供 VASP 赝势库访问：

1. 联系您所在机构的计算中心
2. 检查是否有共享的 VASP 赝势库
3. 通常位于：`/shared/vasp/potpaw_PBE/` 或类似位置

## 方法 3: 使用开源替代方案

### 选项 A: 使用 pymatgen 生成（如果可用）

```bash
pip install pymatgen
python3 -c "
from pymatgen.io.vasp import Potcar
# 注意：这需要 VASP 赝势库的访问权限
"
```

### 选项 B: 从 Materials Project 获取结构信息

Materials Project 提供结构数据，但通常不直接提供 POTCAR：
- 网站: https://materialsproject.org
- API: https://next-gen.materialsproject.org/api

## 方法 4: 联系 VASP 支持

如果您是 VASP 用户：
- 联系 VASP 技术支持
- 或联系您的 VASP 供应商

## 所需文件

对于 Fe80Si10B10，您需要：
- Fe/POTCAR (或 Fe_pv/POTCAR)
- Si/POTCAR (或 Si_sv/POTCAR)  
- B/POTCAR (或 B_sv/POTCAR)

## 验证下载的文件

下载后，验证文件：

```bash
# 检查文件是否存在
ls -lh Fe/POTCAR Si/POTCAR B/POTCAR

# 检查文件内容
head -5 Fe/POTCAR
grep "TITEL" Fe/POTCAR
```
