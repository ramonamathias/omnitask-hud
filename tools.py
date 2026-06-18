import os
import shutil
import subprocess
import ctypes
import pyautogui
import keyboard
from plyer import notification

def send_desktop_notification(text: str) -> str:
    try:
        if isinstance(text, (list, tuple)):
            text = text[0] if text else ""
        text_str = str(text).strip()
        notification.notify(
            title="OmniTask-OS Alert",
            message=text_str,
            app_name="OmniTask-OS",
            timeout=5
        )
        return "Notification sent successfully."
    except Exception as e:
        return f"Failed to send notification: {str(e)}"

def open_application(app_name: str) -> str:
    try:
        if isinstance(app_name, (list, tuple)):
            app_name = app_name[0] if app_name else ""
        app_name_lower = str(app_name).lower().strip()
        apps = {"notepad": "notepad.exe", "calculator": "calc.exe", "chrome": "chrome.exe"}
        exe = apps.get(app_name_lower)
        if exe:
            subprocess.Popen(exe, shell=True)
            return f"Successfully opened {app_name_lower}."
        else:
            subprocess.Popen(f"{app_name_lower}.exe", shell=True)
            return f"Attempted to open process: {app_name_lower}"
    except Exception as e:
        return f"Failed to open application: {str(e)}"

def execute_system_control(action: str) -> str:
    try:
        if isinstance(action, (list, tuple)):
            action = action[0] if action else ""
        action_lower = str(action).lower().strip()
        if "lock" in action_lower:
            ctypes.windll.user32.LockWorkStation()
            return "System locked successfully."
        elif "mute" in action_lower or "audio" in action_lower or "volume" in action_lower:
            keyboard.send("volume mute")
            return "Windows audio toggled!"
        elif "screenshot" in action_lower or "ss" in action_lower:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            pyautogui.screenshot(os.path.join(desktop_path, "omnitask_screenshot.png"))
            return "Screenshot saved to Desktop!"
        return f"Action {action_lower} completed."
    except Exception as e:
        return f"System action failed: {str(e)}"

def organize_folder(target_folder="Desktop") -> str:
    try:
        while isinstance(target_folder, (list, tuple)):
            target_folder = target_folder[0] if target_folder else "Downloads"
        
        target_str = str(target_folder).strip()
        home = os.path.expanduser("~")
        
        if "desktop" in target_str.lower():
            folder_path = os.path.join(home, "Desktop")
        elif "download" in target_str.lower():
            folder_path = os.path.join(home, "Downloads")
        else:
            folder_path = os.path.join(home, "Downloads")

        if not os.path.exists(folder_path):
            return f"Folder path '{folder_path}' does not exist."

        DIRECTORIES = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Executables": [".exe", ".msi"],
            "Code": [".py", ".js", ".html", ".css", ".json"]
        }

        moved_count = 0
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                continue
                
            # --- THE CRITICAL FIX ---
            # Get the extension string first, THEN turn it lowercase
            split_ext = os.path.splitext(item)[1]
            file_ext = str(split_ext).lower().strip()
            
            for category, extensions in DIRECTORIES.items():
                if file_ext in extensions:
                    dest_dir = os.path.join(folder_path, category)
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.move(item_path, os.path.join(dest_dir, item))
                    moved_count += 1
                    break

        if moved_count > 0:
            return f"Cleaned up {moved_count} files into sorted categories!"
        return "Folder is already clean!"
    except Exception as e:
        return f"File organization failed: {str(e)}"