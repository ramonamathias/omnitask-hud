# omnitask-hud

A sleek, borderless, multi-threaded desktop automation console built with Python and Tkinter. This client serves as a transient HUD (Heads-Up Display) for dispatching background automation tasks to a local orchestration server.

## Key Technical Features

- **Stealth UI Mode:** Toggle the interface anywhere instantly using global system hotkeys (`Ctrl + Q`), hiding it seamlessly when not in use.
- **Non-Blocking Architecture:** Built on top of Python's `threading` library to isolate API requests, preventing UI freezing during asynchronous background tasks.
- **Zero-Admin Overhead:** Utilizes safe, user-level background hooks to bypass restrictive Windows administrative privilege requirements.
- **Auto-Refocus State Machine:** Input fields automatically clear and refocus immediately after a command is sent for rapid, successive workflows.
- **Modern Aesthetics:** A borderless, dark-mode transient design that fits perfectly into a power-user's desktop environment.

## Tech Stack

- **Language:** Python 3
- **UI Framework:** Tkinter
- **Concurrency:** `threading`
- **Hotkey Interceptor:** `pynput`
- **Network Layer:** `requests`

## How It Works

The system takes global system-wide hotkeys via low-level event listeners, toggles the transient HUD into view, accepts user commands, dispatches payloads to a local orchestration server via isolated daemon threads, and resets the input focus state machine instantly to maintain a locked 60 FPS.

## Setup and Installation

### 1. Install dependencies

Run this command in your environment to ensure the required packages are installed:

<pre><code>pip install requests pynput</code></pre>

### 2. Clone the repository

Clone the workspace files into your local desktop environment:

<pre><code>git clone https://github.com/YOUR_USERNAME/omnitask-hud.git</code></pre>

### 3. Launch the HUD application

Execute the main script sequentially to initialize the interface architecture, bind the background event hooks, and begin the automation dispatch loop:

<pre><code>python frontend.py</code></pre>
