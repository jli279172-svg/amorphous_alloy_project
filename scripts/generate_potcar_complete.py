#!/usr/bin/env python3
"""
完整的 POTCAR 生成流程
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
VASPKIT_BIN = PROJECT_ROOT / "tools" / "vaspkit.1.5.0" / "bin" / "vaspkit"
TEMP_DIR = PROJECT_ROOT / "data" / "temp_vaspkit"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "melt_quench_simulation"
CONFIG_FILE = Path.home() / ".vaspkit"

def check_vaspkit():
    """检查 vaspkit"""
    print("=" * 60)
    print("步骤 1: 检查 vaspkit")
    print("=" * 60)
    
    if not VASPKIT_BIN.exists():
        print("✗ 错误: 未找到 vaspkit")
        return False
    
    print(f"✓ vaspkit 已找到: {VASPKIT_BIN}")
    return True

def check_poscar():
    """检查 POSCAR 文件"""
    print("\n" + "=" * 60)
    print("步骤 2: 检查 POSCAR 文件")
    print("=" * 60)
    
    poscar_source = PROJECT_ROOT / "outputs" / "POSCAR_initial"
    poscar_target = TEMP_DIR / "POSCAR"
    
    if not poscar_target.exists():
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        if poscar_source.exists():
            import shutil
            shutil.copy(poscar_source, poscar_target)
            print(f"✓ POSCAR 已复制到: {poscar_target}")
        else:
            print("✗ 错误: 未找到 POSCAR_initial")
            return False
    
    # 显示 POSCAR 信息
    with open(poscar_target, 'r') as f:
        lines = f.readlines()
        if len(lines) >= 7:
            print(f"✓ POSCAR 文件已准备")
            print(f"  元素: {lines[5].strip()}")
            print(f"  数量: {lines[6].strip()}")
            return True
    
    print("✗ POSCAR 文件格式错误")
    return False

def check_pbe_path():
    """检查并设置 PBE_PATH"""
    print("\n" + "=" * 60)
    print("步骤 3: 检查 VASP 赝势库配置")
    print("=" * 60)
    
    if not CONFIG_FILE.exists():
        print("✗ 错误: ~/.vaspkit 配置文件不存在")
        return None
    
    # 读取配置文件
    pbe_path = None
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            if line.strip().startswith('PBE_PATH'):
                # 提取路径
                parts = line.split('=')
                if len(parts) >= 2:
                    pbe_path = parts[1].strip().split('#')[0].strip()
                    # 展开 ~
                    pbe_path = os.path.expanduser(pbe_path)
                    break
    
    if not pbe_path or pbe_path == "~/POTCAR/PBE":
        print("⚠ PBE_PATH 未设置或使用默认值")
        print("当前设置:", pbe_path if pbe_path else "未设置")
        print("")
        print("请手动设置 PBE_PATH:")
        print(f"1. 编辑配置文件: {CONFIG_FILE}")
        print("2. 找到 PBE_PATH 行，设置为您的实际路径")
        print("   例如: PBE_PATH = /path/to/potpaw_PBE")
        print("")
        
        # 检查常见路径
        common_paths = [
            "/opt/vasp/potpaw_PBE",
            "/usr/local/vasp/potpaw_PBE",
            str(Path.home() / "vasp" / "potpaw_PBE"),
            str(Path.home() / "POTCAR" / "PBE"),
            "/shared/vasp/potpaw_PBE",
        ]
        
        found = False
        for path in common_paths:
            test_path = Path(path)
            if test_path.exists() and (test_path / "Fe" / "POTCAR").exists():
                print(f"✓ 找到可能的路径: {path}")
                found = True
                response = input(f"是否使用此路径？(Y/n): ").strip()
                if not response or response.lower() != 'n':
                    pbe_path = path
                    # 更新配置文件
                    update_config_file(pbe_path)
                    break
        
        if not found:
            manual_path = input("请输入您的 VASP 赝势库路径（或按 Enter 退出）: ").strip()
            if manual_path:
                test_path = Path(manual_path)
                if test_path.exists() and (test_path / "Fe" / "POTCAR").exists():
                    pbe_path = manual_path
                    update_config_file(pbe_path)
                else:
                    print("✗ 路径无效或不存在 Fe/POTCAR")
                    return None
            else:
                return None
    else:
        print(f"✓ 使用配置的路径: {pbe_path}")
    
    # 验证路径
    pbe_path_obj = Path(pbe_path)
    if not pbe_path_obj.exists():
        print(f"⚠ 警告: 路径不存在: {pbe_path}")
        return None
    
    # 检查必需的元素
    required_elements = ['Fe', 'Si', 'B']
    missing = []
    for elem in required_elements:
        if not (pbe_path_obj / elem / "POTCAR").exists():
            missing.append(elem)
    
    if missing:
        print(f"⚠ 警告: 缺少元素: {', '.join(missing)}")
        print(f"   路径: {pbe_path}")
    else:
        print(f"✓ 所有必需元素都存在")
    
    return pbe_path

def update_config_file(pbe_path):
    """更新配置文件中的 PBE_PATH"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            lines = f.readlines()
        
        with open(CONFIG_FILE, 'w') as f:
            for line in lines:
                if line.strip().startswith('PBE_PATH'):
                    # 保持格式，只更新路径
                    parts = line.split('=')
                    if len(parts) >= 2:
                        comment = parts[1].split('#')[1] if '#' in parts[1] else "  #  Path of PBE potential"
                        f.write(f"PBE_PATH                      =     {pbe_path}{comment}\n")
                    else:
                        f.write(line)
                else:
                    f.write(line)
        
        print(f"✓ 已更新 ~/.vaspkit 中的 PBE_PATH")
    except Exception as e:
        print(f"⚠ 更新配置文件时出错: {e}")

