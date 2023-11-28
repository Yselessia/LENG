from spellchecker import SpellChecker
import re                           #imports regex
spell = SpellChecker()
CONSONANT= '[a-z&&[^aeiou]]'
VOWEL = '[aeiou]'
CAPITALS = '[A-Z]'
PUNCTUATION = '[?:,.!\'"]'
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
        @property
        def person(self):
            person = [i for i in range(1,4) if i in self.plural or i in self.singular]
            return person   #returns persons as a list *not* differentiated by plural
        def all(self):
            self.plural = 1,2,3
            self.singular = 1,2,3
        
        #these set the plural + singular attributes without the need to remember trailing commas within the main code
        def p(self,t):
            if type(t) == int:
                t = t,
            self.plural = t
        def s(self,t):
            if type(t) == int:
                t = t,
            self.singular = t

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
    @property
    def dupli_index_key(self):
        length_key = []
        i = 0
        while i < len(self):
            if self[i].id:
                length_key.append(self[i].id)
                i = i + len(self[i].id) + 1
            else:
                length_key.append([i])
                i = i + 1
        return length_key
    
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
        copies_bool = False
        if id:
            for index in range(len(self)):
                if self[index].id == id:
                    index_list.append(index)
        if len(index_list) > 0:
            copies_bool = True
        return copies_bool, index_list

def compile_all_patterns():     #<<<< fix th eorder of these
    all_patterns = [(r'\bdet\b', r'\bdet\b\s+(adj|n)' ,'determinerMatch'),
                    (r'\badj\b', r'\badj\b\s+(adj|n)' ,'adjectiveMatch'),
                    (r'\badv\b', r'\badv\b\s+(v|adv)' ,'adverbMatch'),
                    (r'\bv\b', r'\b(v\s+){2,}v\b', 'verbRepetition'),
                    (r'v\b', r'n\b.*\bv\b', 'verbSubject'),
                    (r'pron|n', r'\b(?:n|pron)\s(?!pron|n)', 'nounRepetition')]
    return [(re.compile(pattern[0]), re.compile(pattern[1]), pattern[2]) for pattern in all_patterns]

def clean_sentence(sentence):
    #in this, each word, number, punctuation mark, is separated by a space.
    cleaned_sentence = re.sub(r'([^a-zA-Z\']+)', r' \1 ', sentence)
    cleaned_sentence_words = re.sub(r'[^a-zA-Z\']+', ' ', sentence)
    # Split the cleaned sentence into words
    cleaned_punctuated = [[item, True] if re.match(PUNCTUATION, item) else [item, False] for item in cleaned_sentence.split()]
    return cleaned_sentence_words.split(), cleaned_punctuated

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

def add_word(orig_word):
    global DUPLI
    word = spell.correction(orig_word.lower())
    if word != orig_word.lower():
        spell_error = True
    word = Word(word)
    word_data = dictionary.get(word.word)
    dialogue(word_data)
    word_copies = find_word(word, word_data)
    dialogue("L",word_copies)
    for i in word_copies:
        dialogue("F",i,i.word,i.get_key,i.pos)
    if len(word_copies) > 1:            #the DUPLI flag _dupli represents when a word in the sentence is a copy of another
        DUPLI = DUPLI + 1               #it is a unique number for each (word_copies)
    if len(word_copies) >= 1:
        for item in word_copies:
            new_sen_list.append(item)
    else:
        dialogue("Word not found")
        new_sen_list.append(None)
    return spell_error, word.word

def find_word(word, word_data):
    word_duplicates = []
    dialogue(">",word.word, word.get_key, word_data)
    #the first option is that the word is a root word, so a key in the dictionary
    if word_data:
        word.id
        if type(word_data[0]) == int:
            for i in range(len(word_data)):
                word_duplicates.append(word.make_dupli())
                word_duplicates[i].set_key(word_data[i])
                word_duplicates[i].pos = dictionary.get(word_data[i])
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
                        word.person.s(1,2)
                        word.person.p(1,2,3)
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
                                word.person.s(3)
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
                                word.person.s(2)
                                word.person.p(1,2,3)
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][5]:
                                word.tense = "present"
                                word.person.s(2)
                                word.person.p(1,2,3)
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][0]:
                                word.tense = "present"
                                word.person.s(1)
                                word, word_duplicates, single = append_dupli(word, word_duplicates, single)
                            elif word == item[2][4]:
                                word.tense = "past"
                                word.person.s(1,3)
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
                dialogue(form)
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
                        word.person.s(int(form[len(word)])) #here, 3 - always in last char
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


