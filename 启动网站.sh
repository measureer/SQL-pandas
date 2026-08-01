#!/bin/bash
# macOS / Linux 启动脚本
cd "$(dirname "$0")"
( sleep 1; open "http://127.0.0.1:8765" 2>/dev/null || xdg-open "http://127.0.0.1:8765" 2>/dev/null ) &
python3 -m http.server 8765 --bind 127.0.0.1
