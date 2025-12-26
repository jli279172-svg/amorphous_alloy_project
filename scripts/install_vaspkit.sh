#!/bin/bash
# vaspkit 安装脚本

set -e  # 遇到错误立即退出

echo "=========================================="
echo "vaspkit 安装脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 项目目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALL_DIR="$PROJECT_ROOT/tools"
VASPKIT_DIR="$INSTALL_DIR/vaspkit"

echo "安装目录: $INSTALL_DIR"
echo ""

# 检查 git
if ! command -v git &> /dev/null; then
    echo -e "${RED}错误: 未找到 git${NC}"
    echo "请先安装 git:"
    echo "  macOS: brew install git"
    echo "  Linux: sudo apt-get install git (Ubuntu/Debian)"
    exit 1
fi

# 检查是否已安装
if [ -d "$VASPKIT_DIR" ] && [ -f "$VASPKIT_DIR/bin/vaspkit" ]; then
    echo -e "${YELLOW}检测到 vaspkit 已安装在: $VASPKIT_DIR${NC}"
    read -p "是否重新安装？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "跳过安装"
        exit 0
    fi
    echo "移除旧版本..."
    rm -rf "$VASPKIT_DIR"
fi

# 创建安装目录
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "=========================================="
echo "步骤 1: 下载 vaspkit"
echo "=========================================="
echo ""

# 方法 1: 从 GitHub 克隆（推荐）
if [ -d "vaspkit" ]; then
    echo "检测到现有 vaspkit 目录，更新..."
    cd vaspkit
    git pull || echo "无法更新，使用现有版本"
    cd ..
else
    echo "从 GitHub 克隆 vaspkit..."
    # 尝试多个可能的仓库地址
    REPOS=(
        "https://github.com/huangwenshi/vaspkit.git"
        "https://github.com/vaspkit/vaspkit.git"
        "https://gitee.com/vaspkit/vaspkit.git"
    )
    
    SUCCESS=false
    for repo in "${REPOS[@]}"; do
        echo "尝试: $repo"
        if git clone "$repo" vaspkit 2>/dev/null; then
            echo -e "${GREEN}✓ 下载成功${NC}"
            SUCCESS=true
            break
        fi
    done
    
    if [ "$SUCCESS" = false ]; then
        echo -e "${YELLOW}从 GitHub 下载失败，尝试其他方法...${NC}"
        echo ""
        echo "vaspkit 可能需要从官方网站下载:"
        echo "1. 访问: https://vaspkit.com/"
        echo "2. 或访问: https://github.com/vaspkit (如果存在)"
        echo "3. 下载最新版本（通常是 .tar.gz 文件）"
        echo "4. 解压到: $INSTALL_DIR"
        echo ""
        echo "或者，如果您已有 vaspkit 文件，可以:"
        echo "1. 将 vaspkit 目录复制到: $INSTALL_DIR"
        echo "2. 确保可执行文件在: $INSTALL_DIR/vaspkit/bin/vaspkit"
        echo ""
        read -p "是否继续手动安装？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# 检查下载是否成功
if [ ! -d "vaspkit" ]; then
    echo -e "${RED}错误: vaspkit 目录不存在${NC}"
    exit 1
fi

cd vaspkit

# 查找可执行文件
VASPKIT_BIN=""
if [ -f "bin/vaspkit" ]; then
    VASPKIT_BIN="bin/vaspkit"
elif [ -f "vaspkit" ]; then
    VASPKIT_BIN="vaspkit"
else
    echo -e "${YELLOW}警告: 未找到 vaspkit 可执行文件${NC}"
    echo "可能需要编译，请查看 vaspkit 文档"
fi

if [ -n "$VASPKIT_BIN" ] && [ -f "$VASPKIT_BIN" ]; then
    # 确保可执行
    chmod +x "$VASPKIT_BIN"
    echo -e "${GREEN}✓ 找到 vaspkit 可执行文件: $VASPKIT_BIN${NC}"
fi

