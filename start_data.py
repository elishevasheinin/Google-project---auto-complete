import json
from restart import get_word_without_punctuation
my_search_db = {}

def check_cont(db_dict, rest_of_input):
    if len(rest_of_input) > 1:
        try:
            check_cont(db_dict[rest_of_input[0]], rest_of_input[1:])
        except:
            finally_dict = fix_misstake(db_dict, rest_of_input[0], 10, rest_of_input)
            # i = 1
            # while finally_dict == {} and i < len(line_sentence):
            #     finally_dict = fix_misstake(db_dict[line_sentence[i-1]], line_sentence[i], len_search, line_sentence)
            #     i += 1
            if finally_dict == {}:
                return False
            else:
                return True
    else:
        try:
            d=db_dict[rest_of_input[0]]["sentences"]
            return True
        except:
            finally_sentences = fix_last_misstake(db_dict, rest_of_input[0], 10)
            if finally_sentences == []:
                return False
            else:
                return True

def get_score(name_word, len_search, pay_erro_score):
    global input_user
    for c in name_word:
        if c != "*":
            ind = name_word.index(c)
            if ind <= 3:
                score = len_search * 2 - pay_erro_score[ind]
            else:
                score = len_search * 2 - 2
            return score

def add(db_dict, name_word, len_search, flag):
    pay_erro_score = [10, 8, 6, 4]
    state_name = name_word
    for word in db_dict:
        name_word = state_name
        count = 0
        if len(word)+1 == len(name_word):
            for c in word:
                try:
                    ind = name_word.index(c)
                    name_word = name_word[:ind] + "*" + name_word[ind+1:]
                except:
                    count += 1
            if name_word[-1] != "*" or name_word[-2] != "*":
                count += 1
            score = get_score(name_word, len_search, pay_erro_score)
            if count <= 1:
                if flag == -1:
                    return db_dict[word]["sentences"], score
                else:
                    return db_dict[word], score
    return 0

def delete(db_dict, name_word, len_search, flag):
    pay_erro_score = [10, 8, 6, 4]
    state_name = name_word
    for word in db_dict:
        name_word = state_name
        count = 0
        if len(word) - 1 == len(name_word):
            for c in word:
                try:
                    ind = name_word.index(c)
                    if ind + 1 < len(name_word):
                        name_word = name_word[:ind] + "*" + name_word[ind+1:]
                    else:
                        name_word = name_word[:ind] + "*"
                except:
                    ind = word.index(c)
                    name_word = name_word[:ind] + c + name_word[ind:]
            for i in name_word:
                if i != "*":
                    count += 1
                    ind = name_word.index(i)
            if ind <= 3:
                score = len_search * 2 - pay_erro_score[ind]
            else:
                score = len_search * 2 - 2
            if count == 1:
                if flag == -1:
                    return db_dict[word]["sentences"], score
                else:
                    return db_dict[word], score
    return 0

def replace(db_dict, name_word, len_search, flag):
    pay_erro_score = [5, 4, 3, 2]
    state_name = name_word
    ind = 0
    for word in db_dict:
        name_word = state_name
        count = 0
        if len(word) == len(name_word):
            for c in range(len(word)):
                if word[c] != name_word[c]:
                    count += 1
                    ind = c
            if ind <= 3:
                score = len_search * 2 - pay_erro_score[ind]
            else:
                score = len_search * 2 - 1
            if count == 1:
                if flag == -1:
                    return db_dict[word]["sentences"], score
                else:
                    return db_dict[word], score
    return 0

def get_five_best_sentence(array_result):
    array_score = []
    for i in array_result:
        array_score.append(i[1])
    array = []
    while len(array) < len(array_result):
        for i in array_result:
            if i[1] == max(array_score):
                array.append(i)
                ind = array_score.index(i[1])
                array_score[ind] = min(array_score)
    finally_sentences = []
    for sentences in array:
        n = 5 - len(finally_sentences)
        if n > 0:
            if n <= len(sentences[0]):
                finally_sentences += sentences[0][:n]
            else:
                finally_sentences += sentences[0]
    return finally_sentences

def fix_misstake(db_dict, word, len_search,line_sentence):
    all_add = add(db_dict, word, len_search, 0)
    all_delete = delete(db_dict, word, len_search, 0)
    all_replace = replace(db_dict, word, len_search, 0)
    array = [all_add, all_delete, all_replace]
    max_scoure = 0
    finally_dict = {}
    for dict in array:
        if dict != 0 and dict[1] >= max_scoure:
            if check_cont(dict[0], line_sentence[1:]):
                max_scoure = dict[1]
                finally_dict = dict[0]
    return finally_dict

def fix_last_misstake(db_dict, word, len_search):
    add_sentences = add(db_dict,word, len_search, -1)
    delete_sentences = delete(db_dict, word, len_search, -1)
    replace_sentences = replace(db_dict, word, len_search, -1)
    array = []
    array_result = [add_sentences, delete_sentences, replace_sentences]
    for i in array_result:
        if i != 0:
            array.append(i)
    return array

def read_db():
    global my_search_db
    with open("my_db1.json", "r") as f:
        my_search_db = json.load(f)

def search_interface():
    print("Loading the files and preparing the system...")
    read_db()
    while True:
        print("The system is ready. Enter your text:")
        user_input = input()
        while True:
            search(user_input)
            print(user_input, end='')
            user_new_input = input()
            if user_new_input == '#':
                break
            user_input += user_new_input

def search(user_input):
    print("Here are five suggestions")
    user_input = user_input.split()
    len_search = 0
    fixed_input = []
    for word in user_input:
        fixed_word = get_word_without_punctuation(word)
        len_search += len(fixed_word) + 1
        fixed_input.append(fixed_word)
    get_auto_complete_from_data(my_search_db, fixed_input, len_search - 1)

def get_auto_complete_from_data(db_dict, line_sentence, len_search):
    if len(line_sentence) > 1:
        try:
            if check_cont(db_dict[line_sentence[0]],line_sentence[1:]):
                get_auto_complete_from_data(db_dict[line_sentence[0]], line_sentence[1:], len_search)
            else:
                finally_dict=fix_misstake(db_dict, line_sentence[0], len_search,line_sentence)
                if finally_dict == {}:
                    print("we have no sentence to your searche")
                    return
                get_auto_complete_from_data(finally_dict, line_sentence[1:], len_search)
        except:
            finally_dict = fix_misstake(db_dict, line_sentence[0], len_search,line_sentence)
            if finally_dict=={}:
                print("we have no sentence to your searche")
                return
            get_auto_complete_from_data(finally_dict, line_sentence[1:], len_search)
    else:
        try:
            finally_sentences = db_dict[line_sentence[0]]["sentences"]
            if len(finally_sentences)<5:
                array = fix_last_misstake(db_dict, line_sentence[0], len_search)
                n=5-len(finally_sentences)
                finally_sentences += get_five_best_sentence(array)[:n]
        except:
            array=fix_last_misstake(db_dict, line_sentence[0], len_search)
            finally_sentences = get_five_best_sentence(array)
        for i in range(len(finally_sentences)):
            print(i + 1, ".", finally_sentences[i])


search_interface()
