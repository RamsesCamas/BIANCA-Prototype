import wikipedia

def get_wiki(search_topic):
    search_result = wikipedia.search(search_topic,results=3)
    for result in search_result:
        try:
            print(wikipedia.summary(result))
        except:
            print('Error')

if __name__ == '__main__':
    wikipedia.set_lang("es")
    search_result = wikipedia.search('Python',results=3)
    print(search_result)
    for result in search_result:
        try:
            print(wikipedia.summary(result))
        except:
            print('Error')