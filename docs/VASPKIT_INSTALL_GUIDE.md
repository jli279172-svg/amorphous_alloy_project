# vaspkit 安装指南

## 系统信息

- **操作系统**: macOS (Darwin arm64)
- **Git**: 已安装 ✓

## 安装方法

### 方法 1: 从官方网站下载（推荐）

vaspkit 是二进制文件，无需编译，直接下载即可使用。

#### 步骤 1: 下载 vaspkit

1. 访问 vaspkit 官方网站: https://vaspkit.com/
2. 或访问 GitHub: https://github.com/vaspkit (如果可用)
3. 下载最新版本的压缩包（通常是 `.tar.gz` 格式）

#### 步骤 2: 解压到项目目录

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project/tools

# 如果下载的是 .tar.gz 文件
tar -xzf vaspkit.x.x.x.tar.gz

# 或如果下载的是 .zip 文件
unzip vaspkit.x.x.x.zip
```

#### 步骤 3: 验证安装

```bash
cd tools/vaspkit
ls -la bin/vaspkit
# 应该看到 vaspkit 可执行文件

# 测试运行
./bin/vaspkit -v
# 或
bin/vaspkit -v
```

### 方法 2: 使用我们的安装脚本

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project
./scripts/install_vaspkit.sh
```

如果自动下载失败，脚本会提示手动安装步骤。

### 方法 3: 从已有文件安装

如果您已经有 vaspkit 文件：

```bash
# 1. 复制 vaspkit 目录到项目
cp -r /path/to/vaspkit /Users/lijunchen/coding/amorphous_alloy_project/tools/

# 2. 确保可执行
chmod +x tools/vaspkit/bin/vaspkit

# 3. 测试
tools/vaspkit/bin/vaspkit -v
```

## 配置 vaspkit

### 步骤 1: 创建配置文件

```bash
# 复制配置文件模板
cp tools/vaspkit/how_to_set_environment_variable ~/.vaspkit

# 编辑配置文件
vi ~/.vaspkit
```

### 步骤 2: 设置 VASP 赝势库路径

在 `~/.vaspkit` 文件中设置：

```
PBE_PATH       /path/to/potpaw_PBE    # 您的 PBE 赝势库路径
POTCAR_TYPE    PBE                    # 赝势类型
RECOMMENDED_POTCAR  .TRUE.            # 使用推荐赝势
```

**重要**: 将 `/path/to/potpaw_PBE` 替换为您实际的 VASP 赝势库路径。

## 添加到 PATH（可选）

### 方法 1: 临时添加（当前终端会话）

```bash
export PATH="/Users/lijunchen/coding/amorphous_alloy_project/tools/vaspkit/bin:$PATH"
```

### 方法 2: 永久添加（推荐）

编辑您的 shell 配置文件：

```bash
# 对于 zsh (macOS 默认)
echo 'export PATH="/Users/lijunchen/coding/amorphous_alloy_project/tools/vaspkit/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 或对于 bash
echo 'export PATH="/Users/lijunchen/coding/amorphous_alloy_project/tools/vaspkit/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 方法 3: 创建符号链接

```bash
# 创建符号链接到 /usr/local/bin（需要管理员权限）
sudo ln -s /Users/lijunchen/coding/amorphous_alloy_project/tools/vaspkit/bin/vaspkit /usr/local/bin/vaspkit

# 或创建到用户本地 bin
mkdir -p ~/bin
ln -s /Users/lijunchen/coding/amorphous_alloy_project/tools/vaspkit/bin/vaspkit ~/bin/vaspkit
export PATH="$HOME/bin:$PATH"
```

## 验证安装

```bash
# 检查 vaspkit 是否在 PATH 中
which vaspkit

# 测试运行
vaspkit -v

# 或使用完整路径
/Users/lijunchen/coding/amorphous_alloy_project/tools/vaspkit/bin/vaspkit -v
```

## 使用 vaspkit 生成 POTCAR

安装并配置完成后：

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project/data/temp_vaspkit

# 运行 vaspkit
vaspkit

# 在菜单中选择:
# 1 -> 103 (自动生成 POTCAR)
# 或 1 -> 104 (手动选择: Fe_pv, Si, B)
```

## 常见问题

### Q1: 找不到 vaspkit 命令

**解决方案**:
- 检查 PATH 设置
- 使用完整路径: `tools/vaspkit/bin/vaspkit`
- 或创建符号链接

### Q2: vaspkit 无法找到赝势库

**解决方案**:
- 检查 `~/.vaspkit` 配置文件
- 确认 `PBE_PATH` 设置正确
- 确认路径存在且可访问

### Q3: 权限错误

**解决方案**:
```bash
chmod +x tools/vaspkit/bin/vaspkit
```

## 参考资源

- vaspkit 官方网站: https://vaspkit.com/
- vaspkit 文档: https://vaspkit.com/installation.html
- 项目中的手册: `VASPKIT_manual/`

## 下一步

安装完成后，继续生成 POTCAR 文件：

1. 配置 `~/.vaspkit` 文件
2. 运行 vaspkit 生成 POTCAR
3. 验证 POTCAR 文件
4. 开始 VASP 计算

