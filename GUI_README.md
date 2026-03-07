# Social Auto Upload - GUI 打包说明

## 概述

本项目使用 PySide6 + QWebEngine 将 Social Auto Upload 打包为桌面应用程序。

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 GUI 打包依赖
pip install -r requirements-gui.txt

# 安装 Playwright 浏览器驱动
playwright install chromium
```

### 2. 构建并打包

```bash
# 运行一键构建脚本
build_gui.bat
```

### 3. 运行应用

构建完成后，运行：
```
dist\SocialAutoUpload\SocialAutoUpload.exe
```

## 文件说明

| 文件 | 说明 |
|------|------|
| main_gui.py | GUI 主入口 |
| sau_gui.spec | PyInstaller 配置文件 |
| build_gui.bat | 一键构建脚本 |
| generate_icon.py | 图标生成脚本 |
| gui/ | GUI 模块和资源文件 |
| requirements-gui.txt | GUI 打包依赖 |

## 注意事项

1. 首次打包可能需要 5-10 分钟
2. 打包体积约 100-150 MB
3. 确保已安装 Chrome 浏览器（用于 Playwright）

## 故障排除

如果遇到问题，请检查：
- Python 环境是否正确
- 依赖是否完整安装
- 前端是否成功构建
