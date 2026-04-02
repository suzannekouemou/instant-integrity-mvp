// Instant Integrity — Tauri v2 Desktop Wrapper
// No custom IPC commands needed; the frontend communicates
// directly with Supabase and HuggingFace cloud APIs.

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("error while running Instant Integrity");
}
