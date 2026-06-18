# omnitask-hud 

A sleek, borderless, multi-threaded desktop automation console built with Python and Tkinter. This client serves as a transient HUD (Heads-Up Display) for dispatching background automation tasks to a local orchestration server.

---

##  Features

* **Stealth UI Mode:** Toggle the interface anywhere instantly using global system hotkeys (`Ctrl + Q`), hiding it seamlessly when not in use.
* **Non-Blocking Architecture:** Built on top of Python's `threading` library to isolate API requests, preventing UI freezing during asynchronous background tasks.
* **Zero-Admin Overhead:** Utilizes safe, user-level background hooks to bypass restrictive Windows administrative privilege requirements.
* **Auto-Refocus State Machine:** Input fields automatically clear and refocus immediately after a command is sent for rapid, successive workflows.
* **Modern Aesthetics:** A borderless, dark-mode transient design that fits perfectly into a power-user's desktop environment.

---

##  Architecture & Tech Stack

* **Language:** Python 3
* **UI Framework:** Tkinter (Native lightweight desktop interface rendering)
* **Concurrency:** `threading` (Asynchronous task dispatching)
* **Hotkey Interceptor:** `pynput` (Global system-wide keyboard listener)
* **Network Layer:** `requests` (REST API client handling orchestration server communication)

---

##  Getting Started

### Prerequisites

Ensure you have Python 3 installed on your system. Then, install the required dependencies:

```bash
pip install requests pynput
Installation & Execution
Clone this repository:

Bash
git clone [https://github.com/YOUR_USERNAME/omnitask-hud.git](https://github.com/YOUR_USERNAME/omnitask-hud.git)
cd omnitask-hud
Launch the HUD application:

Bash
python frontend.py
💡 Key Technical Insights for Reviewers
1. Asynchronous Task Dispatching
Traditional Tkinter applications freeze when making network requests because they run on a single main thread. omnitask-hud spins up isolated daemon threads for every outbound payload, ensuring the user interface remains responsive at a locked 60 FPS.

2. Low-Level Event Hooking
By utilizing pynput to listen to global keyboard events, the application hooks into operating system inputs natively. This allows user macros to trigger the HUD even when the application is minimized or unfocused.