
import speech_recognition as sr
import pyttsx3
import nltk 
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize
import cv2
from random import randrange
from time import time

# Initialize the recognizer
r = sr.Recognizer()

car_tracker = cv2.CascadeClassifier('HaarCascade_carDetection.xml')

def video_car_detection(): 
    #to get video from the webcam (0 means default camera)

    # webcam.set(cv2.CAP_PROP_FPS, 15)
    previous = time()
    delta = 0
    webcam = cv2.VideoCapture('footage.webm')

    while True:
        current = time()
        delta += current - previous
        previous = current
        # read the current frame
        _, frame = webcam.read()

        # Check if 3 (or some other value) seconds passed
        if delta > 1:
            # Operations on image
            # convert to greyscale
            greyscaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect the car based on the pre-trained data.
            car_coordinates = car_tracker.detectMultiScale(greyscaled)

            if not isinstance(car_coordinates, tuple):
                print(car_coordinates)

            # draw rectangles around the pedestrians detected
            for x, y, w, h in car_coordinates:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, randrange(255), 0), 3)
            # Reset the time counter
            delta = 0

        if frame is not None and frame.any():
            cv2.imshow("the image with detected car", frame)
            cv2.waitKey(10)
        else:
            return

        # # to stop the process
        # if key == 81 or key == 113:
        #     webcam.release()
        #     cv2.destroyAllWindows()
        #     return i



def speak_text(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# function to clear up the order as best as possible
def better_order(order):

    order = order.lower()
    order_list = order.split("and")
    size = len(order_list)
    
    for i in range(size):
        text_tokens = word_tokenize(order_list[i])

        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        order_list[i] = ' '.join(tokens_without_sw)
    return order_list


car_count = video_car_detection()
print(car_count)
exit()
while(1):

    try:

        print(1)

        # use the microphone as source for input.
        with sr.Microphone() as source:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source, duration=0.2)

            print("now starting")

            audio_data = r.record(source, duration=10)
            print("Recognizing...")

            # Using google to recognize audio
            MyText = r.recognize_google(audio_data)

            order_list = better_order(MyText)

            print("Did you order ")
            for i in order_list:
                print("\n" + i)
            speak_text(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occured")
