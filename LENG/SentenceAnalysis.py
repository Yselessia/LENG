from spellchecker import SpellChecker
import re                           #imports regex
spell = SpellChecker()
CONSONANT= '[a-z&&[^aeiou]]'
VOWEL = '[aeiou]'
CAPITALS = '[A-Z]'
DUPLI = 0
            #note: add separate infinitive check within sentence class
            #note: add plural check to the datastore creator

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

#"before": ["prep", false]
#"begin": ["v", true, ["begin", "begins", "began", "begun"]]
#"an": ["article", true, "indefinite"]
#"child": ["n", true, "children"]

class Word:
    def __init__(self, word, key=None):
        self.word = str(word)
        self._key = str(key) if key else word
        self.pos = str()        #i hate myself <3
        self._dupli = None
    @property
    def get_key(self):
        return self._key
    @property
    def id(self):
        return self._dupli
    
    def set_key(self, key):
        self._key = str(key)
    def make_dupli(self):
        new_word = Word(self.word, key=self._key)
        new_word.pos = self.pos
        new_word._dupli = self._dupli = DUPLI
        return new_word
      
class Verb(Word):
    def __init__(self, word_object):
        # Assuming word_object is an instance of the Word class
        super().__init__(word_object.word, key=word_object._key)
        self._dupli = word_object._dupli
        self.pos = "v"
        self.tense  = str()
        self.person = self._Person()
    class _Person():
        def __init__(self):
            self.plural = tuple()
            self.singular = tuple()
        def all(self):
            self.plural = 1,2,3
            self.singular = 1,2,3

class Adjective(Word):
    def __init__(self, word_object):
        # Assuming word_object is an instance of the Word class
        super().__init__(word_object.word, key=word_object._key)
        self._dupli = word_object._dupli
        self.pos = word_object.pos
        self.form = str()

class Noun(Word):
    def __init__(self, word_object):
        # Assuming word_object is an instance of the Word class
        super().__init__(word_object.word, key=word_object._key)
        self._dupli = word_object._dupli
        self.pos = word_object.pos
        self.plural = bool()

class Pronoun(Noun):
    def __init__(self, word_object):
        super().__init__(word_object)
        if isinstance(word_object, Noun):
            # If a Noun object is passed in, inherit attributes and update plural if needed
            self.plural = word_object.plural
        self.person = str()

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
    def get_dupli(self, index):
        id = self[index].id
        index_list = []
        if id:
            for index in range(len(self)):
                if self[index].id == id:
                    index_list.append(index)
        return index_list



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
        pos = "v"                           #"v", as gerund is derived from a verb

    elif word[ln-1] == "s":             #plural noun or present simple
        lemma = [word[:ln-1]]
        if word[ln-2] == "e":
            if word[ln-3] == "o":                   #as in mango
                lemma = [word[:ln-2]]
            elif word[ln-3] == "i":                 #as in city
                lemma = [word[:ln-2]+ "y"]
            elif re.match(r'(sh|ch|a|u|z|x|s)$', word[:ln-2]):
                lemma.append(word[:ln-2])        
            elif word[ln-3] == "i" and re.match(f'{CONSONANT}', word[ln-4]): 
                lemma.append(word[:ln-3]+"y")  
            else:
                lemma.append(word[:ln-2])        
            if word[ln-3] == "v":
                lemma.append(word[:ln-3] + "f")     #as in thief
                lemma.append(word[:ln-3] + "fe")    #as in wife
        form = "plural:present3"
        pos = "n:v"

    elif (word[ln-2:ln] == "er" and (word[ln-3] != "y" or re.match(f'{VOWEL}y', word[ln-3:ln-1]))) or word[ln-2:ln] == "ed" or word[ln-3:ln] == "est":
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
        pos = "adj"
        match word[ln-1]:
            case "t":
                form = "superlative"
            case "r":
                form = "comparative"
            case "d":
                form = "past"
                pos = "v"
    else:
        form = None
        pos = None
    for i in range(len(lemma)):
            lemma[i] = [lemma[i], form, pos]
    return lemma                            #returns an array holding all valid options for the root word

def add_word(word):
    global DUPLI
    word = spell.correction(word.lower())
    word = Word(word)
    word_data = dictionary.get(word.word)
    print(word_data)
    word_copies = find_word(word, word_data)
    print("L",word_copies)
    for i in word_copies:
        print("F",i,i.word,i.get_key,i.pos)
    if len(word_copies) > 1:            #the DUPLI flag _dupli represents when a word in the sentence is a copy of another
        DUPLI = DUPLI + 1               #it is a unique number for each (word_copies)
    if len(word_copies) >= 1:
        for item in word_copies:
            new_sen_list.append(item)
    else:
        print("Word not found")
        new_sen_list.append(None)

