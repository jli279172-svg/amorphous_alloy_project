#!/bin/bash
# vaspkit 快速配置脚本

set -e

echo "=========================================="
echo "vaspkit 配置脚本"
echo "=========================================="
echo ""

PROJECT_ROOT="/Users/lijunchen/coding/amorphous_alloy_project"
VASPKIT_DIR="$PROJECT_ROOT/tools/vaspkit.1.5.0"
VASPKIT_BIN="$VASPKIT_DIR/bin/vaspkit"

# 检查 vaspkit 是否存在
if [ ! -f "$VASPKIT_BIN" ]; then
    echo "错误: 未找到 vaspkit 可执行文件"
    echo "请确保 vaspkit 已解压到: $PROJECT_ROOT/tools/"
    exit 1
fi

echo "✓ 找到 vaspkit: $VASPKIT_BIN"
echo ""

# 1. 确保可执行
echo "步骤 1: 设置可执行权限..."
chmod +x "$VASPKIT_BIN"
echo "✓ 完成"
echo ""

# 2. 配置环境变量文件
echo "步骤 2: 配置 ~/.vaspkit 文件..."
if [ -f "$VASPKIT_DIR/how_to_set_environment_variables" ]; then
    if [ ! -f "$HOME/.vaspkit" ]; then
        cp "$VASPKIT_DIR/how_to_set_environment_variables" "$HOME/.vaspkit"
        echo "✓ 配置文件已创建: ~/.vaspkit"
        echo ""
        echo "⚠ 重要: 请编辑 ~/.vaspkit 设置 VASP 赝势库路径"
        echo "   需要设置: PBE_PATH = /path/to/potpaw_PBE"
    else
        echo "~/.vaspkit 已存在，跳过"
    fi
else
    echo "⚠ 未找到配置文件模板"
fi
echo ""

# 3. 添加到 PATH
echo "步骤 3: 添加到 PATH..."
SHELL_RC="$HOME/.zshrc"
if [ -f "$HOME/.bashrc" ] && [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if ! grep -q "vaspkit.1.5.0/bin" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# vaspkit" >> "$SHELL_RC"
    echo "export PATH=\"$VASPKIT_DIR/bin:\$PATH\"" >> "$SHELL_RC"
    echo "✓ 已添加到 $SHELL_RC"
else
    echo "PATH 中已包含 vaspkit"
fi
echo ""

# 4. 测试
echo "步骤 4: 测试 vaspkit..."
export PATH="$VASPKIT_DIR/bin:$PATH"
if vaspkit -v &> /dev/null; then
    echo "✓ vaspkit 可以运行"
    vaspkit -v
else
    echo "⚠ vaspkit 可能需要配置后才能使用"
fi
echo ""

echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 编辑 ~/.vaspkit 设置 VASP 赝势库路径:"
echo "   vi ~/.vaspkit"
echo "   设置: PBE_PATH = /path/to/potpaw_PBE"
echo ""
echo "2. 使 PATH 生效:"
echo "   source $SHELL_RC"
echo "   或重新打开终端"
echo ""
echo "3. 生成 POTCAR:"
echo "   cd $PROJECT_ROOT/data/temp_vaspkit"
echo "   vaspkit"
echo "   选择: 1 -> 103 (自动生成 POTCAR)"
echo ""
echo "=========================================="

