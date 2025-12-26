#!/usr/bin/env python3
"""
如果 data/potcars 目录中有 POTCAR 文件，使用它们生成最终的 POTCAR
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
POTCARS_DIR = PROJECT_ROOT / "data" / "potcars"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "melt_quench_simulation"
POSCAR_FILE = PROJECT_ROOT / "outputs" / "POSCAR_initial"

def check_local_potcars():
    """检查本地 POTCAR 文件"""
    print("=" * 60)
    print("检查本地 POTCAR 文件")
    print("=" * 60)
    print()
    
    elements = ['Fe', 'Si', 'B']
    potcar_files = {}
    
    for elem in elements:
        potcar_path = POTCARS_DIR / elem / "POTCAR"
        if potcar_path.exists() and potcar_path.stat().st_size > 0:
            size = potcar_path.stat().st_size
            print(f"✓ 找到 {elem}/POTCAR: {size:,} bytes")
            potcar_files[elem] = potcar_path
        else:
            print(f"✗ 未找到 {elem}/POTCAR")
    
    print()
    return potcar_files

def generate_potcar_from_local(potcar_files):
    """从本地文件生成 POTCAR"""
    print("=" * 60)
    print("从本地文件生成 POTCAR")
    print("=" * 60)
    print()
    
    # 读取 POSCAR 获取元素顺序
    with open(POSCAR_FILE, 'r') as f:
        poscar_lines = f.readlines()
        poscar_elements = poscar_lines[5].strip().split()
    
    print(f"POSCAR 元素顺序: {' '.join(poscar_elements)}")
    print()
    
    # 按 POSCAR 顺序连接 POTCAR
    output_path = OUTPUT_DIR / "POTCAR"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("连接 POTCAR 文件...")
    with open(output_path, 'wb') as outfile:
        for elem in poscar_elements:
            if elem in potcar_files:
                print(f"  添加 {elem}...")
                with open(potcar_files[elem], 'rb') as infile:
                    outfile.write(infile.read())
            else:
                print(f"  ✗ 错误: 缺少 {elem} 的 POTCAR")
                return False
    
    print()
    print(f"✓ POTCAR 已生成: {output_path}")
    return True

def verify_potcar():
    """验证生成的 POTCAR"""
    potcar_file = OUTPUT_DIR / "POTCAR"
    
    if not potcar_file.exists() or potcar_file.stat().st_size == 0:
        return False, "POTCAR 不存在或为空"
    
    with open(potcar_file, 'r') as f:
        content = f.read()
    
    import re
    titels = re.findall(r'TITEL\s*=\s*PAW\s+(\w+)', content)
    
    if len(titels) != 3:
        return False, f"元素数量错误: {len(titels)}"
    
    return True, titels

def main():
    """主函数"""
    # 检查本地 POTCAR
    potcar_files = check_local_potcars()
    
    if len(potcar_files) != 3:
        print("⚠ 本地 POTCAR 文件不完整")
        print()
        print("请:")
        print("1. 将 POTCAR 文件放置到:")
        print(f"   {POTCARS_DIR}/Fe/POTCAR")
        print(f"   {POTCARS_DIR}/Si/POTCAR")
        print(f"   {POTCARS_DIR}/B/POTCAR")
        print()
        print("2. 或使用 vaspkit 生成 POTCAR")
        print("3. 或从 VASP 赝势库连接")
        return
    
    # 生成 POTCAR
    if generate_potcar_from_local(potcar_files):
        # 验证
        is_valid, result = verify_potcar()
        if is_valid:
            print()
            print("=" * 60)
            print("✓ POTCAR 验证成功")
            print("=" * 60)
            print()
            print(f"元素列表: {' '.join(result)}")
            print(f"文件位置: {OUTPUT_DIR / 'POTCAR'}")
            print(f"文件大小: {os.path.getsize(OUTPUT_DIR / 'POTCAR'):,} bytes")
            print()
            print("下一步: 可以开始运行 VASP 计算")
            print(f"  cd {OUTPUT_DIR}")
            print("  ./run_all_stages.sh")
        else:
            print(f"✗ 验证失败: {result}")

if __name__ == "__main__":
    main()

