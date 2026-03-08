use std::process::Command;
use std::thread;
use std::time::Duration;
use tauri::Manager;

#[cfg(windows)]
use std::os::windows::process::CommandExt;

#[cfg(windows)]
const CREATE_NO_WINDOW: u32 = 0x08000000;

fn check_port(port: u16) -> bool {
    #[cfg(windows)]
    {
        let mut cmd = Command::new("netstat");
        cmd.args(["-ano"]);
        cmd.creation_flags(CREATE_NO_WINDOW);

        if let Ok(output) = cmd.output() {
            if output.status.success() {
                let stdout = String::from_utf8_lossy(&output.stdout);
                for line in stdout.lines() {
                    if line.contains(&format!(":{}", port)) && line.contains("LISTENING") {
                        return true;
                    }
                }
            }
        }
        false
    }

    #[cfg(not(windows))]
    {
        let output = Command::new("lsof")
            .args(["-ti", &format!(":{}", port)])
            .output();

        output.map(|o| o.status.success()).unwrap_or(false)
    }
}

fn start_backend() {
    let exe_dir = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_default();

    let backend_path = exe_dir.join("backend-dist").join("sau-backend.exe");

    if !backend_path.exists() {
        eprintln!("Backend not found: {:?}", backend_path);
        return;
    }

    println!("Starting backend...");

    let _ = Command::new(&backend_path).current_dir(exe_dir).spawn();
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    println!("Social Auto Upload starting...");

    // 启动后端
    start_backend();

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(
            tauri_plugin_log::Builder::default()
                .level(log::LevelFilter::Info)
                .build(),
        )
        .setup(move |app| {
            let webview = app.get_webview_window("main").unwrap();
            
            let loading_html = r#"<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Social Auto Upload</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; }
        .container { text-align: center; color: white; }
        .spinner { width: 50px; height: 50px; border: 4px solid rgba(255,255,255,0.3); border-top: 4px solid white; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        h2 { margin: 0 0 10px; }
        p { opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h2>正在启动服务...</h2>
        <p id="status">初始化中...</p>
    </div>
    <script>
        async function checkBackend() {
            const statusEl = document.getElementById('status');
            for (let i = 0; i < 60; i++) {
                try {
                    const r = await fetch('http://127.0.0.1:5409/getAccounts', { signal: AbortSignal.timeout(2000) });
                    if (r.ok) { window.location.href = 'http://127.0.0.1:5409/'; return; }
                } catch(e) {}
                await new Promise(r => setTimeout(r, 1000));
                statusEl.textContent = '等待后端启动... (' + (i+1) + '/60)';
            }
            statusEl.innerHTML = '<span style="color:#ff6b6b">后端启动失败</span>';
        }
        checkBackend();
    </script>
</body>
</html>"#;

            let _ = webview.eval(&format!("document.write('{}'); document.close();", loading_html.replace("'", "\\'").replace("\n", "")));
            
            // 异步检测后端就绪
            let webview_clone = webview.clone();
            thread::spawn(move || {
                for _ in 0..60 {
                    thread::sleep(Duration::from_secs(1));
                    if check_port(5409) {
                        let _ = webview_clone.eval("window.location.href = 'http://127.0.0.1:5409/';");
                        return;
                    }
                }
            });
            
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
