#this just handles everything to do with extracting info from config file, and reformatting info
import os
import sys
from auto_move import get_screen_size

def get_info_from_config(file_path, target_keyword):

    target_keyword = target_keyword+"="
    try:
    # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read each line in the file
            for line in file:
                # Check if the line contains "number="
                if target_keyword in line:
                    # Extract the number by splitting the line using '=' as the delimiter
                    _, number_str = line.split('=')
                    # Convert the extracted string to an integer
                    number = number_str.strip()
                    # Break out of the loop once the number is found (optional)
                    break

        # Check if a number was successfully extracted
        if number is not None:
            return number
        else:
            print(target_keyword," not found in the config file.")

    except FileNotFoundError:
        print("Config file not found:", file_path)
    except Exception as e:
        print("An error occurred:", str(e))

def set_info_in_config(file_path, key, value):
    try:
        lines = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

        target = key + "="
        found = False
        for idx, line in enumerate(lines):
            if line.strip().startswith(target):
                lines[idx] = f"{key}={value}\n"
                found = True
                break

        if not found:
            # Ensure newline before appending if file doesn't end with one
            if lines and not lines[-1].endswith('\n'):
                lines[-1] = lines[-1] + '\n'
            lines.append(f"{key}={value}\n")

        with open(file_path, 'w') as file:
            file.writelines(lines)
    except Exception as e:
        print("Failed to write config:", str(e))

def get_file_name_w_directory(folder_path):
    files = os.listdir(folder_path)

    if len(files) == 0:
        print("No files found in the folder. Please add at least one photo to the folder.")
        input("Press any key to exit...")
        sys.exit()
    else:
        file_name = files[0]
        print("Using file name: " + str(file_name))
        file_dir = folder_path+"/"+file_name
        print("With Directory: " + file_dir)
        return file_dir

#returns [target coordinates, text_coords]
def change_resolution():

    screen_size = get_screen_size()

    if screen_size[0] == 2560 and screen_size[1] == 1440:
        target_coordinates = [1600,1267]
        text_coords = [400,480,600,560]
        tmp = [target_coordinates, text_coords]
        return tmp
    elif screen_size[0] == 3840 and screen_size[1] == 2160:
        target_coordinates = [2400, 1900]
        text_coords = [600,720,900,840]
    
    elif screen_size[0] == 7680 and screen_size[1] == 4320:
        target_coordinates = [4800,3800]
        text_coords = [1200,1440,1800,1680]
    else:
        target_coordinates = [1200,950]
        text_coords = [300,360,450,420]
        
    tmp = [target_coordinates, text_coords]
    return tmp