def run_vaspkit():
    """运行 vaspkit 生成 POTCAR"""
    print("\n" + "=" * 60)
    print("步骤 4: 运行 vaspkit 生成 POTCAR")
    print("=" * 60)
    print("")
    print("vaspkit 是交互式程序，请按照以下步骤操作:")
    print("")
    print("1. 输入: 1")
    print("   (选择 VASP Input Files Generator)")
    print("")
    print("2. 输入: 103")
    print("   (自动生成 POTCAR，使用推荐赝势)")
    print("   或输入: 104 (手动选择每个元素的赝势类型)")
    print("")
    print("如果选择 104，推荐输入:")
    print("  - Fe: Fe_pv (包含 p 价电子，适合金属)")
    print("  - Si: Si (标准版本)")
    print("  - B: B (标准版本)")
    print("")
    input("按 Enter 开始运行 vaspkit...")
    
    # 切换到工作目录
    os.chdir(TEMP_DIR)
    
    # 运行 vaspkit
    try:
        subprocess.run([str(VASPKIT_BIN)], check=False)
    except KeyboardInterrupt:
        print("\n用户中断")
        return False
    except Exception as e:
        print(f"✗ 运行 vaspkit 时出错: {e}")
        return False
    
    return True

def verify_potcar():
    """验证生成的 POTCAR"""
    print("\n" + "=" * 60)
    print("步骤 5: 验证生成的 POTCAR")
    print("=" * 60)
    
    potcar_file = TEMP_DIR / "POTCAR"
    
    if not potcar_file.exists() or potcar_file.stat().st_size == 0:
        print("✗ POTCAR 文件未生成或为空")
        return False
    
    print(f"✓ POTCAR 文件已生成")
    print(f"  文件大小: {potcar_file.stat().st_size:,} bytes")
    print("")
    
    # 读取并检查元素
    with open(potcar_file, 'r') as f:
        content = f.read()
    
    import re
    titels = re.findall(r'TITEL\s*=\s*PAW\s+(\w+)', content)
    
    if len(titels) != 3:
        print(f"✗ 错误: POTCAR 中元素数量不是 3 (当前: {len(titels)})")
        return False
    
    print("元素检查:")
    print(f"  元素数量: {len(titels)}")
    print("  元素列表:")
    for i, elem in enumerate(titels, 1):
        print(f"    {i}. {elem}")
    print("")
    
    # 验证元素顺序
    poscar_file = TEMP_DIR / "POSCAR"
    with open(poscar_file, 'r') as f:
        poscar_lines = f.readlines()
        poscar_elements = poscar_lines[5].strip().split()
    
    potcar_elements = titels
    
    print("元素顺序验证:")
    print(f"  POSCAR: {' '.join(poscar_elements)}")
    print(f"  POTCAR: {' '.join(potcar_elements)}")
    print("")
    
    if poscar_elements == potcar_elements:
        print("✓ 元素顺序匹配！")
    else:
        print("⚠ 警告: 元素顺序不匹配")
        print("  这可能导致 VASP 计算错误")
    
    # 复制到目标位置
    print("")
    print("复制 POTCAR 到目标位置...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(potcar_file, OUTPUT_DIR / "POTCAR")
    print(f"✓ 已复制到: {OUTPUT_DIR / 'POTCAR'}")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("POTCAR 生成完整流程")
    print("=" * 60)
    print("")
    
    # 检查步骤
    if not check_vaspkit():
        sys.exit(1)
    
    if not check_poscar():
        sys.exit(1)
    
    pbe_path = check_pbe_path()
    if not pbe_path:
        print("\n请先设置正确的 PBE_PATH，然后重新运行此脚本")
        sys.exit(1)
    
    # 运行 vaspkit
    if not run_vaspkit():
        print("\n请手动运行 vaspkit 生成 POTCAR")
        sys.exit(1)
    
    # 验证
    if verify_potcar():
        print("\n" + "=" * 60)
        print("✓ POTCAR 文件生成完成！")
        print("=" * 60)
        print("")
        print(f"文件位置: {OUTPUT_DIR / 'POTCAR'}")
        print("")
        print("下一步: 可以开始运行 VASP 计算")
        print(f"  cd {OUTPUT_DIR}")
        print("  ./run_all_stages.sh")
    else:
        print("\n✗ POTCAR 验证失败")
        sys.exit(1)

if __name__ == "__main__":
    main()

