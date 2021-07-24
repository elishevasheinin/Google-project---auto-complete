import json
import pathlib
import string

my_search_db = {}


def get_folders_from_folder(folder="2021-archive"):
    folders = []
    contents = pathlib.Path(folder).iterdir()
    for content in contents:
        if not content.is_file():
            folders.append(content)
    return folders


def get_files_of_folder(folder="2021-archive"):
    files = []
    contents = pathlib.Path(folder).iterdir()
    for content in contents:
        if content.is_file():
            files.append(content)
    return files


def get_word_without_punctuation(word):
    punctuations = string.punctuation
    no_punct = ""
    for char in word:
        if char not in punctuations:
            no_punct = no_punct + char
    fix_word = no_punct.lower()
    return fix_word


def restart(data_file):
    name_file = data_file[0]
    list_sentences = data_file[1]
    global my_search_db
    for sentence in list_sentences:
        for word in sentence.split(" "):
            old_word = word
            word = get_word_without_punctuation(word)
            try:
                if sentence not in my_search_db[word]["sentences"] and len(my_search_db[word]["sentences"]) < 5:
                    my_search_db[word]["sentences"].append(
                        "{} ({} {})".format(sentence.strip(), name_file, list_sentences.index(sentence)))
            except:
                my_search_db[word] = {}
                my_search_db[word]["sentences"] = ["{} ({} {})".format(
                    sentence.strip(), name_file, list_sentences.index(sentence))]
            cont_sentence = sentence[sentence.index(old_word) + len(old_word) + 1:]
            i = 0
            db_dict = my_search_db[word]
            while i < len(cont_sentence.split(" ")):
                next_word = cont_sentence.split(" ")[i]
                next_word = get_word_without_punctuation(next_word)
                try:
                    if sentence not in db_dict[next_word]["sentences"] and len(db_dict[next_word]["sentences"]) < 5:
                        db_dict[next_word]["sentences"].append("{}({} {})".format(
                            sentence.strip(), name_file, list_sentences.index(sentence)))
                except:
                    db_dict[next_word] = {}
                    db_dict[next_word]["sentences"] = ["{} ({} {})".format(
                        sentence.strip(), name_file, list_sentences.index(sentence))]
                db_dict = db_dict[next_word]
                i += 1



def get_files_content_from_folder(folder_name="2021-archive"):
    files_names = get_files_of_folder(folder_name)
    for file_name in files_names:
        with open(file_name, encoding='utf8') as f:
            lines = f.read().splitlines()
            file_content = [file_name, lines]
            restart(file_content)

def open_folders(folder_name="2021-archive"):
    global my_search_db
    files_content = get_folders_from_folder(folder_name)
    folder_content = get_folders_from_folder("{}".format(files_content[0]))
    for folder in folder_content:
        get_files_content_from_folder("{}".format(folder))
    # get_files_content_from_folder("{}".format(files_content[1]))
    with open("my_db1.json", "w", encoding='utf8') as f:
        json.dump(my_search_db, f)

# open_folders()