echo ""
echo "=========================================="
echo "步骤 2: 配置环境变量"
echo "=========================================="
echo ""

# 检查配置文件模板
CONFIG_TEMPLATE=""
if [ -f "how_to_set_environment_variable" ]; then
    CONFIG_TEMPLATE="how_to_set_environment_variable"
elif [ -f "examples/how_to_set_environment_variable" ]; then
    CONFIG_TEMPLATE="examples/how_to_set_environment_variable"
fi

if [ -n "$CONFIG_TEMPLATE" ]; then
    echo "找到配置文件模板: $CONFIG_TEMPLATE"
    
    if [ ! -f "$HOME/.vaspkit" ]; then
        echo "复制配置文件到 ~/.vaspkit"
        cp "$CONFIG_TEMPLATE" "$HOME/.vaspkit"
        echo -e "${GREEN}✓ 配置文件已创建: ~/.vaspkit${NC}"
        echo ""
        echo -e "${YELLOW}重要: 请编辑 ~/.vaspkit 设置 VASP 赝势库路径${NC}"
        echo "  需要设置: PBE_PATH = /path/to/potpaw_PBE"
    else
        echo -e "${YELLOW}~/.vaspkit 已存在，跳过${NC}"
        echo "如需更新，请手动编辑: ~/.vaspkit"
    fi
else
    echo -e "${YELLOW}警告: 未找到配置文件模板${NC}"
fi

echo ""
echo "=========================================="
echo "步骤 3: 添加到 PATH（可选）"
echo "=========================================="
echo ""

VASPKIT_BIN_PATH="$VASPKIT_DIR/bin"
SHELL_RC=""

# 检测 shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
    if [ ! -f "$SHELL_RC" ]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
else
    SHELL_RC="$HOME/.profile"
fi

if [ -f "$SHELL_RC" ]; then
    if ! grep -q "vaspkit/bin" "$SHELL_RC"; then
        echo "添加到 PATH: $SHELL_RC"
        echo "" >> "$SHELL_RC"
        echo "# vaspkit" >> "$SHELL_RC"
        echo "export PATH=\"$VASPKIT_BIN_PATH:\$PATH\"" >> "$SHELL_RC"
        echo -e "${GREEN}✓ 已添加到 PATH${NC}"
        echo ""
        echo "请运行以下命令使配置生效:"
        echo "  source $SHELL_RC"
        echo "  或重新打开终端"
    else
        echo -e "${YELLOW}PATH 中已包含 vaspkit${NC}"
    fi
else
    echo -e "${YELLOW}未找到 shell 配置文件，请手动添加:${NC}"
    echo "  export PATH=\"$VASPKIT_BIN_PATH:\$PATH\""
fi

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "vaspkit 安装位置: $VASPKIT_DIR"
echo ""

# 测试 vaspkit
if [ -f "$VASPKIT_BIN_PATH/vaspkit" ]; then
    echo "测试 vaspkit..."
    if "$VASPKIT_BIN_PATH/vaspkit" -v &> /dev/null; then
        echo -e "${GREEN}✓ vaspkit 可以运行${NC}"
        "$VASPKIT_BIN_PATH/vaspkit" -v
    else
        echo -e "${YELLOW}⚠ vaspkit 可能需要配置后才能使用${NC}"
    fi
fi

echo ""
echo "=========================================="
echo "下一步操作"
echo "=========================================="
echo ""
echo "1. 配置 VASP 赝势库路径:"
echo "   vi ~/.vaspkit"
echo "   设置: PBE_PATH = /path/to/potpaw_PBE"
echo ""
echo "2. 使 PATH 生效:"
echo "   source $SHELL_RC"
echo ""
echo "3. 测试 vaspkit:"
echo "   vaspkit -v"
echo ""
echo "4. 生成 POTCAR:"
echo "   cd $PROJECT_ROOT/data/temp_vaspkit"
echo "   vaspkit"
echo "   选择: 1 -> 103 (自动生成 POTCAR)"
echo ""
echo "=========================================="

