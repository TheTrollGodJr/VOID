import subprocess
import os
import time

# Starts a different python program
# Set filetype to python for .py files and pythonw for .pyw files
def launch_program(program_path, arg, filetype):
    try:
        subprocess.Popen([filetype, program_path] + arg)
    except subprocess.CalledProcessError as e:
        print(f"Error Launching Program: {e}")

if __name__ == "__main__":
    path = "C:/Users/thetr/Documents/Python/VOID/playAudioFunctions.py"
    launch_program(path, ["https://www.youtube.com/watch?v=q_NbeowU_9s&ab_channel=The8-BitBigBand"], "pythonw")
    time.sleep(10)
    os._exit(1)