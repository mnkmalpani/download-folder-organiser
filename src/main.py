# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
import sys
import shutil
import os
import argparse
from datetime import datetime
import json

# class MyHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         for filename in os.listdir(folder_to_track):
#             if filename.lower().endswith('.json'):
#                 source_file_name = folder_to_track + '/' + filename
#                 destination_file_name = folder_for_json + '/' + filename
#                 os.rename(source_file_name, destination_file_name)

def check_folder_exists(new_file_folder):
    return os.path.isdir(new_file_folder)


def move_files(folder_to_track, new_file_folder, extention_dict):
    file_extension_found = False
    if not check_folder_exists(new_file_folder):
        os.mkdir(new_file_folder)
    for filename in os.listdir(folder_to_track):
        source_file_name = folder_to_track + '/' + filename
        sub_folder = new_file_folder
        if os.path.isfile(source_file_name):
            name, file_ext = os.path.splitext(source_file_name)
            for folder_name in extention_dict:
                if file_ext[1:] in extention_dict[folder_name]:
                    sub_folder = sub_folder + '/' + folder_name
                    if not check_folder_exists(sub_folder):
                        os.mkdir(sub_folder)
                    shutil.copy(source_file_name, sub_folder)
                    file_extension_found = True
            if not file_extension_found:
                sub_folder = sub_folder + '/others'
                if not check_folder_exists(sub_folder):
                    os.mkdir(sub_folder)
                shutil.copy(source_file_name, sub_folder)

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
        new_file_folder = folder_to_track + '/' + "organised" + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    move_files(folder_to_track=folder_to_track, new_file_folder=new_file_folder, extention_dict=extention_dict)