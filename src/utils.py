import os
import shutil


def check_folder_exists(new_file_folder):
    return os.path.isdir(new_file_folder)

def move_files(folder_to_track, new_file_folder, extention_dict):
    file_extension_found, should_create_other = False, False
    if not check_folder_exists(new_file_folder):
        os.mkdir(new_file_folder)
    for filename in os.listdir(folder_to_track):
        source_file_name = folder_to_track + '/' + filename
        sub_folder = new_file_folder
        if os.path.isfile(source_file_name):
            name, file_ext = os.path.splitext(source_file_name)
            for folder_name in extention_dict:
                if file_ext[1:] in extention_dict[folder_name]["extensions"]:
                    if extention_dict[folder_name]["subFolder"] == "false":
                        sub_folder = sub_folder + '/' + folder_name
                        if not check_folder_exists(sub_folder):
                            os.mkdir(sub_folder)
                    else:
                        sub_folder = sub_folder + '/' + folder_name + '/' + file_ext[1:].upper()
                        if not check_folder_exists(sub_folder):
                            os.makedirs(sub_folder)
                    shutil.copy(source_file_name, sub_folder)
                    file_extension_found = True
            if not file_extension_found and should_create_other:
                sub_folder = sub_folder + '/others'
                if not check_folder_exists(sub_folder):
                    os.mkdir(sub_folder)
                shutil.copy(source_file_name, sub_folder)