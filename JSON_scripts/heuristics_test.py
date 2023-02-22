import json
from spellchecker import SpellChecker
import string

text = input()

spell = SpellChecker()

#with open(text_file, "r") as file:            
#    text = text_file.read()
#table = str.maketrans('', '', "!\"#$%&'()*+, -.:;<=>?@[]^_`{|}~")
print(text)

translation = {
    "!" : ' ', "," : ' ', "." : ' ', ":" : " ", "_" : " ", "-" : ' ', "^" : ' ',
    "\u2014" : ' ', "\u2019" : "\'" 
}

trans1 = "!\"#$%&'()*+,-.:;<=>?@[]^_`{|}~\u2014\u2019"
trans2 = "                               \'"

text = str(bytes(text, "utf-8").decode("unicode_escape"))
table = str.maketrans(trans1, trans2)
text = text.translate(table)
words = text.split()
#words_edited = []
#for word in words:
    #print(word)
    #new_words = word.split()
    #for new_word in new_words:
    #    words_edited.append(new_word)

misspelled = spell.unknown(words)



print(misspelled)

total = len(words)
wrong = len(misspelled)
ratio = 1 - (wrong/total)

print(ratio)