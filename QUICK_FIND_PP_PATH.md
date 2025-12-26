# 快速查找 VASP 赝势库路径

## 🎯 快速方法

### 运行查找脚本

```bash
cd /Users/lijunchen/coding/amorphous_alloy_project
python3 scripts/find_vasp_pp.py
```

## 📍 常见路径位置

VASP 赝势库（potpaw_PBE）通常位于：

### macOS:
- `/opt/vasp/potpaw_PBE`
- `/usr/local/vasp/potpaw_PBE`
- `~/vasp/potpaw_PBE`
- `~/POTCAR/PBE`
- `/Applications/vasp/potpaw_PBE`

### Linux/集群:
- `/opt/vasp/potpaw_PBE`
- `/usr/local/vasp/potpaw_PBE`
- `/shared/vasp/potpaw_PBE`
- `~/vasp/potpaw_PBE`

## 🔍 手动查找命令

```bash
# 检查常见路径
for path in /opt/vasp/potpaw_PBE /usr/local/vasp/potpaw_PBE ~/vasp/potpaw_PBE ~/POTCAR/PBE; do
    if [ -f "$path/Fe/POTCAR" ] 2>/dev/null; then
        echo "✓ 找到: $path"
        ls -d "$path"/{Fe,Si,B} 2>/dev/null
        break
    fi
done

# 搜索系统
find /opt /usr/local ~ -maxdepth 3 -type d -name "*potpaw*" 2>/dev/null | head -5
```

## ✅ 验证路径

找到路径后，验证：

```bash
PBE_PATH="/您的路径"
ls $PBE_PATH/Fe/POTCAR  # 应该存在
ls $PBE_PATH/Si/POTCAR  # 应该存在
ls $PBE_PATH/B/POTCAR   # 应该存在
```

## ⚙️ 设置路径

```bash
vi ~/.vaspkit
# 修改: PBE_PATH = /您的实际路径
```

## 📝 如果找不到

1. **从 VASP 官网下载**（需要许可证）:
   - https://www.vasp.at/
   - 下载 potpaw_PBE.tgz
   - 解压到 ~/vasp/potpaw_PBE

2. **联系计算中心**:
   - 询问共享路径

3. **检查环境变量**:
   ```bash
   echo $VASP_PP_PATH
   env | grep -i vasp
   ```

