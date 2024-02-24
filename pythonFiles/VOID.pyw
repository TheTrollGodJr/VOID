import threading
import numpy as np
import keyboard
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr
import sys

from Functions.checkUpdate import *
from Functions.voiceCommandFunctions import *
from Functions.fileStart import *
#from Functions.getUpdate import *
from Functions.videoFunctions import *

def stop_audio():
    global audioPlaying
    if audioPlaying:
        sd.stop()
        audioPlaying = False

def play_audio_file(file_path):
    #return
    global audioPlaying
    if audioPlaying:
        return
    audioPlaying = True

    data, samplerate = sf.read(file_path)
    try:
        sd.play(data, samplerate=samplerate, device=audioDevice, blocking=True) # Blocking = false means that audio CAN be overriden
        keyboard.add_hotkey('ctrl+shift+s', stop_audio)
        sd.wait()
    except Exception as e:
        print(e)
    finally:
        audioPlaying = False

def recognize_speech_from_mic(recognizer, microphone):
    global listening
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    listening = True
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    listening = False
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def mouse_callback(event, x, y, flags, param):
    global buttonPressed
    if event == cv2.EVENT_LBUTTONDOWN:
        global buttonPressLocation
        buttonPressed = True
        buttonPressLocation = [x,y]
    elif event == cv2.EVENT_LBUTTONUP:
        buttonPressed = False

def video():
    global threadsRunning
    global buttonPressed
    if threadsRunning:
        notifSent = False
        detectionOn = False
        waitCount = 0

        cap = cv2.VideoCapture(0)  # Open webcam, change 0 to the appropriate camera index if needed

        _, prev_frame = cap.read()
        prev_frame = Image.fromarray(cv2.cvtColor(prev_frame, cv2.COLOR_BGR2RGB))

        crop_width = 480
        crop_height = 480

        threshold_percentage = 1  # Adjust this threshold based on your requirements
        consecutive_frames_with_movement = 5  # Number of consecutive frames with movement to trigger detection

        frames_with_movement = 0

        play_audio_file(f"{audioPath}/start.wav")

        while True:
            _, frame = cap.read()

            if detectionOn: 
                if notifSent:
                    if waitCount >= 150:
                        notifSent = False
                        waitCount = 0
                    else:
                        waitCount += 1

                current_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                current_frame = crop_center(current_frame, crop_width, crop_height)

                diff_image = image_difference(prev_frame, current_frame)
                diff_percentage = calculate_difference_percentage(diff_image)

                #print(f"Difference Percentage: {diff_percentage:.2f}%")

                if diff_percentage > threshold_percentage:
                    frames_with_movement += 1
                else:
                    frames_with_movement = 0

                if frames_with_movement >= consecutive_frames_with_movement and notifSent == False:
                    #print("Movement detected")
                    play_audio_file(f"{audioPath}/detection.wav")
                    notifSent = True

                prev_frame = current_frame

            #print(average_brightness(frame))
            if average_brightness(frame) >= 200:
                play_audio_file(f"{audioPath}/welcome.wav")
            elif average_brightness(frame) <= 10:
                #put sound for leaving/turning light off here
                pass
            
            if keyboard.is_pressed('ctrl+shift+~'):
                if detectionOn:
                    detectionOn = False
                    play_audio_file(f"{audioPath}/stop.wav")
                else:
                    detectionOn = True
                    play_audio_file(f"{audioPath}/start.wav")

            if keyboard.is_pressed('ctrl+q'):
                play_audio_file(f"{audioPath}/stop.wav")
                cap.release()
                cv2.destroyAllWindows()
                threadsRunning = False
                break
            
            if listening == True:
                cv2.circle(frame, (30,30), 20, (0,255,0), -1)
            else:
                cv2.circle(frame, (30,30), 20, (255,0,0), -1)

            frame = cv2.putText(frame, word, (25, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

            draw_button(frame, settingsIcon, 600, 10) # Draw settings icon
            #draw_button(frame, )
            cv2.imshow("Survalience", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            cv2.setMouseCallback("Survalience", mouse_callback, settingsIcon)
            if buttonPressed:
                #while buttonPressed:
                #    time.sleep(.1)
                button_height, button_width, _ = settingsIcon.shape
                if 600 <= buttonPressLocation[0] <= 600 + button_width and 10 <= buttonPressLocation[1] <= 10 + button_height:
                    #print("Button clicked!")
                    launch_program("commandTable.py", [], "python")
                    buttonPressed = False

            cv2.waitKey(1)

def audioListening():
    global word
    global audioPlaying
    while True:
        if threadsRunning == False:
            break

        if keyboard.is_pressed("ctrl+q"):
            break

        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        recog = recognize_speech_from_mic(recognizer, microphone)
        #print(recog)

        if recog["error"]:
            print("ERROR: {}".format(recog["error"]))
            
        word = "{}".format(recog["transcription"]).lower()
        #word = recog
        print(word)

        if "void event horizon protocol" in word:
            os.system("shutdown /s /t 1")
            break

        if not audioPlaying:
            for items in commands:
                if items[0] in word:
                    download_audio(f"https://www.youtube.com/watch?v={items[1]}")
                    play_audio_file(f"{voidPath}/audioFiles/downloads/audio.wav")
                    #print("played")

def check_for_update():
    with open(f"{voidPath}/version.txt", "r") as f:
        currentVersion = f.readline() 
    webVersion = get_webpage_text("https://github.com/TheTrollGodJr/VOID/blob/main/VOID/version.txt")[0]
    if webVersion != currentVersion:
        launch_program("getUpdate.py", [], "python")
        sys.exit(1)

if __name__ == "__main__":
    check_for_update()

    commands = get_commands("commands.txt")
    #print(commands)
    voidPath = os.path.dirname(__file__).split("\\pythonFiles")[0].replace("\\", "/")
    settingsIcon = cv2.imread(f"{voidPath}/Images/settingsicon.png", cv2.IMREAD_UNCHANGED)
    
    listening = False
    audioPlaying = False
    threadsRunning = True
    buttonPressed = False
    buttonPressLocation = [0,0] # x,y
    
    #audioPath = 'E:/Kieran Python Codes/MotionDetection/audioFiles'
    audioPath = f'{voidPath}/audioFiles'
    word = ""
    audioDevice = 1

    #'''
    t1 = threading.Thread(target=video)
    t2 = threading.Thread(target=audioListening)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    #'''
