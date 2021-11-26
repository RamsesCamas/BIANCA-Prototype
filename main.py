import speech_recognition as sr
from tkinter import Tk, Label, Button, PhotoImage,font
import pyttsx3
import io
import pyglet
from gtts import gTTS
import threading
from dfa import DFA
import time
import os
import wikipedia
import re
import requests

automata_commands = {
    'S': {'o', 'p', 'e', 'n', ' ', 'c', 'a', 'l', 'u', 't', 'r', 'm', 'b', 'B', 's', 'Y', 'W', 'i', 'k', 'd', 'h'},
    'Q': {'Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 
            'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 
            'Q29', 'Q30', 'Q31', 'Q32', 'Q33', 'Q34', 'Q35', 'Q36', 'Q37', 'Q38', 'Q39', 'Q40', 'Q41', 'Q42', 
            'Q43', 'Q44', 'Q45', 'Q46', 'Q47', 'Q48', 'Q49', 'Q50', 'Q51', 'Q52', 'Q53', 'Q54'
            },
    'D': {('Q0','o'):'Q1',('Q0','c'):'Q5',('Q0','r'):'Q14',('Q0','h'):'Q22',('Q0','B'):'Q30',('Q1','p'):'Q2',('Q2','e'):'Q3',('Q3','n'):'Q4',('Q5','a'):'Q6',('Q6','l'):'Q7',
    ('Q7','c'):'Q8',('Q8','u'):'Q9',('Q9','l'):'Q10',('Q10','a'):'Q11',('Q11','t'):'Q12',('Q12','e'):'Q13',('Q14','e'):'Q15',
    ('Q15','m'):'Q16',('Q16','e'):'Q17',('Q17','m'):'Q18',('Q18','b'):'Q19',('Q19','e'):'Q20',('Q20','r'):'Q21',
    ('Q22','a'):'Q23',('Q23','b'):'Q24',('Q24','l'):'Q25',('Q25','e'):'Q26',('Q26','m'):'Q27',('Q27','o'):'Q28',('Q28','s'):'Q29',
    ('Q30','u'):'Q31',('Q31','s'):'Q32',('Q32','c'):'Q33',('Q33','a'):'Q34',('Q34',' '):'Q35',('Q35','e'):'Q36',('Q36','n'):'Q37',('Q37',' '):'Q38',('Q38','Y'):'Q39',('Q38','W'):'Q46',('Q39','o'):'Q40',('Q40','u'):'Q41',('Q41','t'):'Q42',('Q42','u'):'Q43',('Q43','b'):'Q44',('Q44','e'):'Q45',('Q46','i'):'Q47',('Q47','k'):'Q48',('Q48','i'):'Q49',('Q49','p'):'Q50',('Q50','e'):'Q51',('Q51','d'):'Q52',('Q52','i'):'Q53',('Q53','a'):'Q54'},
    'q0': 'Q0',
    'F': {'Q4','Q13','Q21','Q29','Q45','Q54'}
}

COMMANDS = ['open','calculate','remember', 'Busca en Youtube','Busca en Wikipedia','hablemos']
OPEN_COMMANDS = ['calculator','Visual Studio code','documents folder','notion','download folder','browser','Spotify']
GREETINGS = ['hello Bianca', 'Hello Bianca', 'Hola Bianca', 'hola Bianca']
GREETINGS_RAM = ['hola Bianca yo soy Ram']
GREETINGS_VIC = ['hola Bianca yo soy Victor']

ENCRYPTED_NAME = 'Alejandro 117'

REGEX_TITLE = r'<title>.* - YouTube</title>'

REGEX_DATE = r'"dateText":\{"simpleText":".{12}"\}'

REGEX_CHANNEL = r'<link itemprop="name" content="[^<]*>'


had_presented = False
user_name = ''

pyglet.options["audio"] = ("pulse",)
engine = pyttsx3.init()
recog = sr.Recognizer()
#device_inder = 7 point to system default input device
mic = sr.Microphone(device_index=6)

def is_valid_command(command):
    my_dfa = DFA()
    res = my_dfa.accepts_dfa(command,automata_commands)
    return res

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
        recog.pause_threshold = 1
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
    speak(f'El resultado es: {result}')

