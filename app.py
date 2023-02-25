import json
import subprocess
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def download_videos():
    response = requests.get('https://api.ipify.org')
    ip_address = response.text
    print(ip_address)
    returnObj = [{"ip": ip_address}]

    print('got data')
    data = request.get_json()
    for obj in data:
        link = obj['link']
        destination = obj['destination']
        item = {
            "Link": link,
            "Dest": destination
        }
        returnObj.append(item)
        print('Link:', link, ' dest:', destination)
        subprocess.call(['yt-dlp', '-o', destination + "/%(title)s.%(ext)s", link])
    return jsonify(returnObj)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)