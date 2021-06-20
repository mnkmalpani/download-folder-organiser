from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import argparse
from datetime import datetime
import json
import time
from utils import *
import platform


class MyHandler(FileSystemEventHandler):

    def __init__(self, folder_to_track, new_file_folder, extention_dict):
        self.folder_to_track = folder_to_track
        self.new_file_folder = new_file_folder
        self.extention_dict = extention_dict
        move_files(folder_to_track=self.folder_to_track, new_file_folder=self.new_file_folder,
                   extention_dict=self.extention_dict)

    def on_modified(self, event):
        move_files(folder_to_track, self.new_file_folder, self.extention_dict)
        #         os.rename(source_file_name, destination_file_name)


if __name__ == "__main__":

    json_obj = open('master_file_type.json')
    extention_dict = json.load(json_obj)

    folder_to_track = ""
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="pass the target folder")
    parser.add_argument("--add", help="Add a folder")
    parser.add_argument("--extensions", help="Pass the list of extension that you want for the new folder")
    arg = parser.parse_args()

    if not arg.target:
        print("Please provide the target folder to be organised")
        sys.exit(1)
    else:
        folder_to_track = arg.target
        if not check_folder_exists(folder_to_track):
            print("Either folder does not exist or it's an invalide folder path, please try again")
            sys.exit(1)
        new_file_folder = folder_to_track + '/' + "organised" + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") \
            if platform.system() != "Windows" \
            else folder_to_track + '\\' + "organised" + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    event_handler = MyHandler(folder_to_track, new_file_folder, extention_dict)
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
