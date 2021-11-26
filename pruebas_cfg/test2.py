import nltk
from random import randint

joke_grammar = nltk.CFG.fromstring("""
S -> FK WQ A R
FK -> K K
K -> "toc" | "knock"
WQ -> SIU QQ BE SID
QQ -> "Quién" | "Qué" | "Cómo"
BE -> "es" | "fue"
SIU -> "¿"
SID -> "?"
A -> SER P | WQ QQ
SER -> "Soy"
P -> "yo"
R -> "jajaja"
""")

K = ['toc','knock']
QQ = ['Quién', 'Qué', 'Cómo']
BE = ['es','fue']

toc = K[randint(0,1)]
joke = f'{toc} {toc}'
question_choose = QQ[randint(0,2)]
verb = BE[randint(0,1)]
question = f' ¿ {question_choose} {verb} ?'
joke = joke + question
choose = randint(0,1)
if choose == 0:
    joke = joke + ' Soy yo jajaja'
else:
    joke = joke + question + f' {question_choose} ' + 'jajaja'

sent = joke.split()
rd_parser = nltk.RecursiveDescentParser(joke_grammar)
try:
    cfg_parsed = rd_parser.parse(sent)
    for i in cfg_parsed:
        print(i)
except:
    print('La entrada no coincide con la gramática de chistes 2')