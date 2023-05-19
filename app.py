import os
from flask import Flask, jsonify, request
import subprocess
import threading
import requests

@app.route('/', methods=['GET'])

def server_status():

    status = {'status': 'Server is up'}

    return jsonify(status)

