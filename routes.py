from flask import Flask, request, jsonify
from processes import add_links, start_loop, stop_loop
import sys
import logging
from logger import logger 

app = Flask(__name__)

# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# app.logger.addHandler(handler)
# app.logger.setLevel(logging.INFO)
# logInfo = app.logger.info

@app.route('/add', methods=['POST'])
def handle_post():
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
    
@app.route('/', methods=['POST'])
def base():
    print("hi")
    print('Hello, world!', file=sys.stdout)
    return 'gg'
