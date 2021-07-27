
import speech_recognition as sr
import pyttsx3
import nltk 
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize

# Initialize the recognizer
r = sr.Recognizer()

def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# function to clear up the order as best as possible
def betterOrder(order):

    order = order.lower()
    order_list = order.split("and")
    size = len(order_list)
    
    for i in range(size):
        text_tokens = word_tokenize(order_list[i])

        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        order_list[i] = ' '.join(tokens_without_sw)
    return order_list



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

            order_list = betterOrder(MyText)

            print("Did you order ")
            for i in order_list:
                print("\n" + i)
            SpeakText(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occured")
