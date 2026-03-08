use std::process::Command;
use std::thread;
use std::time::Duration;

fn start_backend() {
    thread::spawn(|| {
        let exe_dir = std::env::current_exe()
            .ok()
            .and_then(|p| p.parent().map(|p| p.to_path_buf()))
            .unwrap_or_default();

        let backend_path = exe_dir.join("backend-dist").join("sau-backend.exe");

        if backend_path.exists() {
            println!("Starting backend service...");
            if let Err(e) = Command::new(&backend_path).spawn() {
                eprintln!("Failed to start backend: {}", e);
            }
        } else {
            eprintln!("Backend executable not found at: {:?}", backend_path);
        }
    });
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    start_backend();

    thread::sleep(Duration::from_secs(3));

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(
            tauri_plugin_log::Builder::default()
                .level(log::LevelFilter::Info)
                .build(),
        )
        .setup(|_app| Ok(()))
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
