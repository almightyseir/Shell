FROM ubuntu:latest

# Set user to root
USER root

# Update packages and install necessary dependencies
RUN apt-get update -y && \
    apt-get install -y curl python3 python3-pip tmate python3-venv screen

# Copy the requirements file to the Docker image
COPY requirements.txt /requirements.txt

# Create a virtual environment and install dependencies
RUN python3 -m venv /venv
RUN /venv/bin/python -m pip install --upgrade pip
RUN /venv/bin/pip install -r /requirements.txt

# Copy all necessary files to the Docker image
COPY GeoSpy.session /GeoSpy.session
COPY GeoSpy.session-journal /GeoSpy.session-journal
COPY Geospybot.db /Geospybot.db
COPY app.py /app.py
COPY bot.py /bot.py
COPY db.py /db.py
COPY dbinit.py /dbinit.py
COPY hmm.sh /hmm.sh
COPY huh.sh /huh.sh
COPY log.txt /log.txt
COPY misc.py /misc.py
COPY test.py /test.py

# Copy the DL directory to the Docker image
COPY DL /DL

# Expose the necessary port(s)
EXPOSE 8000

# Create a script to start the bot in a screen session and the Flask app with Gunicorn
RUN echo '#!/bin/bash\n\
source /venv/bin/activate\n\
screen -dmS bot_session python /bot.py\n\
gunicorn --bind 0.0.0.0:8000 app:app\n\
exec "$@"' > /start.sh \
&& chmod +x /start.sh

# Set the command to run the start script
CMD ["/bin/bash", "/start.sh"]
