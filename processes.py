import subprocess
import requests 
import json 
import time
import datetime
import pytz
import threading
import os
from logger import logger  
# from routes import app, logInfo

# set the timezone to Los Angeles
tz = pytz.timezone('America/Los_Angeles')

# global variable to keep track of whether the search_files loop is running
search_files_running = False

def add_links(data):
    logger.info("Data received: {}".format(data))
    now = datetime.datetime.now(tz)
    subprocess.call(['mkdir', '-p', '/home/files/'])
    subprocess.call(['mkdir', '-p', '/home/files/notDone/'])
    filename = "/home/files/notDone/" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return 'Success'

def execute_on_file(obj):
    # function to execute on the file
    # replace with your own implementation
    link = obj['link']
    destination = "/home/downloads/" + obj['destination']
    logger.info("Operating on: Link: {} \tDest: {}".format(link, destination))
    process = subprocess.call(['yt-dlp', '-N', '20','-o', destination + "/%(title)s.%(ext)s", link])

    command = f"yt-dlp -N 20 -o {destination}/'%(title)s.%(ext)s' {link}"
    # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # done = False
    done = True

    # for line in iter(process.stdout.readline, b''):
    #     line = line.decode('utf-8')
    #     logger.info(line)

    #     if '[download] 100% of' in line:
    #         logger.info('Download finish confirmed')
    #         done = True
    #     else:
    #         print(line.strip())
    #     # time.sleep(1)
    
    # for line in iter(process.stderr.readline, b''):
    #     line = line.decode('utf-8')
    #     logger.error(line)
    #     print(line.strip())


    ####################################################

    # while True:
    #     output = process.stdout.readline() + process.stderr.readline()
    #     if output == b'' and process.poll() is not None:
    #         break
    #     if output:
    #         output_str = output.decode('utf-8').strip()  
    #         if '[download] 100% of' in output_str:
    #             logger.info('Download finish confirmed')
    #             done = True
    #         logger.info(output_str)

    # if process.returncode == 0:
    #     print("Download finished successfully!")
    # else:
    #     print(f"Download failed with exit code {process.returncode}")   

    # returncode = process.poll()
    # process.wait()
    # logger.info('Process finished with code {}'.format(returncode))
    return done

def search_files():
    global search_files_running
    while search_files_running:
        dir_path = '/home/files/notDone/'
        json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

        response = requests.get('https://api.ipify.org')
        ip_address = response.text
        logger.info(ip_address)

        if json_files:
            json_files.sort(reverse=True)
            first_json_file = json_files[0]
            doneDir = '/home/files/done/'
            doneFilePath = doneDir + first_json_file

            # Create file that tracks what downloads are done
            subprocess.call(['mkdir', '-p', doneDir])
            subprocess.call(['touch', doneFilePath])

            try:
                with open(doneFilePath, 'r') as f:
                    existingData = json.load(f)
                    logger.info("Read done file first time with contents {}".format(existingData))
            except json.decoder.JSONDecodeError:
                logger.info("Exception, existingData set to []")
                existingData = []

            # Read data from notDone file
            with open(os.path.join(dir_path, first_json_file), 'r') as f:
                addData = json.load(f)

            for obj in addData:
                if obj in existingData:
                    logger.info("{} already done".format(obj))
                else:
                    status = execute_on_file(obj)
                    if (status):
                        write_to_done_file(obj, os.path.join('/home/files/done/', first_json_file))
                        # remove_obj_from_file(obj, os.path.join(dir_path, first_json_file))

            
            subprocess.call(['mv', '/home/files/notDone/' + first_json_file, '/home/files/done/'])
        else:
            print('No JSON files found in directory')
        
        # search for json files every 5 seconds
        for i in range(1,6):
            logger.info("Count-A {}".format(i))
            time.sleep(1)

def write_to_done_file(obj, file):
    logger.info("Beggining write")
    try:
        with open(file, 'r') as f:
            existingData = json.load(f)
            logger.info("Read file with contents {}".format(existingData))
    except json.decoder.JSONDecodeError:
        logger.info("Exception, existingData set to []")
        existingData = []

    if obj not in existingData:
        logger.info("Appending object")
        existingData.append(obj)

    with open(file, 'w') as d:
        json.dump(existingData, d, indent=2)
        logger.info("Dumped")

def remove_obj_from_file(obj, file):
    logger.info("Reading original file")
    with open(file, 'r') as f:
        data = json.load(f)
    
    if obj in data:
        logger.info("{} obj found in data, removing".format(obj))
        data.remove(obj)
        logger.info("New data: {}".format(data))
    
    with open('/home/files/done/modifed.json', 'w') as f:
        logger.info("Dumping")
        json.dump(data, f, indent=2)
    

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