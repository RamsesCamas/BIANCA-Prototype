import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init()
recog = sr.Recognizer()
mic = sr.Microphone(device_index=7)
voices = engine.getProperty('voices')
GREETINGS = ['hello Bianca', 'Hello Bianca', 'Hola Bianca', 'hola Bianca']

def recog_voice():
    value = None
    with mic as audio_file:
        print('Speak please')
        audio = recog.listen(audio_file)
        print('Convirtiendo a texto')
        print('Dijiste:')
        try:
            value = recog.recognize_google(audio)
            print(value)
        except Exception as e:
            print('Error: ',e)
    return value

if __name__ == '__main__':
    print('La voz es: ',voices[0].id)
    engine.setProperty('voice', voices[0].id)
    greeting = recog_voice()
    if greeting in GREETINGS:
        saludo = 'Hola Ramsés'
        engine.say('Hola')
        engine.runAndWait()
        engine.stop()
    engine.say('Good morning')
    engine.runAndWait()
    engine.stop()
    
        
    