def pos_clean_sva(sentence, punctuated_sen,punctuated_index_key):  #sentence in this function is new_sen_list
    verb_list = [item for item in sentence.get_verb]
    #false represents that the verb has no possible variations.
    if len(verb_list) > 1:
        #this ????????? checks if there r diff clauses in the sentence
        comma = []
        comma_index = 0
        while "," in [i[0] for i in punctuated_sen]:
            #the position of the comma in the unsearched portion of the sentence
            comma_index =  [i[0] for i in punctuated_sen][comma_index:].index(",") 
            for i, sublist in enumerate(punctuated_index_key):
                if comma_index in sublist:
                    comma.append(i)
        #if there is a comma in the sentence: - unfinished - creates <clause_sen> + changes sentence
        if comma:
            match len(comma):
                case 1:
                    pass
                case 2:
                    # list[index] = a,b,c where index is representative of the actual no. of words in the submitted sentence
                    clause_full_index = sentence.dupli_index_key[comma[0]:comma[1]]
                    #here it is a list (of lists) of indexes of words in the clause
                    #next it is narrowed down to just the start and end indexes
                    clause_full_index = [clause_full_index[0], clause_full_index[len(clause_full_index)]]
                    #clause contains 
                    clause = sentence[clause_full_index[0], clause_full_index[1]]
                    clause.pos = "n"
                    clause_rep = Noun(Word("<>", None)) #a custom word to represent the clause
                    clause_sen = sentence[clause_full_index[0]:clause_full_index[1]]
                    sentence = sentence[:clause_full_index[0]] + [clause_rep] + sentence[clause_full_index[1] +1:]
                    verb_list = [item for item in sentence.get_verb]
                case _:
                    pass
        #this checks if some of the verbs are actually nouns or something idk
        verb_definite = []
        for i in verb_list:
            if sentence.get_dupli(i)[0] == False:
                verb_definite.append(verb_list[i])

    if (verb_definite and len(verb_definite) == 1) or len(verb_list) == 1:
        if verb_definite:
            verb_list = verb_definite
    #add to conditional <<<<<
    if clause:
        all_errors_list_1, clause = subject_verb_error(clause)

    all_errors_list, new_sentence = subject_verb_error(sentence)
    if clause:
        #adding the clause back into the sentence
        new_sentence[clause_pos] = clause[0]
        for word in clause:
            new_sentence.insert(clause_pos+1, word)
        #updating the number of errors
        for i in range(len(all_errors_list)):
            my_err = all_errors_list[i]
            if my_err[0] in [i[0] for i in all_errors_list_1]:
                err_count = my_err[1] + all_errors_list_1[all_errors_list_1.index[my_err]][1]
                all_errors_list[i] = my_err[0], err_count
        for i in range(len(all_errors_list_1)):
            if all_errors_list_1[i][0] not in [i[0] for i in all_errors_list]:
                all_errors_list.append(all_errors_list_1[i])
    return all_errors_list, new_sentence

