# irys 自动打字任务脚本

## 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install requests
```

## 文件结构

- `bot.py` - 主脚本文件
- `address.txt` - 钱包地址列表
- `proxy.txt` - 代理列表（可选）
- `log.txt` - 运行日志（自动生成）

## 配置说明

配置直接在 `bot.py` 文件中设置：

```python
config = {
    'run_count': 5,  # 每个账号运行次数
    'run_mode': 1  # 运行模式：1=正常，2=快速
}
```

## 使用方法

1. 确保 `address.txt` 文件存在并包含钱包地址（每行一个）
2. 如果需要使用代理，创建 `proxy.txt` 文件并添加代理地址（每行一个）
3. 如需修改配置，直接编辑 `bot.py` 文件中的 `config` 变量
4. 运行脚本：

```bash
python bot.py
```
