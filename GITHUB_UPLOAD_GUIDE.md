# GitHub 上传指南

项目已经初始化了 Git 仓库并创建了初始提交。现在您可以按照以下步骤将项目上传到 GitHub。

## 步骤 1: 在 GitHub 上创建新仓库

1. 登录您的 GitHub 账户
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `amorphous_alloy_project` (或您喜欢的名称)
   - **Description**: 可选，例如 "VASP melt-quench simulation for amorphous alloys"
   - **Visibility**: 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为我们已经有了）
4. 点击 "Create repository"

## 步骤 2: 添加远程仓库并推送

在项目目录下执行以下命令（将 `YOUR_USERNAME` 替换为您的 GitHub 用户名）：

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/amorphous_alloy_project.git

# 推送代码到 GitHub
git branch -M main
git push -u origin main
```

如果您使用 SSH 方式（需要先配置 SSH key），可以使用：

```bash
git remote add origin git@github.com:YOUR_USERNAME/amorphous_alloy_project.git
git branch -M main
git push -u origin main
```

## 步骤 3: 验证上传

推送成功后，访问 `https://github.com/YOUR_USERNAME/amorphous_alloy_project` 查看您的项目。

## 注意事项

1. **大文件**: 项目包含 `tools/vaspkit.1.5.0/` 和 `VASPKIT_manual/` 目录，这些可能包含大量文件。如果推送时遇到问题，可以考虑：
   - 使用 Git LFS (Large File Storage) 处理大文件
   - 或者将这些目录添加到 `.gitignore` 中（如果不需要版本控制）

2. **认证**: 如果推送时要求输入用户名和密码：
   - 对于 HTTPS，建议使用 Personal Access Token 而不是密码
   - 或者配置 SSH key 使用 SSH 方式

3. **后续更新**: 以后更新代码时，使用：
   ```bash
   git add .
   git commit -m "您的提交信息"
   git push
   ```

## 快速命令（复制粘贴）

```bash
# 替换 YOUR_USERNAME 为您的 GitHub 用户名
cd /Users/lijunchen/coding/amorphous_alloy_project
git remote add origin https://github.com/YOUR_USERNAME/amorphous_alloy_project.git
git branch -M main
git push -u origin main
```

## 如果遇到问题

- **认证失败**: 检查您的 GitHub 用户名和密码/Token
- **仓库已存在**: 如果远程仓库已存在，使用 `git remote set-url origin <URL>` 更新 URL
- **推送被拒绝**: 确保远程仓库是空的，或者先执行 `git pull` 合并远程更改

