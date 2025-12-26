#!/usr/bin/env python3
"""
Script to help download or locate POTCAR files for Fe, Si, B.
Provides multiple options including Materials Project API and manual instructions.
"""

import os
import sys
import argparse
from pathlib import Path

# Try to import requests (optional)
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# Materials Project API endpoint (requires API key)
MP_API_BASE = "https://api.materialsproject.org"
MP_POTCAR_BASE = "https://www.materialsproject.org/static/calculators/"


def check_vasp_installation():
    """Check if VASP is installed and find POTCAR directory."""
    print("=" * 60)
    print("检查 VASP 安装...")
    print("=" * 60)
    
    # Common VASP POTCAR locations
    common_paths = [
        "/opt/vasp/potpaw_PBE",
        "/opt/vasp/potpaw_PBE.54",
        "/usr/local/vasp/potpaw_PBE",
        "/usr/local/vasp/potpaw_PBE.54",
        os.path.expanduser("~/vasp/potpaw_PBE"),
        os.path.expanduser("~/vasp/potpaw_PBE.54"),
    ]
    
    # Check environment variable
    vasp_pp_path = os.environ.get("VASP_PP_PATH")
    if vasp_pp_path:
        common_paths.insert(0, vasp_pp_path)
        common_paths.insert(1, os.path.join(vasp_pp_path, "potpaw_PBE"))
    
    found_paths = []
    for path in common_paths:
        full_path = Path(path)
        if full_path.exists():
            # Check if it contains element directories
            fe_path = full_path / "Fe"
            if fe_path.exists() and (fe_path / "POTCAR").exists():
                found_paths.append(full_path)
                print(f"✓ 找到 VASP 赝势库: {full_path}")
    
    if found_paths:
        print(f"\n建议使用路径: {found_paths[0]}")
        return found_paths[0]
    else:
        print("✗ 未找到 VASP 赝势库")
        print("\n请检查以下位置之一：")
        for path in common_paths[:5]:
            print(f"  - {path}")
        return None


def download_from_materials_project(api_key=None, elements=None):
    """
    Download POTCAR files from Materials Project (if available).
    Note: This requires API key and may not always be available.
    """
    if not HAS_REQUESTS:
        print("\n注意: 需要安装 requests 库才能使用此功能")
        print("安装: pip install requests")
        return False
    
    if not api_key:
        print("\n" + "=" * 60)
        print("Materials Project 选项")
        print("=" * 60)
        print("Materials Project 提供一些赝势文件，但需要 API key。")
        print("获取 API key: https://next-gen.materialsproject.org/api")
        print("\n如果您有 API key，请使用 --mp-api-key 参数")
        return False
    
    print("\n" + "=" * 60)
    print("从 Materials Project 下载...")
    print("=" * 60)
    
    # Note: Materials Project may not provide direct POTCAR downloads
    # This is a placeholder for the actual implementation
    print("注意: Materials Project 可能不直接提供 POTCAR 文件下载")
    print("建议使用其他方法")
    return False


def create_download_instructions():
    """Create instructions for manual download."""
    instructions = """
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
"""
    return instructions


def setup_local_potcar_structure():
    """Create directory structure for POTCAR files."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    potcar_dir = project_root / "data" / "potcars"
    
    potcar_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for each element
    for element in ["Fe", "Si", "B"]:
        (potcar_dir / element).mkdir(exist_ok=True)
    
    print(f"\n已创建目录结构: {potcar_dir}")
    print("请将 POTCAR 文件放置到以下位置：")
    print(f"  - {potcar_dir}/Fe/POTCAR")
    print(f"  - {potcar_dir}/Si/POTCAR")
    print(f"  - {potcar_dir}/B/POTCAR")
    
    return potcar_dir


def check_existing_potcars():
    """Check if POTCAR files already exist in common locations."""
    print("\n" + "=" * 60)
    print("检查现有 POTCAR 文件...")
    print("=" * 60)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Check project data directory
    potcar_dir = project_root / "data" / "potcars"
    if potcar_dir.exists():
        for element in ["Fe", "Si", "B"]:
            potcar_file = potcar_dir / element / "POTCAR"
            if potcar_file.exists():
                print(f"✓ 找到 {element}/POTCAR: {potcar_file}")
            else:
                print(f"✗ 未找到 {element}/POTCAR")
    
    # Check simulation directory
    sim_dir = project_root / "outputs" / "melt_quench_simulation"
    potcar_file = sim_dir / "POTCAR"
    if potcar_file.exists():
        print(f"✓ 找到已连接的 POTCAR: {potcar_file}")
        return True
    
    return False


def main():
    parser = argparse.ArgumentParser(
        description='帮助下载或定位 POTCAR 文件',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--check-vasp',
        action='store_true',
        help='检查 VASP 安装和赝势库位置'
    )
    
    parser.add_argument(
        '--check-existing',
        action='store_true',
        help='检查是否已有 POTCAR 文件'
    )
    
    parser.add_argument(
        '--setup-dirs',
        action='store_true',
        help='创建本地 POTCAR 目录结构'
    )
    
    parser.add_argument(
        '--mp-api-key',
        type=str,
        help='Materials Project API key（如果可用）'
    )
    
    parser.add_argument(
        '--instructions',
        action='store_true',
        help='显示详细的下载说明'
    )
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        # Default: run all checks
        args.check_vasp = True
        args.check_existing = True
        args.setup_dirs = True
        args.instructions = True
    
    print("=" * 60)
    print("POTCAR 文件获取助手")
    print("=" * 60)
    
    vasp_path = None
    if args.check_vasp:
        vasp_path = check_vasp_installation()
    
    if args.check_existing:
        has_potcar = check_existing_potcars()
        if has_potcar:
            print("\n✓ 已找到 POTCAR 文件！")
            print("您可以使用 prepare_potcar.py 来准备最终的 POTCAR 文件")
            return
    
    if args.setup_dirs:
        potcar_dir = setup_local_potcar_structure()
    
    if args.instructions:
        instructions = create_download_instructions()
        instructions_file = Path(__file__).parent.parent / "docs" / "POTCAR_DOWNLOAD_INSTRUCTIONS.md"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        print(f"\n详细说明已保存到: {instructions_file}")
    
    if args.mp_api_key:
        download_from_materials_project(args.mp_api_key)
    
    print("\n" + "=" * 60)
    print("下一步操作")
    print("=" * 60)
    
    if vasp_path:
        print(f"\n1. 如果您的 VASP 赝势库在: {vasp_path}")
        print("   运行以下命令准备 POTCAR:")
        print(f"   python3 scripts/prepare_potcar.py --pp-path {vasp_path} --elements Fe Si B")
    else:
        print("\n1. 获取 POTCAR 文件:")
        print("   - 从 VASP 官方获取（需要许可证）")
        print("   - 从您所在机构的计算中心获取")
        print("   - 查看 docs/POTCAR_DOWNLOAD_INSTRUCTIONS.md 获取详细说明")
    
    print("\n2. 将 POTCAR 文件放置到 data/potcars/ 目录")
    print("   或使用 --pp-path 指定 VASP 赝势库路径")
    
    print("\n3. 准备最终的 POTCAR 文件:")
    print("   python3 scripts/prepare_potcar.py --elements Fe Si B")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

