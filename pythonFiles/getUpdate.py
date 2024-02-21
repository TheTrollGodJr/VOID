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

def download_file(url, output_file_path):
    response = requests.get(url, stream=True)
    with open(output_file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

def transfer_files():
    zip_file_path = "VOID/VOID.zip"
    target_folder = "VOID"
    
    # Extract all files from the zip archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(target_folder)
    
    # Move files from VOID-main to VOID folder
    main_folder = os.path.join(target_folder, 'VOID-main')
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(target_folder, file)
            shutil.move(source_path, destination_path)
    
    # Remove the VOID-main folder
    shutil.rmtree(main_folder)

def get_packages():
    with open('VOID/requirements.txt', 'r') as file:
        requirements = file.readlines()
    
    for requirement in requirements:
        subprocess.call(['pip', 'install', requirement.strip()])

def launch_program(program_path, arg, filetype):
    try:
        subprocess.Popen([filetype, program_path] + arg)
    except subprocess.CalledProcessError as e:
        print(f"Error Launching Program: {e}")

if __name__ == "__main__":
    download_file("https://github.com/TheTrollGodJr/VOID/archive/refs/heads/main.zip", "VOID/VOID.zip")
    transfer_files()
    get_packages()
    launch_program("VOID/VOID.pyw", [], "pythonw")
