from spellchecker import SpellChecker
import re                           #imports regex
spell = SpellChecker()
DICTFILE = "dictionary"
CONSONANT= r'[a-z&&[^aeiou]]'
VOWEL = r'[aeiou]'
CAPITALS = r'[A-Z]'
PUNCTUATION = r'[?:,.!\'"]'
dupli = 0
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
        if type(self) == Word:
            new_word = type(self)(self.word, key=self._key)
        else:
            new_word = type(self)(self)
        new_word.pos = self.pos
        new_word._dupli = self._dupli = dupli
        return new_word
      
class Verb(Word):
    def __init__(self, word_object):
        # Assuming word_object is an instance of the Word class
        super().__init__(word_object.word, word_object._key)
        self._dupli = word_object._dupli
        self.pos = "v"
        self.tense  = str()
        self.person = self._Person()
    def make_dupli(self):
        new_word = super().make_dupli()
        new_word.tense = self.tense
        new_word.person = self.person
        return new_word

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
        super().__init__(word_object.word, word_object._key)
        self._dupli = word_object._dupli
        self.pos = "adj"
    def make_dupli(self):
        new_word = super().make_dupli()
        new_word.form = self.form
        return new_word

class Noun(Word):
    def __init__(self, word_object):
        # Assuming word_object is an instance of the Word class
        super().__init__(word_object.word, word_object._key)
        self._dupli = word_object._dupli
        self.pos = "n"
        self.plural = bool()    
    def make_dupli(self):
        new_word = super().make_dupli()
        new_word.plural = self.plural
        return new_word

class Pronoun(Noun):
    def __init__(self, word_object):
        super().__init__(word_object)
        if isinstance(word_object, Noun):
            # If a Noun object is passed in, inherit attributes and update plural if needed
            self.plural = word_object.plural
        self.person = str()
        self.pos = "pron"
    def make_dupli(self):
        new_word = super().make_dupli()
        new_word.person = self.person
        return new_word

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
            length_key.append([])
            if self[i].id:
                all_id = [j.id for j in self if j.id == self[i].id]
                length_key.append((i,i + len(all_id)-1))
                i = i + len(all_id)
            else:
                length_key.append((i,i))
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
    all_patterns = [(r'pron|n\b', r'\b(n|pron)\b\s+(adj|det|pron|n)', 'nounRepeated'),
                    (r'\bdet\b', r'\bdet\b\s+(adj|n)' ,'Determiners'),
                    (r'\bprep\b', r'\bprep\b\s+(det)' ,'Prepositions'),
                    (r'\badj\b', r'\badj\b\s+(adj|n)' ,'Adjectives'),
                    (r'\badv\b', r'\badv\b\s+(v|adv)' ,'Adverbs'),
                    (r'\bv\b', r'\b(v\s+){2,}v\b', 'verbRepeated'),
                    (r'v\b', r'n\b.*\bv\b', 'verbHasSubject')]
    return [(re.compile(pattern[0]), 
             re.compile(pattern[1]), 
             pattern[2], 
             re.compile(pattern[3]) if len(pattern) > 3 else None) 
             for pattern in all_patterns]

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
        form = "singular:participle0"   #please note.
        pos = "n:v"                           #"v", as gerund is derived from a verb

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
    def add_to_dict(event):
        selected_pos = scrll_crit.get(scrll_crit.curselection())
        options.destroy()
        confirm = confirm_change("Is it regularly conjugated?")
        if confirm == True:
            word = user_entry("Enter word:")
            dictionary[word] = [selected_pos, False]
        else:
            try:
                if selected_pos == "n":
                    word = user_entry("Enter singular:")
                    irreg_inputs = user_entry("Enter plural:")
                elif selected_pos == "adj":
                    word = user_entry("Enter positive:")
                    irreg_inputs = [user_entry("Enter comparative:")]
                    irreg_inputs.append( user_entry("Enter superlative:"))
                    irreg_inputs = [pos_adj, comp_adj, super_adj]
                elif selected_pos == "v":
                    word = user_entry("Enter infinitive:")
                    irreg_inputs = [word]
                    irreg_inputs.append( user_entry("Enter third person present:"))
                    irreg_inputs.append( user_entry("Enter simple past tense:"))
                    irreg_inputs.append( user_entry("Enter past participle:"))
                else:
                    raise Exception
                dictionary[word] = [selected_pos, True, irreg_inputs]
            except:
                dialogue("Unable to parse.\nDictionary edits cancelled.")
        try:
            with open(DICTFILE+".json", "w") as file:      
                json.dump(dictionary, file)
            dialogue("Saved to dictionary.\nRelaunch program to see changes")
        except:
            dialogue("Unknown error handling file")

    global dupli
    spell_error = False
    word = spell.correction(orig_word.lower())
    if word != orig_word.lower():
        spell_error = True
    word = Word(word)
    word_data = dictionary.get(word.word)
    word_copies = find_word(word, word_data)
    if len(word_copies) > 1:            #the dupli flag _dupli represents when a word in the sentence is a copy of another
        dupli = dupli + 1               #it is a unique number for each (word_copies)
    if len(word_copies) >= 1:
        for item in word_copies:
            new_sen_list.append(item)
    else:
        confirm = confirm_change(f"Word not found '{word.word}'\nClick confirm to add to dictionary\nor cancel to continue")
        if confirm == True:
            pos_value = ["article","prep","adv","n","v","adj","det","pron","conj","exclam","modal","number"]
            options, scrll_crit = choice_win(pos_value, add_to_dict)
            options.wait_window()
            add_word(orig_word)
        else:
            no_word = Word("<>", None)
            new_sen_list.append(no_word)
    return spell_error, word.word

