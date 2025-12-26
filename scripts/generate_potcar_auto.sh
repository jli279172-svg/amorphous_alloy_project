#!/bin/bash
# 自动生成 POTCAR 文件的脚本

set -e

PROJECT_ROOT="/Users/lijunchen/coding/amorphous_alloy_project"
VASPKIT_BIN="$PROJECT_ROOT/tools/vaspkit.1.5.0/bin/vaspkit"
TEMP_DIR="$PROJECT_ROOT/data/temp_vaspkit"
OUTPUT_DIR="$PROJECT_ROOT/outputs/melt_quench_simulation"

echo "=========================================="
echo "自动生成 POTCAR 文件"
echo "=========================================="
echo ""

# 1. 检查 vaspkit
if [ ! -f "$VASPKIT_BIN" ]; then
    echo "错误: 未找到 vaspkit"
    exit 1
fi
echo "✓ vaspkit 已找到"

# 2. 检查 POSCAR
if [ ! -f "$TEMP_DIR/POSCAR" ]; then
    echo "错误: 未找到 POSCAR 文件"
    exit 1
fi
echo "✓ POSCAR 文件已找到"

# 3. 检查配置文件
if [ ! -f "$HOME/.vaspkit" ]; then
    echo "警告: ~/.vaspkit 配置文件不存在"
    echo "请先配置 VASP 赝势库路径"
    exit 1
fi

PBE_PATH=$(grep "^PBE_PATH" ~/.vaspkit | awk -F'=' '{print $2}' | xargs)
if [ -z "$PBE_PATH" ] || [ "$PBE_PATH" = "~/POTCAR/PBE" ]; then
    echo "警告: PBE_PATH 未设置或使用默认值"
    echo "当前设置: $PBE_PATH"
    echo "请编辑 ~/.vaspkit 设置正确的 PBE_PATH"
    read -p "是否继续？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo "✓ 配置文件检查完成"

# 4. 切换到临时目录
cd "$TEMP_DIR"
echo ""
echo "当前目录: $(pwd)"
echo "POSCAR 内容预览:"
head -7 POSCAR
echo ""

# 5. 运行 vaspkit（交互式）
echo "=========================================="
echo "运行 vaspkit 生成 POTCAR"
echo "=========================================="
echo ""
echo "请按照以下步骤操作:"
echo "1. 输入: 1 (选择 VASP Input Files Generator)"
echo "2. 输入: 103 (自动生成 POTCAR，推荐)"
echo "   或输入: 104 (手动选择: Fe_pv, Si, B)"
echo ""
echo "按 Enter 开始..."
read

# 运行 vaspkit
"$VASPKIT_BIN"

# 6. 检查生成的 POTCAR
echo ""
echo "=========================================="
echo "检查生成的 POTCAR"
echo "=========================================="

if [ -f "POTCAR" ] && [ -s "POTCAR" ]; then
    echo "✓ POTCAR 文件已生成"
    echo ""
    echo "文件信息:"
    ls -lh POTCAR
    echo ""
    echo "元素检查:"
    ELEMENT_COUNT=$(grep -c "TITEL" POTCAR 2>/dev/null || echo "0")
    echo "  元素数量: $ELEMENT_COUNT"
    
    if [ "$ELEMENT_COUNT" -eq "3" ]; then
        echo "  元素列表:"
        grep "TITEL" POTCAR | sed 's/.*TITEL.*= PAW //' | sed 's/ .*//'
        echo ""
        echo "✓ POTCAR 文件有效！"
        
        # 7. 复制到目标位置
        echo ""
        echo "复制 POTCAR 到目标位置..."
        mkdir -p "$OUTPUT_DIR"
        cp POTCAR "$OUTPUT_DIR/POTCAR"
        echo "✓ 已复制到: $OUTPUT_DIR/POTCAR"
        
        # 8. 最终验证
        echo ""
        echo "=========================================="
        echo "最终验证"
        echo "=========================================="
        echo "POSCAR 元素顺序:"
        head -6 "$TEMP_DIR/POSCAR" | tail -1
        echo ""
        echo "POTCAR 元素顺序:"
        grep "TITEL" "$OUTPUT_DIR/POTCAR" | sed 's/.*TITEL.*= PAW //' | sed 's/ .*//' | tr '\n' ' '
        echo ""
        echo ""
        
        # 检查顺序是否匹配
        POSCAR_ELEMENTS=$(head -6 "$TEMP_DIR/POSCAR" | tail -1)
        POTCAR_ELEMENTS=$(grep "TITEL" "$OUTPUT_DIR/POTCAR" | sed 's/.*TITEL.*= PAW //' | sed 's/ .*//' | tr '\n' ' ' | xargs)
        
        if [ "$POSCAR_ELEMENTS" = "$POTCAR_ELEMENTS" ]; then
            echo "✓ 元素顺序匹配！"
        else
            echo "⚠ 警告: 元素顺序可能不匹配"
            echo "  POSCAR: $POSCAR_ELEMENTS"
            echo "  POTCAR: $POTCAR_ELEMENTS"
        fi
        
        echo ""
        echo "=========================================="
        echo "✓ POTCAR 文件生成完成！"
        echo "=========================================="
        echo ""
        echo "文件位置: $OUTPUT_DIR/POTCAR"
        echo ""
        echo "下一步: 可以开始运行 VASP 计算"
        echo "  cd $OUTPUT_DIR"
        echo "  ./run_all_stages.sh"
        
    else
        echo "⚠ 警告: POTCAR 中元素数量不是 3"
        echo "请检查生成过程"
    fi
else
    echo "✗ POTCAR 文件未生成或为空"
    echo "请检查 vaspkit 的输出信息"
    exit 1
fi

