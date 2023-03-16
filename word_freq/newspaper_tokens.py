import spacy
from os import path, walk

nlp = spacy.load("en_core_web_sm")

for f in walk('evening-star'):
    print(f)

# filename = "evening-star/1917/10/01/ed-1/seq-1/ocr.txt"

# token_counts = {}

# with open(filename) as fp:
#     doc = nlp(fp.read())

#     for token in doc:
#         if(token.text in token_counts):
#             token_counts[token.text] += 1
#         else:
#             token_counts[token.text] = 0

# sorted_t_counts = sorted(token_counts.items(), key=lambda x:x[1], reverse=True)

# for i in range(100):
#     print("Rank " + str(i+1) + ": " + str(sorted_t_counts[i]))