def find_word(word, word_data):
    word_duplicates = []
    #the first option is that the word is a root word, so a key in the dictionary
    if word_data:
        if type(word_data[0]) == int:
            for i in range(len(word_data)):
                word_duplicates.append(word.make_dupli())
                word_duplicates[i].set_key(word_data[i])
                word_duplicates[i].pos = dictionary.get(word_data[i])
            word_duplicates.append(word)
        else:
            word_duplicates.append(word)
        for i in range(len(word_duplicates)):
            word = word_duplicates[i]
            word_data = dictionary[word.get_key]
            if type(word_data[0]) == str:
                word.pos = word_data[0]
            else:
                continue
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
                        word.person.s((1,2))
                        word.person.p((1,2,3))
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
        for item in values:
            if type(item[0]) == int:
                pass
            elif item[1] == True:
                if word.word == item[2] or (type(item[2]) == list and word.word in item[2]):
                    index = list(values).index(item)
                    key = list(dictionary.keys())[index]
                    word.pos = item[0]
                    word.set_key(key)
                    if word.word == item[2]:
                        if item[0] == "n":
                            word = Noun(word)
                            word.plural = True
                        word_duplicates.append(word)
                    elif len(item[2]) == 2:
                        word = Adjective(word)
                        if word.word == item[2][0]:
                            word.form = "comparative"
                        elif word.word == item[2][1]:
                            word.form = "superlative"
                        word_duplicates.append(word)
                    else:
                        word = Verb(word)
                        
                        if word.word == item[2][0]:
                            word.tense = "present"
                            word.person.s(1)
                            if len(item[2]) == 4:
                                word.person.s(1,2)
                                word.person.p(1,2,3)
                            word_duplicates.append(word.make_dupli())
                                
                        if word.word == item[2][1]:
                            word.tense = "present"
                            word.person.s(3)
                            word_duplicates.append(word.make_dupli())
                        if word.word == item[2][2]:
                            word.tense = "past"
                            word.person.all()
                            if len(item[2]) > 4:
                                word.person.s(2)
                                word.person.p((1,2,3))
                            word_duplicates.append(word.make_dupli())
                        if word.word == item[2][3]:
                            word.tense = "participle"
                            word.person.all()
                            word_duplicates.append(word.make_dupli())
                        if len(item[2]) > 4:
                            if word.word == item[2][4]:
                                word.tense = "past"
                                word.person.s((1,3))
                                word_duplicates.append(word.make_dupli())
                            if word.word == item[2][5]:
                                word.tense = "present"
                                word.person.s(2)
                                word.person.p((1,2,3))
                                word_duplicates.append(word.make_dupli())

                        #0"am" - Present first person singular - normally the same as key
                        #2"were" - Past second person singular and all persons plural
                        #4"was" - Past first and third person singular
                        #5"are" - Present second person singular and all persons plural
        #
        if len(word_duplicates) < 1:
            #it could also be a regular form of a word
            lemma_var = call_lemma(word.word)
            word_data = []
            for i in range(len(lemma_var)):
                form = lemma_var[i][1]
                lemma_data = dictionary.get(lemma_var[i][0])
                pos = []
                key_temp = []
                if lemma_data and type(lemma_data[0]) == int:
                    colon = form.find(":")
                    if colon !=-1:
                        word = Noun(word)
                        if "plural" in form:
                            word.plural = True
                        else:
                            word.plural = False
                        word_duplicates.append(word.make_dupli())
                        word = Verb(word)
                        word.tense = form[colon+1:len(word.word)-1]  #form = "plural:present3"
                        word.person.s(int(form[len(form)-1])) #here, 3 - always in last char
                    else:
                        for i in lemma_data:
                            pos.append(dictionary(i)[0])
                            key_temp.append(i)

                if lemma_data and lemma_data[1] == False:
                    key = key_temp if key_temp else lemma_var[i][0]
                    form = lemma_var[i][1]
                    lemma_data[0] = pos if pos else lemma_data[0]
                    
                    colon = form.find(":")
                    if colon !=-1:
                        if "v" in lemma_data[0]:
                            word = Verb(word)
                            word.tense = form[colon+1:len(word.word)-1]  #form = "plural:present3"
                            person_int = int(form[len(form)-1]) #here, 3 - always in last char
                            if person_int == 0:
                                word.person.all()
                            else:
                                word.person.s(person_int)
                            word_duplicates.append(word.make_dupli())
                        elif "n" in lemma_data[0]:
                            word = Noun(word)
                            word.plural = True
                            word_duplicates.append(word.make_dupli())
                        else:
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
                                    word.form = form
                                word_duplicates.append(word.make_dupli())

    return word_duplicates

