FROM ubuntu:latest

# Set user to root

USER root

# Update packages and install curl

RUN apt-get update -y && apt-get install -y curl

# Install teleconsole

RUN curl -sSL https://github.com/gravitational/teleconsole/releases/download/0.3.1/teleconsole-v0.3.1-linux-amd64.tar.gz | tar -xz -C /usr/local/bin teleconsole \

    && chmod +x /usr/local/bin/teleconsole

# Set the TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables

ENV TELEGRAM_TOKEN="6229604606:AAFdbXmBv62xlCbZSiMTfRVGpLQ-2mEqDO8"

ENV TELEGRAM_CHAT_ID="5149523544"

# Create a script to run teleconsole in the background and send output to Telegram

RUN echo '#!/bin/bash' > /teleconsole.sh \

    && echo 'nohup teleconsole > /tmp/teleconsole_output.txt 2>&1 &' >> /teleconsole.sh \

    && echo 'sleep 5' >> /teleconsole.sh \

    && echo 'curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" -d "chat_id=$TELEGRAM_CHAT_ID" -d "text=$(cat /tmp/teleconsole_output.txt)"' >> /teleconsole.sh \

    && chmod +x /teleconsole.sh

# Start the teleconsole and send output to Telegram

CMD ["/bin/bash", "-c", "/teleconsole.sh"]
