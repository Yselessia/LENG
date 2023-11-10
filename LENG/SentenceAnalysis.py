'''
                    Passive Voice:
    The cake was eaten by the children.
The code might not correctly identify the subject and object in passive voice sentences, 
as it seems to assume a more straightforward sentence structure.
                    Sentences with Pronominal References:
    She gave him the book that I borrowed from her.
The code might not correctly handle sentences with pronouns and their references, 
potentially misidentifying the subject and object.
                    Questions:
    Did you see the movie that I recommended?
In interrogative sentences like this, the subject-verb order is inverted. 
The current code might not account for this inversion and could potentially misidentify the subject and object positions.
'''



'''if type(word_data[0][0]) == int: #this feels so very scuffed but i don't remember what it's for
    key = word_data[0]
    for i in word_data[0]:
        word_data.append(dictionary.get(str(i)))
    word_data = word_data[1:]'''
#for i in range(len(word_data)):
#    word_data[i].insert(0,word)         #the finished sentence will be " ".join(i[x][0] for i in new_sen_list)
#word_data[0].insert(1,form)
#new_sen_list.append(word_data)

#"before": ["prep", false]
#"begin": ["v", true, ["begin", "begins", "began", "begun"]]
#"an": ["article", true, "indefinite"]
#"child": ["n", true, "children"]

class Word:
    def __init__(self, word, key=None):
        self.word = word
        self.key = key if key else word
        self.pos = None
        self.person = None
        self.plural = None
        self.tense = None
        self.form = None        #i hate myself <3

class Sentence(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__num = 0
        self.subject = None
        self.object = None          #not sure abt this

    @property
    def get_verb(self):
        return self.get_pos("v")
                
    @property
    def verb(self):
        try:
            num = self.__num
            self.__num = 0
            verb_index = self.get_verb
            return self[verb_index[num]]
        except (IndexError, TypeError):
            return None
    
    def set_num(self, num):
        self.__num = num

    def get_pos(self, pos):
        index_list = []
        for index in range(len(self)):
            if self[index].pos == pos:
                index_list.append(index)
        return index_list

    def change_word(self, index, attribute, new_value):
        if not hasattr(self[index], attribute):
            raise AttributeError(f"'{type(self[index]).__name__}' object has no attribute '{attribute}'")
        setattr(self[index], attribute, new_value)

        

def set_connections():
    DICTFILE = 'testdictionary'
    import json
    global dictionary
    try:
        with open(DICTFILE+".json","r+") as file:
            dictionary = json.load(file)
            pass
    except:
        err_messg = f"Error: No dictionary.\nCheck directory for {DICTFILE}.json"
        print(err_messg)

set_connections()
capitals = '[A-Z]'
import re

form = "presentThird"
key = "go"
word1 = Word("goes", key)
word_data = [dictionary.get(key)]
word1.pos = word_data[0][0]
word1.plural = True
person = re.search(capitals, form)
word1.person = form[person.start():].lower()
word1.tense = form[:person.start()]

form = "positive"
key = "cheap"
word2 = Word("cheap")
word_data = [dictionary.get(key)]
word2.pos = word_data[0][0]
word2.form = form

form = "presentThird"
key = "go"
word3 = Word("hk", key)
word_data = [dictionary.get(key)]
word3.pos = word_data[0][0]
word3.plural = True
person = re.search(capitals, form)
word3.person = form[person.start():].lower()
word3.tense = form[:person.start()]
sentence1 = Sentence()

sentence1.append(word1)
sentence1.append(word2)
sentence1.append(word3)
print(sentence1[1].key)
x = sentence1.verb
print(x.word)
sentence1.set_num(1)
x = sentence1.verb
print(x.word)
x = sentence1.verb
print(x.word)
sentence1.get_pos("v")[0] 
sentence1.change_word(1, 'word', "cheapest")
print(sentence1[1].word)





'''
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
            word_temp = word[:ln-1]         #superlative adj
        else:
            word_temp = word                #comparative adj or verb simple past
        lnT = len(word_temp)                #length of the word is stored in a variable as it is used often
        if word_temp[lnT-3:lnT-1] == "ie":
            lemma = [word_temp[:lnT-3]+"y"]             #as in happy
        elif word_temp[lnT-2] == word_temp[lnT-3]:
            lemma = [word_temp[:lnT-2]]                 #as in tall
            lemma.append(word_temp[:lnT-3])             #as in fat
        else:
            lemma = [word_temp[:lnT-1]]                 #as in simple, (danced)
            lemma.append(word_temp[:lnT-2])             #as in fast, (stayed)
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
    word_data = [dictionary.get(word)]               #fix datatype for this!!!!!
    if word_data[0]:
        key = word
        match word_data[0]:
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
                    word_data = [dictionary.get(key)]
                    break
        #
        if not index:
            #it could also be a regular form of a word
            lemma_var, form = call_lemma(word)
            word_data = []
            for i in range(len(lemma_var)):
                lemma_data = dictionary.get(lemma_var[i][0])
                if lemma_data and (lemma_data[1] == False or word[len(word)-3:len(word)] == "ing"):
                    word_data.append(lemma_data)
                    key = lemma_var[i][0]
                    form = lemma_var[i][1]
                    break                   #add possibility of multiple possible words being returned in lemma_var
            if word_data:
                colon = form.find(":")
                if colon !=-1:
                    if word_data[0] == "n":
                        form = form[:colon]
                    elif word_data[0] == "v":
                        form = form[colon+1:]
    if word_data:
        word_append(word_data, word, form)
    else:
        print("Word not found")

def word_append(word_data, word, form):
    global key
    if type(word_data[0][0]) == int: #this feels so very scuffed but i don't remember what it's for
        key = word_data[0]
        for i in word_data[0]:
            word_data.append(dictionary.get(str(i)))
        word_data = word_data[1:]
    for i in range(len(word_data)):
        word_data[i].insert(0,word)         #the finished sentence will be " ".join(i[x][0] for i in new_sen_list)
    word_data[0].insert(1,form)
    new_sen_list.append(word_data)

#i have a feeling i'll need this at some point
def get_dupli_data():
    pass  

from spellchecker import SpellChecker
import string
import re                           #imports regex
spell = SpellChecker()

set_connections()
#here we split the sentence into a list of words
sentence = input("Please enter a sentence: ")
new_sen_list = []     #fix this
if sentence != "":
    words, x = clean_sentence(sentence)
    for word in words:
        find_word(word)
else:
    word = input()
    find_word(word)
print(new_sen_list)

'''