def pos_clean_sva(sentence):  #sentence in this function is new_sen_list
    verb_list = [item for item in sentence.get_verb]
    verb_definite = []
    #false represents that the verb has no possible variations.
    if len(verb_list) > 1:
        #this checks if some of the verbs are actually nouns or something idk
        for i in verb_list:
            if sentence.get_dupli(i)[0] == False:
                verb_definite.append(i)
    if verb_definite:
        if len(verb_definite) == 1:
            verb_list = verb_definite
    all_errors_list, new_sentence = find_error_list(sentence)
    auxiliary_errors, sentence    = auxiliary_verb(new_sentence)
    sva_errors, new_sentence      = subject_verb_error(new_sentence)
    verb_errors = sva_errors + auxiliary_errors
    if verb_errors > 0:
        all_errors_list.append(('SVAgreement', verb_errors))

    return all_errors_list, new_sentence

def auxiliary_verb(sentence):
    verbs = sentence.get_verb
    a_verbs = [verbs[i] for i in range(1, len(verbs)-1) if verbs[i-1]==(verbs[i]-1)]
    auxiliary_errors = 0
    for i in a_verbs:
        if sentence[i].tense != "participle":
            verb_data = dictionary[sentence[i].get_key]
            if verb_data[1] == True:
                new_word = Verb(Word(verb_data[2][3], key))
            else:
                key = sentence[i].get_key
                if type(key) == int:
                    values = dictionary.values()
                    for i in len(values):
                        if key in values[i]:
                            new_word = Verb(Word( dictionary.keys()[i], key))
                            break
                else:
                    new_word = Verb(Word(key))
            new_word.person.all()
            new_word.tense = "participle"
            sentence[i] = new_word
            auxiliary_errors = auxiliary_errors + 1
    return auxiliary_errors, sentence