def open_app(app_to_open):
    if app_to_open is not None:
        if app_to_open == OPEN_COMMANDS[0]:
            os.system('kcalc')
        elif app_to_open == OPEN_COMMANDS[1]:
            os.system('code ~/Documentos')
        elif app_to_open == OPEN_COMMANDS[2]:
            os.system('dolphin Documentos')
        elif app_to_open == OPEN_COMMANDS[3]:
            os.system('notion-app-enhanced')
        elif app_to_open == OPEN_COMMANDS[4]:
            os.system('dolphin Descargas')
        elif app_to_open == OPEN_COMMANDS[5]:
            os.system('firefox')
        elif app_to_open == OPEN_COMMANDS[6]:
            os.system('spotify')
        else:
            speak('No está dentro de las aplicaciones contempladas')

def remember_something(topic):
    speak('¿En cuantos minutos quieres que te lo recuerde?')
    speak('En inglés por favor')
    time.sleep(1)
    time_2_wait = recog_voice()
    if 'minutes' in time_2_wait:
        time_2_wait.replace('minutes','')
        time_2_wait.replaceI(' ','')
    time_2_wait = float(time_2_wait) * 60
    time.sleep(time_2_wait)
    speak(f'Tienes un recordatorio de: {topic}')

def get_wiki(search_topic):
    search_result = wikipedia.search(search_topic,results=2)
    for result in search_result:
        try:
            speak(wikipedia.summary(result))
        except:
            speak('No encontré nada')

def search_videos(search_video,top=''):
    html = requests.get(f"https://www.youtube.com/results?search_query={search_video}")
    if html.status_code == 200:
        videos_ids = re.findall(r'watch\?v=(\S{11})',html.text)
        videos = []
        for i in range(5):
            videos.append('https://www.youtube.com/watch?v='+videos_ids[i])
        return videos


def get_info_video(url_video,search_youtube):
    video = requests.get(url_video)
    if video.status_code == 200:
        video_owner = re.findall(REGEX_CHANNEL,video.text)[0]
        video_title = re.findall(REGEX_TITLE,video.text)[0]

        try:
            video_date = re.findall(REGEX_DATE,video.text)[0]
            video_date = re.sub('"dateText":{"simpleText":"','',video_date)
            video_date = re.sub('"}','',video_date)
        except IndexError:
            video_date = 'N/A'

        video_title = re.sub(r'<title>','',video_title)
        video_title = re.sub(r' - YouTube</title>','',video_title)

        video_owner = re.sub('<link itemprop="name" content="','',video_owner)
        video_owner = re.sub('">','',video_owner)

        info_video = f'{video_title}\n{url_video}\nDe: {video_owner} - Subido el {video_date}\n\n'
        with open(f'{search_youtube}.txt',mode='a',encoding='utf-8') as file:
            file.write(info_video)
        speak('Te he creado un archivo con los videos que pediste')


def get_youtube_video(search_youtube):
    search_youtube = search_youtube.lower()
    search_youtube = search_youtube.replace(' ','+')
    videos_page = search_videos(search_youtube)
    for i in range(5):
        get_info_video(videos_page[i],search_youtube)


def listen_and_speak():
    print('Ya entramos')
    global had_presented
    if had_presented:
        command = recog_voice()
        if is_valid_command(command):
            if command == COMMANDS[0]:
                speak('¿Qué aplicación quiere abrir?')
                time.sleep(1)
                app_to_open = recog_voice()
                thread_other_app = threading.Thread(target=open_app,args=([app_to_open]))
                thread_other_app.start()
            elif command == COMMANDS[1]:
                speak('Diga su expresión aritmética, en inglés por favor')
                time.sleep(1)
                expression = recog_voice()
                eval_operation(expression)
            elif command == COMMANDS[2]:
                speak('¿Qué quieres que te recuerde?')
                time.sleep(1)
                reminder = recog_voice()
                thread_remember = threading.Thread(target=remember_something,args=([reminder]))
                thread_remember.start()
            elif command == COMMANDS[3]:
                speak('¿Qué quieres buscar en Youtube?')
                time.sleep(1)
                search_youtube = recog_voice()
            elif command == COMMANDS[4]:
                speak('¿Qué quieres buscar en Wikipedia?')
                time.sleep(1)
                search_wiki = recog_voice()
                if search_wiki is not None and search_wiki is not '':
                    get_wiki(search_wiki)
                else: speak('No te entendí')
            elif command == COMMANDS[5]:
                print('hablar')
    else:
        print('A presentarse')
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
            had_presented = True

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
        btn_micro = Button(root,text='Click me',image=microphone_img,command=listen_and_speak)
        btn_micro.place(x=550,y=450)
        root.mainloop()

if __name__ == '__main__':
    app = App()
    speak('Bienvenido, me llamo Bianca, pulsa el micrófono para hablar')