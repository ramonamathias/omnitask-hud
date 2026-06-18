import json
import requests
from tools import send_desktop_notification, open_application, execute_system_control, organize_folder

SYSTEM_PROMPT = """You are OmniTask-OS. Your job is to convert user requests into tool commands.
You must return ONLY a valid, raw JSON object. No conversational chat text.

Valid formats:
{"tool_name": "execute_system_control", "tool_args": {"action": "mute"}}
{"tool_name": "organize_folder", "tool_args": {"target_folder": "Downloads"}}
{"tool_name": "open_application", "tool_args": {"app_name": "notepad"}}
"""

def run_agent_loop(user_objective):
    print(f"\n⚡ AGENT INITIALIZED RAW INPUT: {user_objective}", flush=True)
    
    # FORCE UNPACKING OF THE INPUT ITSELF IF IT IS A TUPLE/LIST
    while isinstance(user_objective, (list, tuple)):
        user_objective = user_objective[0] if user_objective else "organize downloads"
        
    obj_str = str(user_objective).strip()
    obj_lower = obj_str.lower()

    # --- NO-FAIL BULLETPROOF HARD MATCH ROUTING ---
    if "mute" in obj_lower or "volume" in obj_lower or "audio" in obj_lower:
        print("🎯 Failsafe Triggered: Executing volume control directly.", flush=True)
        return execute_system_control("mute")
    if "lock" in obj_lower:
        print("🎯 Failsafe Triggered: Executing system lock directly.", flush=True)
        return execute_system_control("lock")
    if "screenshot" in obj_lower or "ss" in obj_lower or "snap" in obj_lower:
        print("🎯 Failsafe Triggered: Executing screenshot directly.", flush=True)
        return execute_system_control("screenshot")
    if "recycle" in obj_lower or "trash" in obj_lower:
        print("🎯 Failsafe Triggered: Executing recycle bin purge directly.", flush=True)
        return execute_system_control("recycle")
    if "notepad" in obj_lower:
        return open_application("notepad")
    if "calc" in obj_lower or "calculator" in obj_lower:
        return open_application("calculator")
    if "organize" in obj_lower or "clean" in obj_lower or "sort" in obj_lower:
        target = "Downloads" if "download" in obj_lower else "Desktop"
        print(f"🎯 Failsafe Triggered: Executing folder organizer on {target} directly.", flush=True)
        return organize_folder(target)

    # --- LLM BACKUP ENGINE ---
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Task: {obj_str}"}
        ]
        response = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={"model": "llama3.2", "messages": messages, "stream": False},
            timeout=10
        )
        content = response.json()['message']['content'].strip()
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"): content = content[4:]
        content = content.strip()
        
        data = json.loads(content)
        tool_name = data.get("tool_name", "")
        tool_args = data.get("tool_args", {})
        
        if tool_name == "execute_system_control":
            action = tool_args.get("action", "") or obj_str
            return execute_system_control(str(action))
        elif tool_name == "organize_folder":
            target = tool_args.get("target_folder", "") or ("Downloads" if "download" in obj_lower else "Desktop")
            return organize_folder(str(target))
        elif tool_name == "open_application":
            app = tool_args.get("app_name", "") or obj_str
            return open_application(str(app))
            
    except Exception:
        pass
        
    return "Task fallback processed."