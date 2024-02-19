from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import requests
import shutil

'''
    Copies the code from the specified github page to the local computer
'''

#---------------------------------------------------------#
# Make Sure The Main Program Has Ended Before This Starts #
#---------------------------------------------------------#

# Gets the code from the github page
def get_webpage_text(url=str):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        #url = 'https://github.com/TheTrollGodJr/VOID/blob/main/VOID.pyw'
        driver.get(url)
        element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="read-only-cursor-text-area"]')))
        text = element.text
        driver.quit()
        return text
    except:
        return None

# Writes the new update to the specified filepath
def write_update(filepath, text):
    with open(filepath, 'w') as f:
        f.write(text)

def get_files(path):
    # Initialize an empty list to store files
    files = []
    
    # Get the list of all files and directories
    dir_list = os.listdir(path)
    
    # Iterate through each item in the directory
    for item in dir_list:
        # Construct full path
        item_path = os.path.join(path, item)
        
        # Check if it's a file
        if os.path.isfile(item_path):
            files.append(item_path)
        # If it's a directory, recursively list files in that directory
        elif os.path.isdir(item_path):
            files.extend(get_files(item_path))
    
    '''with open("VOID/filepaths.txt", "w") as f:
        for items in files:
            if "__pycache__" in items or "__init__.py" in items:
                continue
            item = items.replace("\\", "/")
            f.write(f"{item}\n")'''
    return files


def download_update(url=str):
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--headless")

        #prefs = {"download.default_directory": os.path.abspath(__file__).replace('\\', '/').split('/pythonFiles')[0]}
        #chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        while not os.path.exists("VOID/VOID-main.zip"):
            time.sleep(.1)

        driver.quit()
    except:
        return None

def download_file(url, output_file_path):
    response = requests.get(url, stream=True)
    with open(output_file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

if __name__ == "__main__":
    #download_update("https://github.com/TheTrollGodJr/VOID/archive/refs/heads/main.zip")
    download_file("https://github.com/TheTrollGodJr/VOID/archive/refs/heads/main.zip", "VOID/VOID.zip")
    #files = get_files("VOID")

    


    #text = get_webpage_text('https://github.com/TheTrollGodJr/VOID/blob/main/VOID.pyw')
    #write_update("VOID/VOID.pyw", text)