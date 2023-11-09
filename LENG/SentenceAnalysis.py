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
        form = "gerund,presentParticiple"   #please note.

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
        form = "plural:presentThird"

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
            lemma = [wordT[:lnT-1]]                 #as in simple, (danced)
            lemma.append(wordT[:lnT-2])             #as in fast, (stayed)
        match word[ln-1]:
            case "t":
                form = "superlative"
            case "r":
                form = "comparative"
            case "d":
                form = "past"
    else:
        form = None
    for i in range(len(lemma)):
            lemma[i] = [lemma[i], form]
    return lemma, form                        #returns an array holding all valid options for the root word

def find_word(word):
    global consonant, vowel, key
    consonant= '[a-z&&[^aeiou]]'
    vowel = '[aeiou]'
    word = spell.correction(word.lower())

    #the first option is that the word is a root word, so a key in the dictionary
    wordData = [dictionary.get(word)]               #fix datatype for this!!!!!
    if wordData[0]:
        key = word
        match wordData[0]:
            case "n":
                form = "singular"
            case "v":
                form = "present"
                if word == "be":
                    form = "infinitive"
            case "adj":
                form = "positive"
            case _:
                form = None
    else:
        #otherwise it may be an irregular form, so the dictionary values must be searched
        index = None
        values = dictionary.values()
        for item in values:
            if len(item)==3:
                if word == item[2] or (type(item[2]) == list and word in item[2]):
                    index = list(values).index(item)
                    key = list(dictionary.keys())[index]
                    if word == item[2]:
                        form = "plural"
                    elif len(item[2]) == 2:
                        if word == item[2][0]:
                            form = "comparative"
                        elif word == item[2][1]:
                            form = "superlative"
                    else:
                        if word == item[2][0]:
                            form = "present"
                        elif word == item[2][1]:
                            form = "present3"
                        elif word == item[2][2]:
                            form = "past"
                        elif word == item[2][3]:
                            form = "pastParticiple"
                        if len(item[2]) != 4:
                            if word == item[2][2]:
                                form = form + "T2andPlural"   #True (i.e., it is irregular)
                            if word == item[2][5]:
                                form = "presentT2andPlural"
                            elif word == item[2][0]:
                                form = form + "T1"
                            elif word == item[2][4]:
                                form = "pastT1and3"
                        #0"am" - Present first person singular 
                        #2"were" - Past second person singular and all persons plural
                        #4"was" - Past first and third person singular
                        #5"are" - Present second person singular and all persons plural
                    wordData = [dictionary.get(key)]
                    break
        #
        if not index:
            #it could also be a regular form of a word
            lemmaVar, form = call_lemma(word)
            wordData = []
            for i in range(len(lemmaVar)):
                lemData = dictionary.get(lemmaVar[i][0])
                if lemData and (lemData[1] == False or word[len(word)-3:len(word)] == "ing"):
                    wordData.append(lemData)
                    key = lemmaVar[i][0]
                    form = lemmaVar[i][1]
                    break                   #add possibility of multiple possible words being returned in lemmaVar
            if wordData:
                colon = form.find(":")
                if colon !=-1:
                    if wordData[0] == "n":
                        form = form[:colon]
                    elif wordData[0] == "v":
                        form = form[colon+1:]
            
    if wordData:
        word_append(wordData, word, form)
    else:
        print("Word not found")
    

#i have a feeling i'll need this at some point
def get_dupli_data():
    pass    

def word_append(wordData, word, form):
    global key
    if type(wordData[0][0]) == int: #this feels so very scuffed but i don't remember what it's for
        key = wordData[0]
        for i in wordData[0]:
            wordData.append(dictionary.get(str(i)))
        wordData = wordData[1:]

    for i in range(len(wordData)):
        wordData[i].insert(0,word)         #the finished sentence will be " ".join(i[x][0] for i in newSenList)
    wordData[0].insert(1,form)
    newSenList.append(wordData)

from spellchecker import SpellChecker
import string
import re                           #imports regex
spell = SpellChecker()

setConnections()
#here we split the sentence into a list of words
sentence = input("Please enter a sentence: ")
newSenList = []     #fix this
if sentence != "":
    words, x = clean_sentence(sentence)
    for word in words:
        find_word(word)
else:
    word = input()
    find_word(word)
print(newSenList)

