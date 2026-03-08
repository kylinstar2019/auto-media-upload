# Social Auto Upload

Social Auto Upload 是一款强大的自动化工具，旨在帮助内容创作者和运营者高效地将视频内容一键发布到多个国内外主流社交媒体平台。

基于 [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) 项目改编，增加了 Tauri 桌面应用打包支持，提供更便捷的使用体验。

## 功能特性

### 支持的平台

**国内平台：**
- 抖音
- 视频号
- Bilibili
- 小红书
- 快手
- 百家号

**国外平台：**
- TikTok

### 核心功能

- 视频一键多平台发布
- 定时发布 (Scheduled Upload)
- Cookie 账号管理
- 桌面应用（绿色版 / 安装版）

## 下载使用

### 方式一：绿色版（推荐）

下载 `SocialAutoUpload-green-win64.zip` 解压后双击 `SocialAutoUpload.exe` 即可使用。

### 方式二：安装版

下载 `SocialAutoUpload_1.0.0_x64-setup.exe` 安装后即可使用。

## 技术栈

| 层级 | 技术 |
|------|------|
| 桌面框架 | Tauri 2 |
| 前端框架 | Vue.js 3 + Vite |
| UI 组件库 | Element Plus |
| 后端框架 | Flask + Python |
| 浏览器自动化 | Playwright |
| 数据库 | SQLite |

## 开发说明

### 环境要求

- Node.js 18+
- Python 3.10+
- Rust (用于 Tauri 开发)
- Visual Studio Build Tools (Windows)

### 本地开发

```bash
# 安装前端依赖
cd sau_frontend
pnpm install

# 启动前端开发
pnpm run dev

# 启动后端
cd ..
python sau_backend.py
```

### 构建桌面应用

```bash
# 构建 Tauri 应用
cd sau_frontend
npm run tauri build
```

产物位置：
- `src-tauri/target/release/bundle/green/SocialAutoUpload-green-win64.zip` (绿色版)
- `src-tauri/target/release/bundle/nsis/SocialAutoUpload_1.0.0_x64-setup.exe` (安装版)

## 项目结构

```
social-auto-upload/
├── sau_backend.py          # Flask 后端入口
├── sau_frontend/           # Vue 3 前端 + Tauri 配置
│   ├── src/               # Vue 源码
│   └── src-tauri/         # Tauri 源码
├── myUtils/                # 核心工具模块
├── uploader/               # 各平台上传器
├── utils/                  # 通用工具
├── db/                     # SQLite 数据库
└── conf.example.py         # 配置文件示例
```

## 鸣谢

- 原始项目：[dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload)
- 前端界面开发者：Edan Lee

## 许可证

[MIT License](LICENSE)