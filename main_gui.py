#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Social Auto Upload - GUI 主入口
PySide6 + QWebEngine 桌面应用
"""

import sys
import os
import threading
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QUrl, Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent.resolve()
else:
    BASE_DIR = Path(__file__).parent.resolve()

sys.path.insert(0, str(BASE_DIR))
from sau_backend import app


class BackendThread(threading.Thread):
    """Flask 后端线程"""

    def __init__(self, app, port=5409):
        super().__init__(daemon=True)
        self.app = app
        self.port = port

    def run(self):
        self.app.run(host="127.0.0.1", port=self.port, debug=False, use_reloader=False)


class Communicator(QObject):
    """线程间通信"""

    backend_ready = Signal()


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Social Auto Upload - 社交媒体自动上传工具")
        self.setMinimumSize(1200, 700)
        self.resize(1400, 900)

        icon_path = Path(__file__).parent / "gui" / "resources" / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        self.show_loading_page()

        self.start_backend()

        self.setup_system_tray()

        self.health_timer = QTimer()
        self.health_timer.timeout.connect(self.check_backend_health)
        self.health_timer.start(1000)

    def show_loading_page(self):
        """显示启动加载页"""
        loading_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }
                .container {
                    text-align: center;
                    color: white;
                }
                .spinner {
                    width: 50px;
                    height: 50px;
                    border: 4px solid rgba(255,255,255,0.3);
                    border-top: 4px solid white;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 20px;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                h2 { margin: 0 0 10px; }
                p { opacity: 0.8; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="spinner"></div>
                <h2>正在启动服务...</h2>
                <p id="status">初始化后端服务中</p>
            </div>
        </body>
        </html>
        """
        self.browser.setHtml(loading_html, QUrl("about:blank"))

    def start_backend(self):
        """启动 Flask 后端"""
        self.backend_thread = BackendThread(app)
        self.backend_thread.start()

    def check_backend_health(self):
        """检查后端健康状态"""
        import requests

        try:
            response = requests.get("http://127.0.0.1:5409/getAccounts", timeout=1)
            if response.status_code == 200:
                self.health_timer.stop()
                self.load_frontend()
        except:
            pass

    def load_frontend(self):
        """加载前端页面"""
        self.browser.setUrl(QUrl("http://127.0.0.1:5409/"))

    def setup_system_tray(self):
        """设置系统托盘"""
        icon_path = Path(__file__).parent / "gui" / "resources" / "icon.ico"

        if icon_path.exists():
            tray_icon = QIcon(str(icon_path))
        else:
            tray_icon = self.style().standardIcon(self.style().SP_ComputerIcon)

        self.tray = QSystemTrayIcon(tray_icon, self)

        menu = QMenu()

        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.show)
        menu.addAction(show_action)

        hide_action = QAction("隐藏窗口", self)
        hide_action.triggered.connect(self.hide)
        menu.addAction(hide_action)

        menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.close_app)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

    def on_tray_activated(self, reason):
        """托盘图标点击事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()

    def closeEvent(self, event):
        """窗口关闭事件 - 最小化到托盘"""
        event.ignore()
        self.hide()
        self.tray.showMessage(
            "Social Auto Upload",
            "程序已最小化到系统托盘，双击图标可恢复窗口",
            QSystemTrayIcon.Information,
            2000,
        )

    def close_app(self):
        """真正退出应用"""
        self.tray.hide()
        QApplication.quit()


def main():
    """主函数"""
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setApplicationName("Social Auto Upload")
    app.setOrganizationName("SocialAutoUpload")

    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