def subject_verb_error(sentence, Continue=True):
    global all_patterns
    pos_list = " "
    for i in sentence:
        pos_list = pos_list + str(i.pos) + " "
    all_errors = []
    err_positions_list = []
    for j in all_patterns:
        if j[0].findall(pos_list):   
            if j[2] == 'nounRepetition':
                if len(j[1].findall(pos_list)) < len(j[0].findall(pos_list)):
                    all_errors.append(j[2])
                    #this filters the iterable into just the items which are in j[0] but not j[1]
                    position_of_error = [(item.start(), item.end()) for item in j[0].finditer(pos_list) 
                                         if (item.start(), item.end()) not in [(match.start(), match.end()) 
                                                                               for match in j[1].finditer(pos_list)]]
                    err_positions_list.append(position_of_error)

            elif j[2] == 'verbRepetition':
                if j[1].findall(i):
                    all_errors.append(j[2])
                    position_of_error = [(item.start(), item.end()) for item in j[1].finditer(pos_list)]
                    err_positions_list.append(position_of_error)
            elif not j[1].findall(pos_list):
                all_errors.append(j[2])
                position_of_error = []      # <<<<<<<< fix this !!!!!!!!!!!!
                err_positions_list.append(position_of_error)
    if Continue:
        all_errors_list, new_sentence = correct_sva(all_errors, err_positions_list, pos_list, sentence)
        return all_errors_list, new_sentence
    else:
        return all_errors, err_positions_list, pos_list

#this function does a simple check to see if the correction was helpful
def continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list):
    if (all_errors[index] != new_errors[index]) or (len(new_err_pos[index]) < len(err_positions[index])):
        all_errors, err_positions, pos_list = new_errors, new_err_pos, new_pos_list 
        continue_true = True
    else:
        continue_true = False
    return continue_true, all_errors, err_positions, pos_list

def correct_sva(all_errors, err_positions, pos_list, sentence):
    sentence_hold = sentence    #this stores the unchanged sentence for comparison
    #and this holds the error type and number of that error before the sentence is corrected.
    all_errors_hold = [(all_errors[i], len(err_positions[i])) for i in range(len(all_errors))]
    index = 0
    while all_errors:
    	current_err = all_errors[index]
        for err_pos_obj in err_positions[index]:
            #this finds the index of the error in the Sentence obj
            err_pos = pos_list[:err_pos_obj[0]].count(" ") - 1
            match all_errors[index]:
                case 'determinerMatch':
                    if sentence[err_pos-1].pos == "n":
                        if sentence[err_pos-2] != "det":
                            temp_word = sentence[err_pos-1]
                            sentence[err_pos-1 ] = sentence[err_pos]
                            sentence[err_pos] = temp_word
                            new_errors, new_err_pos, new_pos_list = subject_verb_error(sentence, False)
                            continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                        if continue_true == False:
                            sentence = sentence_hold
                            del sentence[err_pos]
                            all_errors, err_positions, pos_list = subject_verb_error(sentence, False)
                    else:
                        for i in range(len(sentence.get_verb)):
                            if i > err_pos:
                                break
                        this_verb = sentence[sentence.get_verb[i]]
                        if 3 in this_verb.person.person:
                            if 3 in this_verb.person.singular:
                                new_word = Pronoun(Word("it"))      # <<< ADD PERSONIFICTAION FLAG TO DICT
                                new_word.plural = False
                            else:
                                new_word = Pronoun(Word("they"))
                                new_word.plural = True
                            new_word.person = 3
                        elif 2 in this_verb.person.person:          # <<< ADD PERSONIFICTAION FLAG TO DICT
                            new_word = Pronoun(Word("you")) 
                            if 2 in this_verb.person.singular:  
                                new_word.plural = False
                            else:
                                new_word.plural = True  
                            new_word.person = 2
                        elif 1 in this_verb.person.person:          # <<< ADD PERSONIFICTAION FLAG TO DICT
                            if 1 in this_verb.person.singular:
                                new_word = Pronoun(Word("i"))
                                new_word.plural = False
                            else:
                                new_word = Pronoun(Word("we"))
                                new_word.plural = True
                            new_word.person = 1
                        new_word.pos = "pron"
                        sentence[err_pos] = new_word
                        all_errors, err_positions, pos_list = subject_verb_error(sentence, False)
                case 'adjectiveMatch':
                    if sentence[err_pos-1].pos == "n":
                        temp_word = sentence[err_pos-1]
                        sentence[err_pos-1 ] = sentence[err_pos]
                        sentence[err_pos] = temp_word
                        new_errors, new_err_pos, new_pos_list = subject_verb_error(sentence, False)
                        continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos]
                        all_errors, err_positions, pos_list = subject_verb_error(sentence, False)
                case 'adverbMatch':
                    if sentence[err_pos-1].pos == "v":
                        temp_word = sentence[err_pos-1]
                        sentence[err_pos-1 ] = sentence[err_pos]
                        sentence[err_pos] = temp_word
                        new_errors, new_err_pos, new_pos_list = subject_verb_error(sentence, False)
                        continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos]
                        all_errors, err_positions, pos_list = subject_verb_error(sentence, False)

                case 'verbSubject':
                    pass    #temporary
                case 'verbRepetition':
                    err_pos_2 = pos_list[:err_pos_obj[1]].count(" ") - 1
                    for i in range(len(sentence[err_pos:err_pos_2])):
                        if sentence[i].get_key == "be" or sentence[i].get_key == "have":
                            if not keep_index:
                                keep_index = i,
                            else:
                                keep_index = keep_index,i
                                break
                    if keep_index:
                        if keep_index[1]:
                            del sentence[keep_index[1]]
                        else: 
                            del sentence[keep_index[0]+2:err_pos_2+1]
                        del sentence[err_pos:keep_index[0]]
                    else:
                        del sentence[err_pos+1:err_pos_2]
                    all_errors, err_positions, pos_list = subject_verb_error(sentence, False)
                case 'nounRepetition':
                    err_pos_2 = pos_list[:err_pos_obj[1]].count(" ") - 1
                    verb_list = sentence.get_verb
                    for i in range(len(verb_list)):
                        if i > err_pos:
                                verb_list = verb_list[i:]
                                break
                    if verb_list[0] > err_pos:
                        #there are verbs after the noun repetition
                        #try moving the noun after each verb.
                        continue_true = False   #temporary
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos+1:err_pos_2]
                    all_errors, err_positions, pos_list = subject_verb_error(sentence, False)
                case _:
                    dialogue("lol help")
        
        if index < len(all_errors)-1:
		    index = index + 1
    	else:
            index = 0
    return all_errors_hold, sentence
        
            

