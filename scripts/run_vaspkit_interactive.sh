#!/bin/bash
# 交互式运行 vaspkit 生成 POTCAR 的脚本

cd /Users/lijunchen/coding/amorphous_alloy_project/data/temp_vaspkit

echo "=========================================="
echo "准备使用 vaspkit 生成 POTCAR"
echo "=========================================="
echo ""
echo "当前目录: $(pwd)"
echo "POSCAR 文件: $(ls -lh POSCAR 2>/dev/null || echo '未找到')"
echo ""

# 检查 vaspkit
if ! command -v vaspkit &> /dev/null; then
    echo "错误: vaspkit 未找到"
    echo ""
    echo "请:"
    echo "1. 安装 vaspkit"
    echo "2. 或将 vaspkit 添加到 PATH"
    echo "3. 或使用以下命令运行:"
    echo "   /path/to/vaspkit/bin/vaspkit"
    echo ""
    exit 1
fi

echo "✓ vaspkit 已找到"
echo ""
echo "=========================================="
echo "运行 vaspkit"
echo "=========================================="
echo ""
echo "请按照以下步骤操作:"
echo "1. 输入 1 (选择 VASP Input Files Generator)"
echo "2. 输入 103 (自动生成 POTCAR，推荐)"
echo "   或输入 104 (手动选择每个元素的赝势类型)"
echo ""
echo "如果选择 104，推荐输入:"
echo "  - Fe: Fe_pv"
echo "  - Si: Si"
echo "  - B: B"
echo ""
echo "按 Enter 开始..."
read

vaspkit

echo ""
echo "=========================================="
if [ -f POTCAR ]; then
    echo "✓ POTCAR 已生成"
    echo "文件大小: $(ls -lh POTCAR | awk '{print $5}')"
    echo ""
    echo "验证 POTCAR:"
    echo "元素数量: $(grep -c 'TITEL' POTCAR)"
    echo "元素列表:"
    grep "TITEL" POTCAR
    echo ""
    echo "复制到目标位置..."
    cp POTCAR ../../outputs/melt_quench_simulation/POTCAR
    echo "✓ 已复制到: outputs/melt_quench_simulation/POTCAR"
else
    echo "✗ POTCAR 未生成"
    echo "请检查 vaspkit 的输出信息"
fi
echo "=========================================="

