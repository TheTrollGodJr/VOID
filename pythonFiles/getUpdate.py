import requests
import shutil
import zipfile
import subprocess
import os

'''
    Downloads the code from the specified github page to the local computer
'''

#---------------------------------------------------------#
# Make Sure The Main Program Has Ended Before This Starts #
#---------------------------------------------------------#

def download_file(url):
    response = requests.get(url, stream=True)
    #
    #   When running in VSCode, it save to the root python file, not the VOID folder.
    #   When running the file normally it saves to the VOID folder properly.
    #
    with open("VOID.zip", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

def transfer_files():
    zip_file_path = "VOID.zip"
    target_folder = os.path.dirname(__file__).split("\\pythonFiles")[0].replace("\\", "/")
    
    # Extract all files from the zip archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(target_folder)
    
    # Move files from VOID-main to VOID folder while maintaining the directory structure
    main_folder = os.path.join(target_folder, 'VOID-main')
    for root, dirs, files in os.walk(main_folder):
        # Determine the corresponding destination folder within VOID
        relative_path = os.path.relpath(root, main_folder)
        destination_folder = os.path.join(target_folder, relative_path)
        
        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)
        
        # Move each file to the destination folder
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.move(source_path, destination_path)
    
    # Remove the VOID-main folder
    shutil.rmtree(main_folder)

def get_packages():
    with open(os.path.dirname(__file__).split("\\pythonFiles")[0].replace("\\", "/") + '/requirements.txt', 'r') as file:
        requirements = file.readlines()
    
    for requirement in requirements:
        subprocess.call(['pip', 'install', requirement.strip()])

def launch_program(program_path, arg, filetype):
    try:
        subprocess.Popen([filetype, program_path] + arg)
    except subprocess.CalledProcessError as e:
        print(f"Error Launching Program: {e}")

if __name__ == "__main__":
    download_file("https://github.com/TheTrollGodJr/VOID/archive/refs/heads/main.zip")
    transfer_files()
    get_packages()
    launch_program("VOID.pyw", [], "pythonw")