#returns all_errors_list, sentence_new, spell_error_count
def main_algorithm(sentence):
    global new_sen_list
    new_sen_list = Sentence()
    spell_error_count = 0
    words, punctuated_sen = clean_sentence(sentence)
    for word in words:
        spell_error, new_word = add_word(word)
        if spell_error == True:
            spell_error_count = spell_error_count + 1
            #this corrects the spelling of the word in the punctuated list of the sentence so that it can be found later
            index_of_word = [item[0] for item in punctuated_sen].index(word)
            punctuated_sen[index_of_word][0] = new_word

    #this creates a key for referencing the position of punctuation in the sentence (combined with .dupli_index_key)
    # list[index] = a,b,c where index is representative of the actual no. of words in the submitted sentence
    punctuated_index_key = [[] for i in range(len(words))]
    j = 0
    for i in range(len(punctuated_sen)):
        if punctuated_sen[i][1] == True:
            punctuated_index_key[j].append(i)
        else:
            j = j + 1

    if len(new_sen_list) > 0:   #??
        all_errors_list, sentence = pos_clean_sva(new_sen_list, punctuated_sen, punctuated_index_key)
        sentence_new = [word.word for word in sentence]
    return all_errors_list, sentence_new, spell_error_count




#testing
'''
def set_connections():
    DICTFILE = 'testdictionary'
    import json
    global dictionary
    try:
        with open(DICTFILE+".json","r+") as file:
            dictionary = json.load(file)
    except:
        err_messg = f"Error: No dictionary.\nCheck directory for {DICTFILE}.json"
        dialogue(err_messg)

dialogue = print
set_connections()
all_patterns = compile_all_patterns()
sentence = input("Please enter a sentence: ")
if sentence != "":
    main_algorithm(sentence)
else:
    word = input()
    add_word(word)

dialogue(new_sen_list)
sentence = ""
for i in new_sen_list:
    if i:
        dialogue("THIS")
        dialogue(i.word) # sentence = sentence+str(i.word)
dialogue(sentence)
'''