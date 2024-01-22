# i3wm back_and_forth per monitor

A simple script that switches to the last workspace and back but per monitor/output.

In `~/.confg/i3/config`:
```
    exec_always --no-startup-id *filepath*/dist/i3-back-forth-monitor
    bindsym $mod+Tab exec echo "switch" > /tmp/i3_workspace_switcher_fifo
```
