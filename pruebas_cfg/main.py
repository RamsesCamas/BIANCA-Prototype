import nltk


grammar = nltk.CFG.fromstring("""
 S -> NP VP
 VP -> V NP | V NP PP
 V -> "vio" | "comió"
 NP -> "John" | "Mary" | "Bob" | Det N | Det N PP | "Ramsés"
 Det -> "un" | "el"| "la" | "mi"
 N -> "perro" | "gato" | "galleta" | "parque"
 PP -> P NP
 P -> "en" | "en" | "por" | "con"
 """)

sent = "Ada vio mi gato".split()
rd_parser = nltk.RecursiveDescentParser(grammar)
try:
    cfg_parsed = rd_parser.parse(sent)
except:
    print('La entrada no coincide con la gramática')
#for p in cfg_parsed:
#      print(p)


jokes_grammar = nltk.CFG.fromstring("""
S -> K Q A R | K
K -> "toc" | "knock" | K
Q -> "¿" WQ T "?" 
WQ -> "Quién" | "Qué" | "Cómo"
T -> "es" | "fue"
A -> "Soy yo" | Q WQ
R -> "jajaja"
""")
sent = "toc toc".split()
rd_parser = nltk.RecursiveDescentParser(jokes_grammar)
try:
    cfg_parsed = rd_parser.parse(sent)
    for i in cfg_parsed:
        print(i)
except:
    print('La entrada no coincide con la gramática')

jokes_grammar_2 = nltk.CFG.fromstring("""
S -> K M
K -> "toc" | "knock" | K K
M -> 'Mundo'
""")
sent = "toc toc Mundo".split()
rd_parser = nltk.RecursiveDescentParser(jokes_grammar_2)
try:
    cfg_parsed = rd_parser.parse(sent)
    for i in cfg_parsed:
        print(i)
except:
    print('La entrada no coincide con la gramática de chistes 2')