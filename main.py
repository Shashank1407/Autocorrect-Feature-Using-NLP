# importing regular expression
import re
# words
w = []
# reading text file
with open('final.txt', 'r', encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\\w+', file_name_data)
 
# vocabulary
main_set = set(w)

# Functions to count the frequency
# of the words in the whole text file
def counting_words(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def prob_cal(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs

# LemmWord: extracting and adding
# root word i.e.Lemma using pattern module
from nltk.stem import WordNetLemmatizer

def LemmWord(word):
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(wd) for wd in word.split()])


# Deleting letters from the words
def DeleteLetter(word):
    delete_list = []
    split_list = []
 
    # considering letters 0 to i then i to -1
    # Leaving the ith letter
    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
 
    for a, b in split_list:
        delete_list.append(a + b[1:])
    return delete_list

# Switching two letters in a word
def Switch_(word):
    split_list = []
    switch_l = []
 
    #creating pair of the words(and breaking them)
    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
     
    #Printint the first word (i.e. a)
    #then replacing the first and second character of b
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_list if len(b) >= 2]
    return switch_l

def Replace_(word):
    split_l = []
    replace_list = []
 
    # Replacing the letter one-by-one from the list of alphs
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    alphs = 'abcdefghijklmnopqrstuvwxyz'
    replace_list = [a + l + (b[1:] if len(b) > 1 else '')
                    for a, b in split_l if b for l in alphs]
    return replace_list

def insert_(word):
    split_l = []
    insert_list = []
 
    # Making pairs of the split words
    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))
 
    # Storing new words in a list
    # But one new character at each location
    alphs = 'abcdefghijklmnopqrstuvwxyz'
    insert_list = [a + l + b for a, b in split_l for l in alphs]
    return insert_list

# Collecting all the words
# in a set(so that no word will repeat)
def colab_1(word, allow_switches=True):
    colab_1 = set()
    colab_1.update(DeleteLetter(word))
    if allow_switches:
        colab_1.update(Switch_(word))
    colab_1.update(Replace_(word))
    colab_1.update(insert_(word))
    return colab_1
 
# collecting words using by allowing switches
def colab_2(word, allow_switches=True):
    colab_2 = set()
    edit_one = colab_1(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = colab_1(w, allow_switches=allow_switches)
            colab_2.update(edit_two)
    return colab_2

# Only storing those values which are in the vocab
def get_corrections(word, probs, vocab, n=2):
    suggested_word = []
    best_suggestion = []
    suggested_word = list(
        (word in vocab and word) or colab_1(word).intersection(vocab)
        or colab_2(word).intersection(
            vocab))
 
    # finding out the words with high frequencies
    best_suggestion = [[s, probs[s]] for s in list(reversed(suggested_word))]
    return best_suggestion

# Input
my_word = input("Enter any word:")
 
# Counting word function
word_count = counting_words(main_set)
 
# Calculating probability
probs = prob_cal(word_count)
 
# only storing correct words
tmp_corrections = get_corrections(my_word, probs, main_set, 2)
for i, word_prob in enumerate(tmp_corrections):
    if(i < 3):
        print(word_prob[0])
    else:
        break
