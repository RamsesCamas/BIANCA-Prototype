import speech_recognition as speech
#Prueba fallida
if __name__ == '__main__':
    recog = speech.Recognizer()
    mic = speech.Microphone(device_index=6)
    with mic as audio_file:
        print('Speak please')
        recog.adjust_for_ambient_noise(audio_file)
        audio = recog.listen(audio_file)
        print('Convirtiendo a texto')
        print('Dijiste:')
        try:
            print(recog.recognize_google(audio))
        except Exception as e:
            print('Error: ',e)
    