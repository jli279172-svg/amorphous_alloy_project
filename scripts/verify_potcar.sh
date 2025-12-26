#!/bin/bash
# 验证 POTCAR 文件的脚本

PROJECT_ROOT="/Users/lijunchen/coding/amorphous_alloy_project"
POTCAR_FILE="$PROJECT_ROOT/outputs/melt_quench_simulation/POTCAR"
POSCAR_FILE="$PROJECT_ROOT/outputs/POSCAR_initial"

echo "=========================================="
echo "POTCAR 文件验证"
echo "=========================================="
echo ""

if [ ! -f "$POTCAR_FILE" ]; then
    echo "✗ POTCAR 文件不存在: $POTCAR_FILE"
    echo ""
    echo "请先生成 POTCAR 文件"
    exit 1
fi

# 检查文件大小
SIZE=$(stat -f%z "$POTCAR_FILE" 2>/dev/null || stat -c%s "$POTCAR_FILE" 2>/dev/null)
if [ "$SIZE" -eq 0 ]; then
    echo "✗ POTCAR 文件为空"
    exit 1
fi

echo "✓ POTCAR 文件存在"
echo "  文件大小: $(ls -lh "$POTCAR_FILE" | awk '{print $5}')"
echo ""

# 检查元素数量
ELEMENT_COUNT=$(grep -c "TITEL" "$POTCAR_FILE" 2>/dev/null || echo "0")
echo "元素检查:"
echo "  元素数量: $ELEMENT_COUNT"

if [ "$ELEMENT_COUNT" -ne "3" ]; then
    echo "  ✗ 错误: 应该是 3 个元素"
    exit 1
fi

echo "  ✓ 元素数量正确"
echo ""

# 显示元素列表
echo "元素列表:"
grep "TITEL" "$POTCAR_FILE" | sed 's/.*TITEL.*= PAW //' | sed 's/ .*//' | nl
echo ""

# 验证元素顺序
if [ -f "$POSCAR_FILE" ]; then
    POSCAR_ELEMENTS=$(head -6 "$POSCAR_FILE" | tail -1)
    POTCAR_ELEMENTS=$(grep "TITEL" "$POTCAR_FILE" | sed 's/.*TITEL.*= PAW //' | sed 's/ .*//' | tr '\n' ' ' | xargs)
    
    echo "元素顺序验证:"
    echo "  POSCAR: $POSCAR_ELEMENTS"
    echo "  POTCAR: $POTCAR_ELEMENTS"
    echo ""
    
    if [ "$POSCAR_ELEMENTS" = "$POTCAR_ELEMENTS" ]; then
        echo "  ✓ 元素顺序匹配！"
    else
        echo "  ⚠ 警告: 元素顺序不匹配"
        echo "    这可能导致 VASP 计算错误"
    fi
fi

echo ""
echo "=========================================="
echo "✓ POTCAR 文件验证完成"
echo "=========================================="

