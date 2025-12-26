#!/usr/bin/env python3
"""
查找 VASP 赝势库路径
"""

import os
from pathlib import Path

def check_path(path_str):
    """检查路径是否存在且包含必需元素"""
    path = Path(path_str)
    if not path.exists():
        return False, "路径不存在"
    
    if not path.is_dir():
        return False, "不是目录"
    
    # 检查必需元素
    required = ['Fe', 'Si', 'B']
    missing = []
    for elem in required:
        potcar_file = path / elem / "POTCAR"
        if not potcar_file.exists():
            missing.append(elem)
    
    if missing:
        return False, f"缺少元素: {', '.join(missing)}"
    
    return True, "完整"

def find_vasp_pp():
    """查找 VASP 赝势库路径"""
    print("=" * 60)
    print("查找 VASP 赝势库路径")
    print("=" * 60)
    print()
    
    found_paths = []
    
    # 1. 检查配置文件
    print("1. 检查 ~/.vaspkit 配置文件...")
    config_file = Path.home() / ".vaspkit"
    if config_file.exists():
        with open(config_file, 'r') as f:
            for line in f:
                if line.strip().startswith('PBE_PATH'):
                    parts = line.split('=')
                    if len(parts) >= 2:
                        pbe_path = parts[1].strip().split('#')[0].strip()
                        pbe_path = os.path.expanduser(pbe_path)
                        print(f"   配置的路径: {pbe_path}")
                        is_valid, msg = check_path(pbe_path)
                        if is_valid:
                            print(f"   ✓ 有效！{msg}")
                            found_paths.append((pbe_path, "配置文件"))
                        else:
                            print(f"   ⚠ {msg}")
    else:
        print("   ~/.vaspkit 不存在")
    print()
    
    # 2. 检查环境变量
    print("2. 检查环境变量...")
    env_vars = ['VASP_PP_PATH', 'VASP_POTENTIALS', 'POTCAR_PATH']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"   {var} = {value}")
            is_valid, msg = check_path(value)
            if is_valid:
                print(f"   ✓ 有效！{msg}")
                found_paths.append((value, f"环境变量 {var}"))
            else:
                print(f"   ⚠ {msg}")
    print()
    
    # 3. 检查常见路径
    print("3. 检查常见路径...")
    home = Path.home()
    common_paths = [
        "/opt/vasp/potpaw_PBE",
        "/opt/vasp/potpaw_PBE.54",
        "/usr/local/vasp/potpaw_PBE",
        "/usr/local/vasp/potpaw_PBE.54",
        str(home / "vasp" / "potpaw_PBE"),
        str(home / "vasp" / "potpaw_PBE.54"),
        str(home / "POTCAR" / "PBE"),
        str(home / "POTCAR" / "PBE.54"),
        "/shared/vasp/potpaw_PBE",
        "/Applications/vasp/potpaw_PBE",
        "/sw/vasp/potpaw_PBE",
    ]
    
    for path_str in common_paths:
        path = Path(path_str)
        if path.exists():
            print(f"   检查: {path_str}")
            is_valid, msg = check_path(path_str)
            if is_valid:
                print(f"   ✓ 找到！{msg}")
                found_paths.append((path_str, "常见路径"))
            elif "缺少" not in msg:
                print(f"   - 目录存在但可能不完整")
    print()
    
    # 4. 搜索系统（限制深度和范围）
    print("4. 搜索系统中的 potpaw 目录...")
    search_roots = [
        Path("/opt"),
        Path("/usr/local"),
        Path.home(),
    ]
    
    search_results = []
    for root in search_roots:
        if root.exists():
            try:
                for item in root.rglob("potpaw*"):
                    if item.is_dir() and item.depth <= 3:
                        search_results.append(item)
                        if len(search_results) >= 5:
                            break
            except (PermissionError, OSError):
                pass
    
    if search_results:
        print(f"   找到 {len(search_results)} 个可能的目录:")
        for path in search_results[:5]:
            print(f"     - {path}")
            is_valid, msg = check_path(str(path))
            if is_valid:
                print(f"       ✓ 有效！{msg}")
                found_paths.append((str(path), "系统搜索"))
    else:
        print("   未找到 potpaw 目录")
    print()
    
    # 5. 总结
    print("=" * 60)
    print("查找结果")
    print("=" * 60)
    
    if found_paths:
        print(f"✓ 找到 {len(found_paths)} 个有效的 VASP 赝势库路径:")
        print()
        for i, (path, source) in enumerate(found_paths, 1):
            print(f"{i}. {path}")
            print(f"   来源: {source}")
            print()
        
        # 推荐第一个
        recommended = found_paths[0][0]
        print("推荐使用:")
        print(f"  {recommended}")
        print()
        print("设置方法:")
        print(f"  vi ~/.vaspkit")
        print(f"  修改: PBE_PATH = {recommended}")
    else:
        print("⚠ 未找到 VASP 赝势库路径")
        print()
        print("可能的原因:")
        print("1. VASP 赝势库未安装")
        print("2. 安装在非标准位置")
        print("3. 需要从 VASP 官方网站下载")
        print()
        print("解决方案:")
        print("1. 如果您有 VASP 许可证:")
        print("   - 访问 https://www.vasp.at/")
        print("   - 登录并下载 potpaw_PBE.tgz")
        print("   - 解压到某个目录，例如: ~/vasp/potpaw_PBE")
        print()
        print("2. 联系您所在机构的计算中心")
        print("   询问共享的 VASP 赝势库路径")
        print()
        print("3. 如果您知道路径，手动设置:")
        print("   vi ~/.vaspkit")
        print("   修改: PBE_PATH = /您的实际路径")
    
    print("=" * 60)

if __name__ == "__main__":
    find_vasp_pp()

