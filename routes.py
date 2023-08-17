from flask import Flask, request, jsonify
from processes import add_links, start_loop, stop_loop
import sys
from logger import logger 

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def handle_post():
    logger.info("Received /add request")
    data = request.json
    status = add_links(data)
    return status

@app.route('/start_search_files')
def start_search_files():
    status = start_loop()
    return jsonify({'status': status})

@app.route('/stop_search_files')
def stop_search_files():
    status = stop_loop()
    return jsonify({'status': status})
    
@app.route('/', methods=['GET'])
def base():
    print("hi")
    print('Hello, world!', file=sys.stdout)
    return 'gg'
