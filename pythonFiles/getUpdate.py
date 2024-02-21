import requests
import shutil
import zipfile

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
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("VOID")

if __name__ == "__main__":
    download_file("https://github.com/TheTrollGodJr/VOID/archive/refs/heads/main.zip", "VOID/VOID.zip")
    transfer_files()
