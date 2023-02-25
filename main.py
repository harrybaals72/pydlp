from flask import Flask, request, jsonify
import requests
import datetime
import threading
import os
import json
import time
import subprocess

app = Flask(__name__)

# global variable to keep track of whether the search_files loop is running
search_files_running = False

@app.route('/add', methods=['POST'])
def handle_post():
    data = request.json
    now = datetime.datetime.now()
    filename = "/home/files/" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    with open(filename, 'w') as f:
        json.dump(data, f)
    return 'Data saved successfully!'

def execute_on_file(obj):
    # function to execute on the file
    # replace with your own implementation
    link = obj['link']
    destination = obj['destination']
    print("Link:", obj['link'], "\tDest:", obj['destination'])
    subprocess.call(['yt-dlp', '-o', destination + "/%(title)s.%(ext)s", link])

def search_files():
    global search_files_running
    while search_files_running:
        dir_path = '/home/files/'
        json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]
        # search for json files every 5 seconds
        for i in range(1,6):
            print("Count-A", i)
            time.sleep(1)

        response = requests.get('https://api.ipify.org')
        ip_address = response.text
        print(ip_address)
        print("\nnew loop\n")

        if json_files:
            json_files.sort()
            first_json_file = json_files[0]
            with open(os.path.join(dir_path, first_json_file), 'r') as f:
                data = json.load(f)
                for obj in data:
                    execute_on_file(obj)
    
        else:
            print('No JSON files found in directory')

@app.route('/start_search_files')
def start_search_files():
    global search_files_running
    if not search_files_running:
        # start the search_files loop if it's not already running
        search_files_running = True
        thread = threading.Thread(target=search_files)
        thread.start()
        return jsonify({'status': 'started'})
    else:
        return jsonify({'status': 'already running'})

@app.route('/stop_search_files')
def stop_search_files():
    global search_files_running
    if search_files_running:
        # stop the search_files loop if it's running
        search_files_running = False
        return jsonify({'status': 'stopped'})
    else:
        return jsonify({'status': 'already stopped'})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5353)
