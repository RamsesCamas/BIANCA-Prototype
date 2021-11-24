import speech_recognition as sr
import pyttsx3
import io
import pyglet
from gtts import gTTS

COMMANDS = ['buscar','abrir','sumar','restar','recordar']
GREETINGS = ['hello Bianca', 'Hello Bianca', 'Hola Bianca', 'hola Bianca']
GREETINGS_RAM = ['hola Bianca yo soy Ram']
GREETINGS_VIC = ['hola Bianca yo soy Victor']

pyglet.options["audio"] = ("pulse",)
engine = pyttsx3.init()
recog = sr.Recognizer()
#device_inder = 7 point to system default input device
mic = sr.Microphone(device_index=7)

def speak(words: str, lang: str="es", tld='com.mx'):
    with io.BytesIO() as f:
        gTTS(text=words, lang=lang,tld=tld).write_to_fp(f)
        f.seek(0)
        
        player = pyglet.media.load('_.mp3', file=f).play()
        while player.playing:
            pyglet.app.platform_event_loop.dispatch_posted_events()
            pyglet.clock.tick()

def recog_voice():
    value = None
    with mic as audio_file:
        print('Speak please')
        speak('Habla por favor')
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
    greeting = recog_voice()
    name = ''
    if greeting in GREETINGS_RAM:
        name = 'Ramsés'
    elif greeting in GREETINGS_VIC:
        name = 'Victor'
    elif greeting in GREETINGS:
        speak('¿Quién eres?')
        speak('Dime como te llamas por favor')
        guest_name = recog_voice()
        name = guest_name

    if name == '':
        speak('Tienes que saludar primero, me llamo Bianca')
    else:
        speak(f'Hola {name}')