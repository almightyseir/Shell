import subprocess
from flask import Flask, jsonify
from threading import Timer

app = Flask(__name__)

# Global variable to store the tmate process
tmate_process = None

@app.route('/', methods=['GET'])
def root_endpoint():
    return 'Server is up'

@app.route('/ssh', methods=['GET'])
def ssh_endpoint():
    global tmate_process

    script = '''
    #!/bin/bash

    BOT_TOKEN="YOUR_BOT_TOKEN"
    CHAT_ID="YOUR_CHAT_ID"

    tmate_output=$(nohup tmate -S /tmp/tmate.sock new-session -d </dev/null >/dev/null 2>&1 &)
    tmate -S /tmp/tmate.sock wait tmate-ready

    sleep 5

    ssh_url=$(tmate -S /tmp/tmate.sock display -p "#{tmate_ssh}")

    echo $ssh_url > /tmp/tmate_ssh_url.txt
    echo "Done"
    '''

    subprocess.run(script, shell=True)

    with open('/tmp/tmate_ssh_url.txt', 'r') as file:
        ssh_url = file.read().strip()

    # Kill tmate process after 3 hours
    if tmate_process:
        tmate_process.kill()

    # Define a timer to kill tmate process after 3 hours
    tmate_process = Timer(3 * 60 * 60, kill_tmate)
    tmate_process.start()

    return jsonify({'ssh_url': ssh_url})

def kill_tmate():
    subprocess.run("pkill tmate", shell=True)

if __name__ == '__main__':
    app.run()

