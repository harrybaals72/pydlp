import subprocess
import requests 
import json 
import time
import datetime
import pytz
import threading
import os

# set the timezone to Los Angeles
tz = pytz.timezone('America/Los_Angeles')

# global variable to keep track of whether the search_files loop is running
search_files_running = False

def add_links(data):
    now = datetime.datetime.now(tz)
    subprocess.call(['mkdir', '-p', '/home/files/'])
    subprocess.call(['mkdir', '-p', '/home/files/notDone/'])
    filename = "/home/files/notDone/" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    with open(filename, 'w') as f:
        json.dump(data, f)
    
    return 'Success'

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
        dir_path = '/home/files/notDone/'
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
            subprocess.call(['mkdir', '-p', '/home/files/done/'])
            subprocess.call(['mv', '/home/files/notDone/' + first_json_file, '/home/files/done/'])
        else:
            print('No JSON files found in directory')

def start_loop():
    global search_files_running
    if not search_files_running:
        # start the search_files loop if it's not already running
        search_files_running = True
        thread = threading.Thread(target=search_files)
        thread.start()
        return 'started'
    else:
        return 'already running'
    
def stop_loop():
    global search_files_running
    if search_files_running:
        # stop the search_files loop if it's running
        search_files_running = False
        return 'stopped'
    else:
        return 'already stopped'