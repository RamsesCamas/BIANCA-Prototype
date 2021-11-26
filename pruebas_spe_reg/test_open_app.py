import os

def open_firefox():
    os.system('firefox')

def open_calculator():
    os.system('kcalc')

def open_spotify():
    os.system('spotify')

def open_document_folder():
    os.system('dolphin Documentos')

def open_downloads_folder():
    os.system('dolphin Descargas')

def open_vscode():
    os.system('code ~/Documentos')

if __name__ == '__main__':
    open_vscode()