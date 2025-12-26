#!/bin/bash
# 完整的 POTCAR 生成流程脚本

set -e

PROJECT_ROOT="/Users/lijunchen/coding/amorphous_alloy_project"
VASPKIT_BIN="$PROJECT_ROOT/tools/vaspkit.1.5.0/bin/vaspkit"
TEMP_DIR="$PROJECT_ROOT/data/temp_vaspkit"
OUTPUT_DIR="$PROJECT_ROOT/outputs/melt_quench_simulation"
CONFIG_FILE="$HOME/.vaspkit"

echo "=========================================="
echo "POTCAR 生成完整流程"
echo "=========================================="
echo ""

# 1. 检查 vaspkit
echo "步骤 1: 检查 vaspkit..."
if [ ! -f "$VASPKIT_BIN" ]; then
    echo "✗ 错误: 未找到 vaspkit"
    exit 1
fi
echo "✓ vaspkit 已找到"
echo ""

# 2. 检查 POSCAR
echo "步骤 2: 检查 POSCAR 文件..."
if [ ! -f "$TEMP_DIR/POSCAR" ]; then
    echo "复制 POSCAR 文件..."
    mkdir -p "$TEMP_DIR"
    cp "$PROJECT_ROOT/outputs/POSCAR_initial" "$TEMP_DIR/POSCAR"
fi
echo "✓ POSCAR 文件已准备"
head -7 "$TEMP_DIR/POSCAR" | tail -2
echo ""

# 3. 检查并设置 PBE_PATH
echo "步骤 3: 检查 VASP 赝势库配置..."
CURRENT_PBE_PATH=$(grep "^PBE_PATH" "$CONFIG_FILE" 2>/dev/null | awk -F'=' '{print $2}' | xargs || echo "")

if [ -z "$CURRENT_PBE_PATH" ] || [ "$CURRENT_PBE_PATH" = "~/POTCAR/PBE" ]; then
    echo "⚠ PBE_PATH 未设置或使用默认值"
    echo ""
    echo "正在查找 VASP 赝势库..."
    
    # 检查常见路径
    FOUND_PATH=""
    for path in "/opt/vasp/potpaw_PBE" "/usr/local/vasp/potpaw_PBE" "$HOME/vasp/potpaw_PBE" "$HOME/POTCAR/PBE" "/shared/vasp/potpaw_PBE"; do
        if [ -d "$path" ] && [ -f "$path/Fe/POTCAR" ] 2>/dev/null; then
            FOUND_PATH="$path"
            echo "✓ 找到 VASP 赝势库: $path"
            break
        fi
    done
    
    if [ -n "$FOUND_PATH" ]; then
        echo ""
        read -p "是否使用此路径？(Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            # 更新配置文件
            if [ -f "$CONFIG_FILE" ]; then
                # 使用 sed 更新 PBE_PATH
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    # macOS
                    sed -i '' "s|^PBE_PATH.*|PBE_PATH                      =     $FOUND_PATH|" "$CONFIG_FILE"
                else
                    # Linux
                    sed -i "s|^PBE_PATH.*|PBE_PATH                      =     $FOUND_PATH|" "$CONFIG_FILE"
                fi
                echo "✓ 已更新 ~/.vaspkit 中的 PBE_PATH"
            fi
            PBE_PATH="$FOUND_PATH"
        else
            echo "请手动设置 PBE_PATH"
            echo "编辑: $CONFIG_FILE"
            exit 1
        fi
    else
        echo "✗ 未找到 VASP 赝势库"
        echo ""
        echo "请手动设置 PBE_PATH:"
        echo "1. 编辑配置文件: vi $CONFIG_FILE"
        echo "2. 找到 PBE_PATH 行，设置为您的实际路径"
        echo "   例如: PBE_PATH = /path/to/potpaw_PBE"
        echo ""
        read -p "请输入您的 VASP 赝势库路径（或按 Enter 退出）: " MANUAL_PATH
        if [ -n "$MANUAL_PATH" ]; then
            if [ -d "$MANUAL_PATH" ] && [ -f "$MANUAL_PATH/Fe/POTCAR" ] 2>/dev/null; then
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    sed -i '' "s|^PBE_PATH.*|PBE_PATH                      =     $MANUAL_PATH|" "$CONFIG_FILE"
                else
                    sed -i "s|^PBE_PATH.*|PBE_PATH                      =     $MANUAL_PATH|" "$CONFIG_FILE"
                fi
                echo "✓ 已更新配置"
                PBE_PATH="$MANUAL_PATH"
            else
                echo "✗ 路径无效或不存在 Fe/POTCAR"
                exit 1
            fi
        else
            exit 1
        fi
    fi
