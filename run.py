import subprocess
import time
import sys
import shutil
import os

# Clean out stale pycache modules entirely to stop Windows caching bugs
print("🧹 Purging old Python compilation cache files...")
for rootdir, dirs, files in os.walk('.', topdown=False):
    for name in dirs:
        if name == '__pycache__':
            shutil.rmtree(os.path.join(rootdir, name), ignore_errors=True)

print("🚀 Starting OmniTask-OS Backend Server...")
backend_process = subprocess.Popen(
    [sys.executable, "main.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

time.sleep(2.5)

print("⚡ Launching Graphical User Interface...")
try:
    subprocess.run([sys.executable, "frontend.py"])
finally:
    print(" Shutting down backend services cleanly...")
    backend_process.terminate()