def subject_verb_error(sentence):
    verbs = sentence.get_verb
    nouns = sentence.get_pos("n") + sentence.get_pos("pronoun")
    nouns.sort()
    sva_errors = 0
    for i in verbs:
        if sentence[i].tense in ("past","present"):
            noun_i = [j for j in nouns if j < i]
            nouns = [j for j in nouns if j > i]
            if noun_i:
                person_verb = 3
                if len(noun_i) > 1:
                    plural_verb = True
                else:
                    subject = sentence[noun_i[0]]
                    if subject.pos == "pron":
                        if subject.word == "i":
                            person_verb = 1
                        elif subject.word == "you":
                            person_verb = 2
                    if subject.plural == True:
                        plural_verb = True
                    else:
                        plural_verb = False
                if (plural_verb == True and person_verb not in sentence[i].person.plural) or (plural_verb == False and person_verb not in sentence[i].person.singular):
                    key = sentence[i].get_key
                    verb_data = dictionary[key]
                    if verb_data[1] == True:
                        if key != "be":
                            if sentence[i].tense == "present":
                                if plural_verb == False and person_verb == 3:
                                    new_word = Verb(Word(verb_data[2][1], key))
                                    new_word.person.s(3)
                                else:
                                    new_word = Verb(Word(verb_data[2][0], key))
                                    new_word.person.s(1,2)
                                    new_word.person.p(1,2,3)
                            elif sentence[i].tense == "past":
                                new_word = Verb(Word(verb_data[2][2], key))
                                new_word.person.all()
                        else:
                            if sentence[i].tense == "present":
                                if plural_verb == False and person_verb == 1:
                                    new_word = Verb(Word(verb_data[2][0], key))
                                    new_word.person.s(1)
                                elif plural_verb == False and person_verb == 3:
                                    new_word = Verb(Word(verb_data[2][1], key))
                                    new_word.person.s(3)
                                else:
                                    new_word = Verb(Word(verb_data[2][5], key))
                                    new_word.person.s(2)
                                    new_word.person.p(1,2,3)
                            elif sentence[i].tense == "past":
                                if plural_verb == False and person_verb in (1,3):
                                    new_word = Verb(Word(verb_data[2][0], key))
                                    new_word.person.s(person_verb)
                                else:
                                    new_word = Verb(Word(verb_data[2][4], key))
                                    new_word.person.s(2)
                                    new_word.person.p(1,2,3)
                    else:
                        if sentence[i].tense == "present":
                            if type(key) == int:
                                values = dictionary.values()
                                for i in len(values):
                                    if key in values[i]:
                                        verb_lemma = dictionary.keys()[i]
                                        break
                            else:
                                verb_lemma = key
                            if plural_verb == False and person_verb == 3:
                                new_word = Verb(Word(verb_lemma+"s", key))
                                new_word.person.s(3)
                            else:
                                new_word = Verb(Word(verb_lemma, key))
                                new_word.person.s(1,2)
                                new_word.person.p(1,2,3)
                    sentence[i] = new_word
                    sva_errors = sva_errors + 1

    return sva_errors, sentence
#       #present participle past infinitive
#       #["am",     "is",       "were",     "been",     "was", "are"]
#       #["become", "becomes",  "became",   "become"]
#present#  allbut   3
#pres be#  1        3                                           2plural123
#pastreg#                       all          participle
#past be#                       2/plural123  participle  13
#       #["add",    "adds",     "added"   
#       #  allbut   3           allpast/participle


