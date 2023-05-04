import spacy
from os import path, walk

nlp = spacy.load("en_core_web_sm")

token_counts = {}
for root, dirs, files in walk('/Volumes/Alpha/evening-star/1917/10/15'):
    if 'ocr.txt' in files:
        filename = path.join(root, 'ocr.txt')
        print(filename)
        with open(filename) as fp:
            doc = nlp(fp.read())
            for token in doc:
                if(token.text in token_counts):
                    token_counts[token.text] += 1
                else:
                    token_counts[token.text] = 0

sorted_t_counts = sorted(token_counts.items(), key=lambda x:x[1], reverse=True)

for i in range(250):
    print("Rank " + str(i+1) + ": " + str(sorted_t_counts[i]))