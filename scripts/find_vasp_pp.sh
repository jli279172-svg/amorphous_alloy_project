#!/bin/bash
# 查找 VASP 赝势库路径的脚本

echo "=========================================="
echo "查找 VASP 赝势库路径"
echo "=========================================="
echo ""

FOUND=0

# 1. 检查配置文件
echo "1. 检查 ~/.vaspkit 配置文件..."
if [ -f ~/.vaspkit ]; then
    PBE_PATH=$(grep "^PBE_PATH" ~/.vaspkit 2>/dev/null | awk -F'=' '{print $2}' | xargs | sed 's/#.*//' | xargs)
    if [ -n "$PBE_PATH" ] && [ "$PBE_PATH" != "~/POTCAR/PBE" ]; then
        PBE_PATH_EXPANDED=$(eval echo "$PBE_PATH")
        if [ -d "$PBE_PATH_EXPANDED" ]; then
            echo "  找到配置的路径: $PBE_PATH"
            echo "  展开后: $PBE_PATH_EXPANDED"
            if [ -f "$PBE_PATH_EXPANDED/Fe/POTCAR" ]; then
                echo "  ✓ 验证: 包含 Fe/POTCAR"
                FOUND=1
            else
                echo "  ⚠ 警告: 路径存在但可能不完整"
            fi
        fi
    fi
fi
echo ""

# 2. 检查环境变量
echo "2. 检查环境变量..."
if [ -n "$VASP_PP_PATH" ]; then
    echo "  VASP_PP_PATH = $VASP_PP_PATH"
    if [ -d "$VASP_PP_PATH" ] && [ -f "$VASP_PP_PATH/Fe/POTCAR" ]; then
        echo "  ✓ 找到有效的路径"
        FOUND=1
    fi
fi
echo ""

# 3. 检查常见路径
echo "3. 检查常见路径..."
COMMON_PATHS=(
    "/opt/vasp/potpaw_PBE"
    "/opt/vasp/potpaw_PBE.54"
    "/usr/local/vasp/potpaw_PBE"
    "/usr/local/vasp/potpaw_PBE.54"
    "$HOME/vasp/potpaw_PBE"
    "$HOME/vasp/potpaw_PBE.54"
    "$HOME/POTCAR/PBE"
    "$HOME/POTCAR/PBE.54"
    "/shared/vasp/potpaw_PBE"
    "/Applications/vasp/potpaw_PBE"
    "/sw/vasp/potpaw_PBE"
)

for path in "${COMMON_PATHS[@]}"; do
    if [ -d "$path" ]; then
        echo "  检查: $path"
        if [ -f "$path/Fe/POTCAR" ] && [ -f "$path/Si/POTCAR" ] && [ -f "$path/B/POTCAR" ]; then
            echo "    ✓ 找到！包含所有必需元素 (Fe, Si, B)"
            echo "    推荐使用此路径"
            FOUND=1
            break
        elif [ -f "$path/Fe/POTCAR" ]; then
            echo "    - 目录存在，包含 Fe，但可能缺少其他元素"
        else
            echo "    - 目录存在但可能不是 PBE 赝势库"
        fi
    fi
done
echo ""

# 4. 搜索系统
echo "4. 搜索系统中的 potpaw 目录..."
SEARCH_RESULTS=$(find /opt /usr/local "$HOME" -maxdepth 4 -type d -name "*potpaw*" 2>/dev/null | head -5)
if [ -n "$SEARCH_RESULTS" ]; then
    echo "  找到以下目录:"
    echo "$SEARCH_RESULTS" | while read dir; do
        echo "    - $dir"
        if [ -f "$dir/Fe/POTCAR" ]; then
            echo "      ✓ 包含 Fe/POTCAR"
        fi
    done
else
    echo "  未找到 potpaw 目录"
fi
echo ""

# 5. 总结
echo "=========================================="
if [ $FOUND -eq 1 ]; then
    echo "✓ 找到 VASP 赝势库路径"
    echo ""
    echo "请将找到的路径设置到 ~/.vaspkit 文件中:"
    echo "  vi ~/.vaspkit"
    echo "  修改: PBE_PATH = /找到的路径"
else
    echo "⚠ 未找到 VASP 赝势库路径"
    echo ""
    echo "可能的原因:"
    echo "1. VASP 赝势库未安装"
    echo "2. 安装在非标准位置"
    echo "3. 需要从 VASP 官方网站下载"
    echo ""
    echo "解决方案:"
    echo "1. 如果您有 VASP 许可证，从 https://www.vasp.at/ 下载"
    echo "2. 联系您所在机构的计算中心"
    echo "3. 如果您知道路径，手动设置到 ~/.vaspkit"
fi
echo "=========================================="

