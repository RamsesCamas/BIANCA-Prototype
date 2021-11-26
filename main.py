import speech_recognition as sr
from tkinter import Tk, Label, Button, PhotoImage
import pyttsx3
import io
import pyglet
from gtts import gTTS
import threading

COMMANDS = ['open','calculate','remember', 'Busca en Youtube','Busca en Wikipedia','hablemos']
OPEN_COMMANDS = ['open calculator','open Visual Studio code','open documents folder','open notion']
GREETINGS = ['hello Bianca', 'Hello Bianca', 'Hola Bianca', 'hola Bianca']
GREETINGS_RAM = ['hola Bianca yo soy Ram']
GREETINGS_VIC = ['hola Bianca yo soy Victor']

ENCRYPTED_NAME = 'Alejandro 117'

had_presented = False
user_name = ''

pyglet.options["audio"] = ("pulse",)
engine = pyttsx3.init()
recog = sr.Recognizer()
#device_inder = 7 point to system default input device
mic = sr.Microphone(device_index=6)

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
        speak('Habla por favor')
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

def eval_operation(operation:str):
    result = eval(operation)

def presentation():
    greeting = recog_voice()
    global user_name
    if greeting in GREETINGS_RAM:
        user_name = 'Ramsés'
    elif greeting in GREETINGS_VIC:
        user_name = 'Victor'
    elif greeting in GREETINGS:
        speak('¿Cómo te llamas?')
        user_name = recog_voice()

    if user_name == '':
        speak('Tienes que saludar primero, me llamo Bianca')
    else:
        while user_name is None:
            speak('Dime de nuevo tu nombre')
            user_name = recog_voice()
        if user_name == ENCRYPTED_NAME:
            user_name = 'Ramsés'
        speak(f'Hola {user_name}')
        global had_presented
        had_presented = True


def listen_and_speak():
    print('Ya entramos')
    if had_presented:
        command = recog_voice()
        print(command)
    else:
        print('A presentarse')
        presentation()

class App(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()
    
    def run(self):
        root = Tk()
        root.geometry('1280x720')
        root.title('B.I.A.N.C.A')
        microphone_img = PhotoImage(file=r'imgs/microphone.png')
        microphone_img = microphone_img.subsample(3,3)
        btn_micro = Button(root,text='Click me',image=microphone_img,command=presentation)
        btn_micro.place(x=550,y=450)
        root.mainloop()

if __name__ == '__main__':
    app = App()
    speak('Bienvenido, me llamo Bianca, pulsa el micrófono para hablar')