else
    PBE_PATH="$CURRENT_PBE_PATH"
    # 展开 ~
    PBE_PATH="${PBE_PATH/#\~/$HOME}"
    echo "✓ 使用配置的路径: $PBE_PATH"
    
    # 验证路径
    if [ ! -d "$PBE_PATH" ] || [ ! -f "$PBE_PATH/Fe/POTCAR" ] 2>/dev/null; then
        echo "⚠ 警告: 配置的路径可能无效"
        echo "  路径: $PBE_PATH"
        echo "  请检查路径是否正确"
    fi
fi
echo ""

# 4. 切换到工作目录
cd "$TEMP_DIR"
echo "步骤 4: 准备生成 POTCAR..."
echo "工作目录: $(pwd)"
echo ""

# 5. 运行 vaspkit
echo "=========================================="
echo "运行 vaspkit 生成 POTCAR"
echo "=========================================="
echo ""
echo "vaspkit 是交互式程序，请按照以下步骤操作:"
echo ""
echo "1. 输入: 1"
echo "   (选择 VASP Input Files Generator)"
echo ""
echo "2. 输入: 103"
echo "   (自动生成 POTCAR，使用推荐赝势)"
echo "   或输入: 104 (手动选择每个元素的赝势类型)"
echo ""
echo "如果选择 104，推荐输入:"
echo "  - Fe: Fe_pv (包含 p 价电子，适合金属)"
echo "  - Si: Si (标准版本)"
echo "  - B: B (标准版本)"
echo ""
echo "按 Enter 开始运行 vaspkit..."
read

# 运行 vaspkit
"$VASPKIT_BIN"

# 6. 检查结果
echo ""
echo "=========================================="
echo "检查生成的 POTCAR"
echo "=========================================="

if [ -f "POTCAR" ] && [ -s "POTCAR" ]; then
    echo "✓ POTCAR 文件已生成"
    echo ""
    
    # 文件信息
    echo "文件信息:"
    ls -lh POTCAR
    echo ""
    
    # 元素检查
    ELEMENT_COUNT=$(grep -c "TITEL" POTCAR 2>/dev/null || echo "0")
    echo "元素检查:"
    echo "  元素数量: $ELEMENT_COUNT"
    
    if [ "$ELEMENT_COUNT" -eq "3" ]; then
        echo "  元素列表:"
        grep "TITEL" POTCAR | sed 's/.*TITEL.*= PAW //' | sed 's/ .*//' | nl
        echo ""
        
        # 验证元素顺序
        POSCAR_ELEMENTS=$(head -6 POSCAR | tail -1)
        POTCAR_ELEMENTS=$(grep "TITEL" POTCAR | sed 's/.*TITEL.*= PAW //' | sed 's/ .*//' | tr '\n' ' ' | xargs)
        
        echo "元素顺序验证:"
        echo "  POSCAR: $POSCAR_ELEMENTS"
        echo "  POTCAR: $POTCAR_ELEMENTS"
        echo ""
        
        if [ "$POSCAR_ELEMENTS" = "$POTCAR_ELEMENTS" ]; then
            echo "✓ 元素顺序匹配！"
        else
            echo "⚠ 警告: 元素顺序不匹配"
            echo "  这可能导致 VASP 计算错误"
        fi
        
        # 复制到目标位置
        echo ""
        echo "复制 POTCAR 到目标位置..."
        mkdir -p "$OUTPUT_DIR"
        cp POTCAR "$OUTPUT_DIR/POTCAR"
        echo "✓ 已复制到: $OUTPUT_DIR/POTCAR"
        
        # 最终验证
        echo ""
        echo "=========================================="
        echo "✓ POTCAR 文件生成完成！"
        echo "=========================================="
        echo ""
        echo "文件位置: $OUTPUT_DIR/POTCAR"
        echo "文件大小: $(ls -lh "$OUTPUT_DIR/POTCAR" | awk '{print $5}')"
        echo ""
        echo "验证命令:"
        echo "  cd $OUTPUT_DIR"
        echo "  grep -c 'TITEL' POTCAR  # 应该输出 3"
        echo "  grep 'TITEL' POTCAR     # 查看元素列表"
        echo ""
        echo "下一步: 可以开始运行 VASP 计算"
        echo "  cd $OUTPUT_DIR"
        echo "  ./run_all_stages.sh"
        
    else
        echo "✗ 错误: POTCAR 中元素数量不是 3 (当前: $ELEMENT_COUNT)"
        echo "请检查生成过程"
        exit 1
    fi
else
    echo "✗ POTCAR 文件未生成或为空"
    echo ""
    echo "可能的原因:"
    echo "1. PBE_PATH 路径不正确"
    echo "2. 赝势库中缺少某些元素"
    echo "3. vaspkit 运行出错"
    echo ""
    echo "请检查:"
    echo "  - ~/.vaspkit 中的 PBE_PATH 设置"
    echo "  - $PBE_PATH 目录是否存在"
    echo "  - $PBE_PATH/Fe, $PBE_PATH/Si, $PBE_PATH/B 是否存在"
    exit 1
fi

