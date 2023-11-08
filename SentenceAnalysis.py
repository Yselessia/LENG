class Word:
    def __init__(self, word):
        self._word = word
        self.person = None

class Noun(Word):
    def __init__(self):
        pass

class Pronoun(Noun):    # <<<<<
    def __init__(self):
        pass

'''
class Verb(Word):
    def __init__(self, tense):
        self.tense = tense
class Adjective(Word):
    pass
class Numeral(Adjective):   # <<<<<<
    pass
class Determiner(Adjective):    # <<<<<<<
    pass
class Article(Determiner):  # <<<<<<<<
    pass
class Adverb(Adjective):    # <<<<<
    pass
class Preposition(Word):
    pass
class Conjunction(Word):
    pass
class Interjection(Word):   # <<<<<<<
    pass
'''


def setConnections():
    DICTFILE = 'testdictionary'
    import json
    global dictionary
    try:
        with open(DICTFILE+".json","r+") as file:
            dictionary = json.load(file)
            pass
    except:
        errMessg = f"Error: No dictionary.\nCheck directory for {DICTFILE}.json"
        print(errMessg)

def clean_sentence(sentence):
    #in this, each word, number, punctuation mark, is separated by a space.
    cleaned_sentence = re.sub(r'([^a-zA-Z\']+)', r' \1 ', sentence)
    cleaned_sentence_words = re.sub(r'[^a-zA-Z\']+', ' ', sentence)
    # Split the cleaned sentence into words
    return cleaned_sentence_words.split(), cleaned_sentence

def call_lemma(word):
    lemma = [None]
    ln = len(word)                      #length of the word is stored in a variable as it is used often
    if word[ln-3:ln] == "ing":          #continuous verb
        lemma = [word[:ln-3]]
        if word[ln-4] != "y":
            lemma.append(word[:ln-3]+"e")

    elif word[ln-1] == "s":             #plural noun or present simple
        lemma = [word[:ln-1]]
        if word[ln-2] == "e":
            if word[ln-3] == "o":                   #as in mango
                lemma = [word[:ln-2]]
            elif word[ln-3] == "i":                 #as in city
                lemma = [word[:ln-2]+ "y"]
            elif re.match(r'(sh|ch|a|u|z|x|s)$', word[:ln-2]):
                lemma.append(word[:ln-2])        
            elif word[ln-3] == "i" and re.match(f'{consonant}', word[ln-4]): 
                lemma.append(word[:ln-3]+"y")  
            else:
                lemma.append(word[:ln-2])        
            if word[ln-3] == "v":
                lemma.append(word[:ln-3] + "f")     #as in thief
                lemma.append(word[:ln-3] + "fe")    #as in wife

    elif (word[ln-2:ln] == "er" and (word[ln-3] != "y" or re.match(f'{vowel}y', word[ln-3:ln-1]))) or word[ln-2:ln] == "ed" or word[ln-3:ln] == "est":
        if word[ln-3:ln] == "est":
            wordT = word[:ln-1]         #superlative adj
        else:
            wordT = word                #comparative adj or verb simple past
        lnT = len(wordT)                #length of the word is stored in a variable as it is used often
        if wordT[lnT-3:lnT-1] == "ie":
            lemma = [wordT[:lnT-3]+"y"]             #as in happy
        elif wordT[lnT-2] == wordT[lnT-3]:
            lemma = [wordT[:lnT-2]]                 #as in tall
            lemma.append(wordT[:lnT-3])             #as in fat
        else:
            lemma = [wordT[:lnT-1]]                 #as in simple, (stayed, worked)

    return lemma                        #returns an array holding all valid options for the root word

def find_word(word):
    global consonant, vowel
    consonant= '[a-z&&[^aeiou]]'
    vowel = '[aeiou]'

    word = spell.correction(word.lower())
    #the first option is that the word is a root word, so a key in the dictionary
    wordData = [dictionary.get(word)]               #fix datatype for this!!!!!
    print(wordData) # <<<<<
    if wordData[0]:
        key = word
    else:
        #otherwise it may be an irregular form, so the dictionary values must be searched
        myindex = None
        values = dictionary.values()
        for item in values:
            if len(item)==3 and (word == item[2] or type(item[2]) == list and word in item[2]):
                myindex = list(values).index(item)
                break
        if myindex:
            key = list(dictionary.keys())[myindex]
            wordData = [dictionary.get(key)]
            print(wordData) # <<<<<
        else:
            lemmaVar = call_lemma(word)
            wordData = []
            for lemma in lemmaVar:
                wordData.append(dictionary.get(lemma))
            wordData = [item for item in wordData if item is not None]
            print(wordData) # <<<<<
            if not wordData:
                print("Word not found")
    print(wordData, "HIIIII") # <<<<<<<
    try:
        if type(wordData[0][0]) == int:
            for i in wordData[0]:
                wordData.append(dictionary.get(i))
            wordData = wordData[1:]

        for i in range(len(wordData)):
            wordData[0].insert(0,word)         #the finished sentence will be " ".join(i[x][0] for i in newSenList)
        newSenList.append(wordData)
    except:
        print("oops")
    



from spellchecker import SpellChecker
import string
import re                           #imports regex
spell = SpellChecker()

setConnections()
#here we split the sentence into a list of words
sentence = input("Please enter a sentence: ")
words, x = clean_sentence(sentence)
newSenList = []
for word in words:
    find_word(word)

print(newSenList)
