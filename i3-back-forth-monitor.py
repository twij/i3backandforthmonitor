#!/usr/bin/env python3

import os
import threading
import i3ipc

FIFO_PATH = "/tmp/i3_workspace_switcher_fifo"
last_workspaces = {}
previous_focused_workspace = {}

def log(message):
    print(f"[LOG] {message}")

def on_workspace_focus(i3, event):
    new_workspace_name = event.current.name
    output = event.current.ipc_data['output']
    if output in previous_focused_workspace and previous_focused_workspace[output] != new_workspace_name:
        last_workspaces[output] = previous_focused_workspace[output]
    previous_focused_workspace[output] = new_workspace_name
    log(f"Workspace focus changed to {new_workspace_name} on output {output}")

def setup_event_listeners(i3):
    i3.on("workspace::focus", on_workspace_focus)
    log("Event listeners registered.")

def fifo_read_thread():
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)
    while True:
        with open(FIFO_PATH, 'r') as fifo:
            for line in fifo:
                line = line.strip()
                if line == "switch":
                    process_switch_command()

def process_switch_command():
    try:
        active_output = get_active_output()
        if active_output in last_workspaces:
            i3.command(f"workspace {last_workspaces[active_output]}")
            log(f"Switched to {last_workspaces[active_output]}")
    except Exception as e:
        log(f"Error processing switch command: {e}")

def get_active_output():
    global i3

    focused_workspace_name = None
    for workspace in i3.get_workspaces():
        if workspace.focused:
            focused_workspace_name = workspace.name
            break

    if focused_workspace_name:
        for workspace in i3.get_workspaces():
            if workspace.name == focused_workspace_name:
                return workspace.output
    
    return None

def main():
    global i3
    i3 = i3ipc.Connection()
    setup_event_listeners(i3)

    threading.Thread(target=fifo_read_thread, daemon=True).start()

    log("Script started. Listening for i3 events and FIFO commands...")
    i3.main()

if __name__ == "__main__":
    main()
