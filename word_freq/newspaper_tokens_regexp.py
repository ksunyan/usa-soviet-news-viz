from nltk.tokenize import RegexpTokenizer
from os import path, walk

token_counts = {}
tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
for root, dirs, files in walk('/Volumes/Alpha/evening-star/1945'):
    if 'ocr.txt' in files:
        filename = path.join(root, 'ocr.txt')
        print(filename)
        with open(filename) as fp:
            txt = fp.read()
            tokens = tokenizer.tokenize(txt) 
            for token in tokens:
                if(token in token_counts):
                    token_counts[token] += 1
                else:
                    token_counts[token] = 0

sorted_t_counts = sorted(token_counts.items(), key=lambda x:x[1], reverse=True)

with open('results.txt','w') as fp:
    for i in range(10000):
        fp.write("Rank " + str(i+1) + ": " + str(sorted_t_counts[i]) + "\n")