def find_error_list(sentence, Continue=True):
    global all_patterns
    pos_list = " "
    for i in sentence:
        if i.pos == "article":
            i.pos = "det"
        elif i.pos == "":
            continue
        pos_list = pos_list + str(i.pos) + " "
    all_errors = []
    err_positions_list = []
    for j in all_patterns:
        if j[0].findall(pos_list):
            if 'Repeated' in j[2]:
                if j[1].findall(pos_list):
                    all_errors.append(j[2])
                    position_of_error = [(item.start(), item.end()) for item in j[1].finditer(pos_list)]
                    err_positions_list.append(position_of_error)
            elif len(j[1].findall(pos_list)) < len(j[0].findall(pos_list)):
                all_errors.append(j[2])
                position_of_error = [(item.start(), item.end()) for item in j[0].finditer(pos_list) 
                                         if (item.start(), item.end()) not in [(match.start(), match.end()) 
                                                                               for match in j[1].finditer(pos_list)]]
                err_positions_list.append(position_of_error)
    if Continue == True:
        x, new_sentence = correct_sva(all_errors, err_positions_list, pos_list, sentence)

        all_errors_hold = [(all_errors[i], len(err_positions_list[i])) for i in range(len(all_errors))]
        return all_errors_hold, new_sentence
    else:
        return all_errors, err_positions_list, pos_list

#this function does a simple check to see if the correction was helpful
def continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list):
    if not new_errors or not new_errors[index]:
        all_errors, err_positions, pos_list = new_errors, new_err_pos, new_pos_list 
        continue_true = True
    elif (all_errors[index] != new_errors[index]) or (len(new_err_pos[index]) < len(err_positions[index])):
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
        err_pos_obj = err_positions[index]
        while err_pos_obj:
            continue_true = False
            if err_positions:
                err_pos_obj = err_positions[index][0]
            else:
                break
            #this finds the index of the error in the Sentence obj
            err_pos = pos_list[:err_pos_obj[0]].count(" ") - 1
            err_pos_2 = pos_list[:err_pos_obj[1]].count(" ") - 1
            match all_errors[index]:
                case 'Determiners':
                    if sentence[err_pos-1].pos == "n":
                        if sentence[err_pos-2] != "det":
                            temp_word = sentence[err_pos]
                            del sentence[err_pos]
                            sentence.insert(err_pos-1, temp_word)
                            new_errors, new_err_pos, new_pos_list = find_error_list(sentence, False)
                            continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    else:
                        later_verb_list = [i for i in sentence.get_verb if i > err_pos]
                        if later_verb_list:
                            this_verb = sentence[sentence.get_verb[sentence.get_verb.index(later_verb_list[0])]]
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
                            sentence[err_pos] = new_word
                            all_errors, err_positions, pos_list = find_error_list(sentence, False)
                            continue_true = True
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos]
                        all_errors, err_positions, pos_list = find_error_list(sentence, False)
                case 'Adjectives':
                    if sentence[err_pos-1].pos == "n":
                        temp_word = sentence[err_pos]
                        del sentence[err_pos]
                        sentence.insert(err_pos-1, temp_word)
                        new_errors, new_err_pos, new_pos_list = find_error_list(sentence, False)
                        continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos]
                        all_errors, err_positions, pos_list = find_error_list(sentence, False)
                case 'Adverbs':
                    if sentence[err_pos-1].pos == "v":
                        temp_word = sentence[err_pos]
                        del sentence[err_pos]
                        sentence.insert(err_pos-1, temp_word)
                        new_errors, new_err_pos, new_pos_list = find_error_list(sentence, False)
                        continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos]
                        all_errors, err_positions, pos_list = find_error_list(sentence, False)

                case 'verbHasSubject':
                    if "n" in pos_list:
                        noun_pos = pos_list[:pos_list.index("n")].count(" ") - 1
                        sentence.insert(noun_pos + 1, sentence[err_pos])
                        del sentence[err_pos]
                        new_errors, new_err_pos, new_pos_list = find_error_list(sentence, False)
                        continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos]
                        all_errors, err_positions, pos_list = find_error_list(sentence, False)

                case 'verbRepeated':
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
                    all_errors, err_positions, pos_list = find_error_list(sentence, False)
                case 'nounRepeated':
                    new_word = Word("and")
                    sentence.insert(err_pos+1,new_word)
                    all_errors, err_positions, pos_list = find_error_list(sentence, False)
                case 'Prepositions':
                    if sentence[err_pos-1].pos == "n":
                        if sentence[err_pos-2].pos == "det" and sentence[err_pos-3] != "prep":
                                temp_word = sentence[err_pos]
                                del sentence[err_pos]
                                sentence.insert(err_pos-3, temp_word)
                                new_errors, new_err_pos, new_pos_list = find_error_list(sentence, False)
                                continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                        elif sentence[err_pos-2] not in ["prep","det"]:
                                temp_word = sentence[err_pos]
                                del sentence[err_pos]
                                sentence.insert(err_pos-2, temp_word)
                                new_errors, new_err_pos, new_pos_list = find_error_list(sentence, False)
                                continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    
                    elif sentence[err_pos-1].pos == "det" or sentence[err_pos-1].pos == "pron":
                        if sentence[err_pos-2] != "prep":
                            temp_word = sentence[err_pos]
                            del sentence[err_pos]
                            sentence.insert(err_pos-1, temp_word)
                            new_errors, new_err_pos, new_pos_list = find_error_list(sentence, False)
                            continue_true, all_errors, err_positions, pos_list = continue_correction(index, all_errors, err_positions, pos_list, new_errors, new_err_pos, new_pos_list)
                    if continue_true == False:
                        sentence = sentence_hold
                        del sentence[err_pos]
                        all_errors, err_positions, pos_list = find_error_list(sentence, False)
                case _:
                    dialogue("unknown error in sentence")

        if index < len(all_errors)-1:
            index = index + 1
        else:
            index = 0
    return all_errors_hold, sentence

