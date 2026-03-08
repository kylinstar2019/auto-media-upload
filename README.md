# Social Auto Upload - Desktop App

基于 Tauri 2 打包的桌面应用程序，提供社交媒体视频一键多平台发布功能。

## 下载使用

### 方式一：绿色版（推荐）

下载 `SocialAutoUpload-green-win64.zip` 解压后双击 `SocialAutoUpload.exe` 即可使用。

### 方式二：安装版

下载 `SocialAutoUpload_1.0.0_x64-setup.exe` 安装后即可使用。

## 功能特性

- 视频一键多平台发布（抖音、视频号，Bilibili，小红书、快手、百家号、TikTok）
- 定时发布
- Cookie 账号管理
- 桌面应用（绿色版 / 安装版）

## 技术栈

| 层级 | 技术 |
|------|------|
| 桌面框架 | Tauri 2 |
| 前端框架 | Vue.js 3 + Vite |
| UI 组件库 | Element Plus |
| 后端框架 | Flask + Python (打包) |
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
# 安装依赖
pnpm install

# 启动前端开发
pnpm run dev

# 启动后端（开发模式）
cd ..
python sau_backend.py
```

### 构建桌面应用

```bash
# 构建应用
pnpm tauri build
```

产物位置：
- `src-tauri/target/release/bundle/green/` (绿色版)
- `src-tauri/target/release/bundle/nsis/` (安装版)

## 项目结构

```
auto-media-upload/
├── src/                    # Vue 源码
├── src-tauri/             # Tauri 源码
│   ├── src/              # Rust 源码
│   └── tauri.conf.json   # Tauri 配置
├── dist/                  # 前端构建产物
├── backend-dist/          # 后端打包产物
├── conf.py               # 配置文件
└── README.md             # 项目说明
```

## 许可证

MIT License
