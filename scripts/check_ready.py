#!/usr/bin/env python3
"""
检查项目文件结构是否准备好进行 VASP 计算
"""

import os
from pathlib import Path

def check_file(filepath, description, required=True):
    """检查文件是否存在且有效"""
    path = Path(filepath)
    status = "✓" if path.exists() else "✗"
    
    if path.exists():
        size = path.stat().st_size
        if size == 0:
            status = "⚠"
            result = f"{status} {description}: 存在但为空"
        else:
            result = f"{status} {description}: 存在 ({size:,} bytes)"
    else:
        result = f"{status} {description}: 不存在"
        if required:
            result += " [必需]"
    
    return result, path.exists() and path.stat().st_size > 0

def check_poscar():
    """检查 POSCAR 文件"""
    print("\n" + "="*60)
    print("1. POSCAR 文件检查")
    print("="*60)
    
    poscar_path = Path("outputs/POSCAR_initial")
    result, valid = check_file(poscar_path, "POSCAR_initial", required=True)
    print(result)
    
    if valid:
        # 检查内容
        with open(poscar_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 7:
                elements = lines[5].strip()
                counts = lines[6].strip()
                print(f"   元素: {elements}")
                print(f"   数量: {counts}")
                total_atoms = sum(int(x) for x in counts.split())
                print(f"   总原子数: {total_atoms}")
    
    return valid

def check_potcar():
    """检查 POTCAR 文件"""
    print("\n" + "="*60)
    print("2. POTCAR 文件检查")
    print("="*60)
    
    potcar_path = Path("outputs/melt_quench_simulation/POTCAR")
    result, valid = check_file(potcar_path, "POTCAR", required=True)
    print(result)
    
    if valid:
        # 检查元素
        with open(potcar_path, 'r') as f:
            content = f.read()
            titel_count = content.count('TITEL')
            print(f"   元素数量: {titel_count}")
            
            # 提取元素名称
            import re
            titels = re.findall(r'TITEL\s*=\s*PAW\s+(\w+)', content)
            if titels:
                print(f"   元素列表: {' '.join(titels)}")
    
    return valid

def check_incar_files():
    """检查 INCAR 文件"""
    print("\n" + "="*60)
    print("3. INCAR 文件检查")
    print("="*60)
    
    incar_dir = Path("outputs/melt_quench_simulation")
    incar_files = list(incar_dir.glob("INCAR_stage_*"))
    
    if incar_files:
        print(f"✓ 找到 {len(incar_files)} 个 INCAR 文件")
        for incar in sorted(incar_files):
            size = incar.stat().st_size
            print(f"   {incar.name}: {size:,} bytes")
        return True
    else:
        print("✗ 未找到 INCAR 文件 [必需]")
        return False

def check_kpoints():
    """检查 KPOINTS 文件"""
    print("\n" + "="*60)
    print("4. KPOINTS 文件检查")
    print("="*60)
    
    kpoints_path = Path("outputs/melt_quench_simulation/KPOINTS")
    result, valid = check_file(kpoints_path, "KPOINTS", required=True)
    print(result)
    
    if valid:
        with open(kpoints_path, 'r') as f:
            lines = f.readlines()
            print(f"   行数: {len(lines)}")
            if len(lines) > 0:
                print(f"   第一行: {lines[0].strip()}")
    
    return valid

def check_scripts():
    """检查运行脚本"""
    print("\n" + "="*60)
    print("5. 运行脚本检查")
    print("="*60)
    
    script_dir = Path("outputs/melt_quench_simulation")
    master_script = script_dir / "run_all_stages.sh"
    stage_scripts = list(script_dir.glob("run_stage_*.sh"))
    
    master_exists = master_script.exists()
    print(f"{'✓' if master_exists else '✗'} run_all_stages.sh: {'存在' if master_exists else '不存在'}")
    
    if stage_scripts:
        print(f"✓ 找到 {len(stage_scripts)} 个阶段脚本")
    else:
        print("✗ 未找到阶段脚本")
    
    return master_exists and len(stage_scripts) > 0

def check_compatibility():
    """检查 POSCAR 和 POTCAR 的兼容性"""
    print("\n" + "="*60)
    print("6. POSCAR 与 POTCAR 兼容性检查")
    print("="*60)
    
    poscar_path = Path("outputs/POSCAR_initial")
    potcar_path = Path("outputs/melt_quench_simulation/POTCAR")
    
    if not poscar_path.exists() or not potcar_path.exists():
        print("✗ 无法检查：缺少必要文件")
        return False
    
    # 读取 POSCAR 元素
    with open(poscar_path, 'r') as f:
        poscar_lines = f.readlines()
        if len(poscar_lines) >= 6:
            poscar_elements = poscar_lines[5].strip().split()
        else:
            print("✗ POSCAR 格式错误")
            return False
    
    # 读取 POTCAR 元素
    with open(potcar_path, 'r') as f:
        content = f.read()
        import re
        potcar_elements = re.findall(r'TITEL\s*=\s*PAW\s+(\w+)', content)
    
    if not potcar_elements:
        print("✗ 无法从 POTCAR 读取元素")
        return False
    
    # 比较
    print(f"   POSCAR 元素顺序: {' '.join(poscar_elements)}")
    print(f"   POTCAR 元素顺序: {' '.join(potcar_elements)}")
    
    if poscar_elements == potcar_elements:
        print("   ✓ 元素顺序匹配！")
        return True
    else:
        print("   ✗ 元素顺序不匹配！")
        print("   ⚠ 警告：这会导致 VASP 计算错误！")
        return False

def main():
    """主检查函数"""
    print("="*60)
    print("VASP 计算准备状态检查")
    print("="*60)
    
    # 切换到项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    results = {}
    
    # 检查各项
    results['POSCAR'] = check_poscar()
    results['POTCAR'] = check_potcar()
    results['INCAR'] = check_incar_files()
    results['KPOINTS'] = check_kpoints()
    results['Scripts'] = check_scripts()
    results['Compatibility'] = check_compatibility()
    
    # 总结
    print("\n" + "="*60)
    print("检查总结")
    print("="*60)
    
    all_ready = True
    for item, status in results.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {item}")
        if not status:
            all_ready = False
    
    print("\n" + "="*60)
    if all_ready:
        print("✓ 所有文件已准备就绪！")
        print("  可以开始运行 VASP 计算")
        print("\n下一步:")
        print("  cd outputs/melt_quench_simulation")
        print("  ./run_all_stages.sh")
    else:
        print("✗ 部分文件缺失，需要准备:")
        if not results['POTCAR']:
            print("  - POTCAR 文件（最重要！）")
            print("    运行: python3 scripts/prepare_potcar_vaspkit.py")
            print("    或查看: docs/POTCAR_DOWNLOAD_GUIDE_CN.md")
        if not results['INCAR']:
            print("  - INCAR 文件")
            print("    运行: python3 scripts/run_melt_quench.py")
        if not results['KPOINTS']:
            print("  - KPOINTS 文件")
            print("    运行: python3 scripts/run_melt_quench.py")
    print("="*60)

if __name__ == "__main__":
    main()