#returns all_errors_list, sentence_new, spell_error_count

def main_algorithm(sentence, lang_dict, lang_patterns, lang_dialogue, lang_confirm_change, lang_choice_win, lang_user_entry):
    global new_sen_list, dictionary, dialogue, confirm_change, choice_win, user_entry, all_patterns
    dictionary = lang_dict
    dialogue = lang_dialogue
    confirm_change = lang_confirm_change
    choice_win = lang_choice_win
    user_entry = lang_user_entry
    all_patterns = lang_patterns
    new_sen_list = Sentence()
    spell_error_count = 0
    words, punctuated_sen = clean_sentence(sentence)
    for word in words:
        spell_error, new_word = add_word(word)
        if spell_error == True:
            spell_error_count = spell_error_count + 1
            #this corrects the spelling of the word in the punctuated list of the sentence
            index_of_word = [item[0] for item in punctuated_sen].index(word)
            punctuated_sen[index_of_word][0] = new_word

    if len(new_sen_list) > 0:   #??
        all_errors_list, sen = pos_clean_sva(new_sen_list)
        sentence_new = ""
        for item in sen:
            if type(word) != str:
                if type(word.word) != str:
                    word = word.word
            sentence_new = sentence_new + " " + item.word
        sentence_new = sentence_new[1].upper()+ sentence_new[2:]+ "."
        sentence_new = sentence_new.replace(" i ", " I ")
        if not sen.get_verb:
            all_errors_list.append("noVerbSubject")
        if sentence_new.replace(".","") == sentence.replace(".",""):
            all_errors_list = None
    return all_errors_list, spell_error_count, sentence_new


'''
dialogue = print
set_connections()
all_patterns = compile_all_patterns()
sentence = input("Please enter a sentence: ")
while sentence == "":
    sentence = input("Please enter a sentence: ")
all_errors_list, sentence_new, spell_error_count = main_algorithm(sentence)
print(all_errors_list, spell_error_count)
print(sentence_new,"\n",sentence)
'''