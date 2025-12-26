# vaspkit 安装指南 - 快速开始

## 📥 安装步骤

### 步骤 1: 下载 vaspkit

vaspkit 需要从官方网站下载，不是开源项目。

1. **访问官方网站**: https://vaspkit.com/installation.html
2. **下载最新版本**（通常是 `.tar.gz` 或 `.zip` 格式）
3. **选择适合 macOS 的版本**（支持 Mac OS X）

### 步骤 2: 解压到项目目录

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project/tools

# 如果下载的是 .tar.gz
tar -xzf vaspkit.x.x.x.tar.gz

# 或如果是 .zip
unzip vaspkit.x.x.x.zip

# 重命名目录（如果需要）
mv vaspkit.x.x.x vaspkit
```

### 步骤 3: 验证安装

```bash
cd tools/vaspkit

# 检查文件结构
ls -la bin/vaspkit

# 测试运行
./bin/vaspkit -v
```

### 步骤 4: 配置环境变量

```bash
# 复制配置文件模板
cp tools/vaspkit/how_to_set_environment_variable ~/.vaspkit

# 编辑配置文件
vi ~/.vaspkit
```

在 `~/.vaspkit` 中设置：
```
PBE_PATH       /path/to/potpaw_PBE    # 您的 PBE 赝势库路径
POTCAR_TYPE    PBE                    # 赝势类型
RECOMMENDED_POTCAR  .TRUE.            # 使用推荐赝势
```

### 步骤 5: 添加到 PATH

```bash
# 添加到 ~/.zshrc (macOS 默认)
echo 'export PATH="/Users/lijunchen/coding/amorphous_alloy_project/tools/vaspkit/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 测试
which vaspkit
vaspkit -v
```

## 🚀 快速安装脚本

如果您已经下载了 vaspkit 压缩包：

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project

# 将下载的 vaspkit 压缩包放到 tools 目录
# 然后运行：
cd tools
tar -xzf vaspkit*.tar.gz  # 或 unzip vaspkit*.zip
mv vaspkit* vaspkit

# 配置
cp vaspkit/how_to_set_environment_variable ~/.vaspkit
vi ~/.vaspkit  # 设置 PBE_PATH

# 添加到 PATH
echo 'export PATH="'$(pwd)'/vaspkit/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## ✅ 验证安装

```bash
# 检查命令
which vaspkit

# 测试运行
vaspkit -v

# 应该显示版本信息
```

## 📝 下一步

安装完成后，生成 POTCAR：

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project/data/temp_vaspkit
vaspkit
# 选择: 1 -> 103 (自动生成 POTCAR)
```

## 🔗 参考资源

- **官方网站**: https://vaspkit.com/
- **安装页面**: https://vaspkit.com/installation.html
- **视频教程**: 
  - [VASPKIT 安装全记录](https://www.bilibili.com/video/BV11G411f7YM/)
  - [国产之光 VASPKIT 安装教程](https://www.bilibili.com/video/BV1ft4y1b7Gy/)

## ⚠️ 注意事项

1. vaspkit 是二进制文件，**无需编译**
2. 需要配置 `~/.vaspkit` 文件设置赝势库路径
3. 需要 VASP 许可证才能使用 VASP 赝势库
4. macOS 用户可能需要允许运行（系统偏好设置 -> 安全性与隐私）

