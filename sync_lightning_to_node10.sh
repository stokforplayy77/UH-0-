#!/usr/bin/env bash
while true; do
    if [ -f "/teamspace/studios/this_studio/uh-zero/train.log" ]; then
        curl -s -X POST "http://139.162.21.81/api/append_log" \
            --data-binary "@/teamspace/studios/this_studio/uh-zero/train.log" \
            -H "Content-Type: text/plain" >/dev/null 2>&1
    fi
    sleep 3
done
