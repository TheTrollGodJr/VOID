from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# gets the code from a specified github link -- typically the VOID.pyw page
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
        return text.split("\n")
    except:
        return None

'''# Gets text from a file -- typically the text from VOID.pyw
def get_file_text(filepath=str):
    try:
        with open(filepath, 'r') as f:
            text = f.readlines()
        for i in range(len(text)):
            if "\n" in text[i]:
                text[i] = text[i].replace("\n", "")
        return text
    except:
        return None

# Compares the txt from the file that was opened and from the webpage
def compare(filepath, url):
    web_text = get_webpage_text(url)
    file_text = get_file_text(filepath)
    if web_text == None or file_text == None:
        return None
    if web_text == file_text:
        return True
    return False

def does_file_exist(filepath=str):
    try:
        with open(filepath, 'r') as f:
            return True
    except:
        return False
'''
if __name__ == "__main__":
    #if get_webpage_text("https://github.com/TheTrollGodJr/VOID/blob/main/VOID.pyw") == get_file_text(r'C:\Users\thetr\Documents\Python\VOID\VOID.pyw'):
    #    print("True")
    #else:
    #    print("False")

    #print(get_webpage_text("https://github.com/TheTrollGodJr/VOID/blob/main/VOID/version.txt"))
    #def check_for_update():
    with open("VOID/version.txt", "r") as f:
        currentVersion = f.readline() 
    webVersion = get_webpage_text("https://github.com/TheTrollGodJr/VOID/blob/main/VOID/version.txt")[0]
    #if webVersion != currentVersion:
        