def find_word(word, word_data):
    word_duplicates = []
    print(">",word.word, word.get_key, word_data)
    #the first option is that the word is a root word, so a key in the dictionary
    if word_data:
        word.id
        if type(word_data[0]) == int:
            for i in range(len(word_data)):
                word_duplicates.append(word.make_dupli())
                word_duplicates[i].set_key(word_data[i])
                word_duplicates[i].pos = dictionary.get(word_data[i])        else:
            word_duplicates.append(word)
        for i in range(len(word_duplicates)):
            word = word_duplicates[i]
            word_data = dictionary[word.get_key]
            word.pos = word_data[0]
            match word_data[0]:
                case "n":
                    word = Noun(word)
                    word.plural = False
                case "v":
                    word = Verb(word)
                    if word == "be":
                        word.tense = "infinitive"
                        word.person.all()
                    else:
                        word.tense = "present"
                        word.person.singular = 1,2
                        word.person.plural = 1,2,3
                case "adj":
                    word = Adjective(word)
                    word.form = "positive"
                case "pron":
                    word = Pronoun(word)
            word_duplicates[i] = word       #saves the changes to the word
    else:
        #otherwise it may be an irregular form, so the dictionary values must be searched
        index = None
        values = dictionary.values()
        single = True               #if there is a duplicate option (more than one word possible) this flag is changed
        for item in values:
            if len(item)==3:
                if word.word == item[2] or (type(item[2]) == list and word.word in item[2]):
                    index = list(values).index(item)
                    key = list(dictionary.keys())[index]
                    word.pos = item[0]
                    word.set_key(key)
                    if word.word == item[2]:
                        word = Noun(item)
                        word.plural = True
                    elif len(item[2]) == 2:
                        word = Adjective(word)
                        if word.word == item[2][0]:
                            word.form = "comparative"
                        elif word.word == item[2][1]:
                            word.form = "superlative"
                    else:
                        word = Verb(word)
                        if len(item[2]) == 4:
                            if word == item[2][1]:
                                word.tense = "present"
                                word.person.singular = 3
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][2]:
                                word.tense = "past"
                                word.person.all()
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][3]:
                                word.tense = "pastParticiple"
                                word.person.all()
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                        elif len(item[2]) > 4:
                            if word == item[2][2]:
                                word.tense = "past"
                                word.person.singular = 2
                                word.person.plural = 1,2,3
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][5]:
                                word.tense = "present"
                                word.person.singular = 2
                                word.person.plural = 1,2,3
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][0]:
                                word.tense = "present"
                                word.person.singular = 1
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][4]:
                                word.tense = "past"
                                word.person.singular = 1,3
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                        #0"am" - Present first person singular 
                        #2"were" - Past second person singular and all persons plural
                        #4"was" - Past first and third person singular
                        #5"are" - Present second person singular and all persons plural
        #
        if len(word_duplicates) < 1:
            #it could also be a regular form of a word
            lemma_var = call_lemma(word.word)
            word_data = []
            for i in range(len(lemma_var)):
                form = lemma_var[i]
                print(form)
                lemma_data = dictionary.get(lemma_var[i][0])
                pos = []
                key_temp = []
                if lemma_data and type(lemma_data[0]) == int:
                    colon = form.find(":")
                    if colon !=-1:
                        word = Noun(word)
                        word.pos = "n"
                        word.plural = True
                        word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                        word = Verb(word)
                        word.tense = form[colon+1:len(word)-1]  #form = "plural:present3"
                        word.person.singular = int(form[len(word)]) #here, 3 - always in last char
                    else:
                        for i in lemma_data:
                            pos.append(dictionary(i)[0])
                            key_temp.append(i)

                if lemma_data and lemma_data[1] == False:
                    key = key_temp if key_temp else lemma_var[i][0]
                    form = lemma_var[i][1]
                    lemma_data[0] = pos if pos else lemma_data[0]
                    comma = form.find(",")
                    if comma !=-1 and "v" in lemma_data[0]:
                        index = lemma_data[0].index("v")
                        key = key[index]
                        word.set_key(key)
                        word = Noun(word)               #a gerund is a type of noun
                        word.pos = "n"
                        word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                        word = Verb(word)
                        word.tense = form[comma+1:]     #presentParticiple
                        word.person.all()
                        word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                    elif comma == -1:
                            check_pos = "adj"
                            if form== "past":
                                check_pos = "v"
                            if check_pos in lemma_data[0]:
                                if type(key) == list:
                                    index = lemma_data[0].index(check_pos)
                                    key = key[index]
                                word.set_key(key)
                                if check_pos == "v":
                                    word = Verb(word)
                                    word.tense = form
                                    word.person.all()
                                else:
                                    word = Adjective(word)
                                    word.pos = "adj"
                                    word.form = form
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
    return word_duplicates

def append_dupli(word, word_duplicates, single):
    if single == True:
        word_duplicates.append(word)
        single = False
    else:
        word_duplicates.append(word.make_dupli())
    return word, word_duplicates, single



set_connections()
#here we split the sentence into a list of words
sentence = input("Please enter a sentence: ")
new_sen_list = Sentence()
if sentence != "":
    words, x = clean_sentence(sentence)
    for word in words:
        add_word(word)
else:
    word = input()
    add_word(word)
print(new_sen_list)
sentence = ""
for i in new_sen_list:
    if i:
        print("THIS")
        print(i.word) # sentence = sentence+str(i.word)
print(sentence)