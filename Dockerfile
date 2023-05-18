FROM ubuntu:latest

# Set user to root

USER root

# Update packages and install curl

RUN apt-get update -y && apt-get install -y curl

# Install teleconsole

RUN curl -sSL https://github.com/gravitational/teleconsole/releases/download/0.3.1/teleconsole-v0.3.1-linux-amd64.tar.gz | tar -xz -C /usr/local/bin teleconsole \

    && chmod +x /usr/local/bin/teleconsole

# Install tmate

RUN apt-get install -y tmate

# Set the TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables

ENV TELEGRAM_TOKEN="6229604606:AAFdbXmBv62xlCbZSiMTfRVGpLQ-2mEqDO8"

ENV TELEGRAM_CHAT_ID="5149523544"

# Create a script to run tmate in the background and send connection string to Telegram

RUN echo '#!/bin/bash' > /start_tmate.sh \

    && echo 'tmate -S /tmp/tmate.sock new-session -d' >> /start_tmate.sh \

    && echo 'connection_string=$(tmate -S /tmp/tmate.sock display -p "#{tmate_ssh}")' >> /start_tmate.sh \

    && echo 'curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" -d "chat_id=$TELEGRAM_CHAT_ID" -d "text=$connection_string"' >> /start_tmate.sh \

    && chmod +x /start_tmate.sh

# Start tmate and send connection string to Telegram

CMD ["/bin/bash", "-c", "/start_tmate.sh"]
