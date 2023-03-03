import pickle
import gensim.models
from spellchecker import SpellChecker
from gensim import utils
import tempfile

spell = SpellChecker

class MyCorpus:

    def __init__(self):
        self.translation = {
            #"!" : ' ', "," : ' ', "." : ' ', ":" : " ", "_" : " ", "-" : ' ', "^" : ' ',
            #"\u2014" : ' ', "\u2019" : "\'" 
            "_" : " ", "!" : ' ', ":" : " "
        }
        self.table = str.maketrans(self.translation)
        self.count = 0

        self.stopwords = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves",
             "he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their",
             "theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was",
             "were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and",
             "but","if","or","because","as","until","while","of","at","by","for","with","about","against","between",
             "into","through","during","before","after","above","below","to","from","up","down","in","out","on","off",
             "over","under","again","further","then","once","here","there","when","where","why","how","all","any","both",
             "each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very",
             "s","t","can","will","just","don","should","now"
            ]

    def __iter__(self):
        for line in corpus_input:
            self.count += 1
            if self.count % 1000 == 0:
                print(self.count)
            yield utils.simple_preprocess(line)

            #line = self.tokenize(line, self.table)


    def tokenize(line, table):
        text = line.translate(table)
        words = spell.split_words(text)


corpus = input()

with open(corpus, "rb") as file:
    corpus_input = pickle.load(file)
    print("loaded")
    print(len(corpus_input))

processed_text = MyCorpus()

model = gensim.models.Word2Vec(sentences=processed_text, vector_size=200)

with tempfile.NamedTemporaryFile(prefix='gensim-model-', delete=False) as tmp:
    temporary_filepath = tmp.name
    print(temporary_filepath)
    model.save(temporary_filepath)

#with open("word2vec_model_" + )
