from nltk.tokenize import RegexpTokenizer
from nltk.corpus import words, stopwords
from os import path, walk, environ
from argparse import ArgumentParser
import mysql.connector

def count_token(token, token_set):
    if(token not in stopwords.words('English')):
        if(token in token_set):
            token_set[token] += 1
        else:
            token_set[token] = 1

if __name__ == "__main__":

    # Command line interface
    parser = ArgumentParser()
    
    # parser.add_argument('db_host')
    # parser.add_argument('db_user')
    # parser.add_argument('db_name')
    parser.add_argument('path')

    args = parser.parse_args()

    # Connect to database
    # mydb = mysql.connector.connect(
    # host=args.db_host,
    # user=args.db_user,
    # password=environ.get('DB_PASSWORD'),
    # database=args.db_name
    # )
    # mycursor = mydb.cursor()

    token_counts = {}

    tokenizer = RegexpTokenizer(r'[a-zA-Z\-]+|\d[\d\,]+|\$[\d\.\,]+|[%&#]')
    for root, dirs, files in walk(args.path):
        if 'ocr.txt' in files:
            filename = path.join(root, 'ocr.txt')
            print(filename)
            with open(filename) as fp:
                # Algorithm to resolve words that span two lines
                token_lines = []
                # 0. Tokenize every line, skipping empty lines
                for line in fp:
                    tkns = tokenizer.tokenize(line)
                    if tkns:
                        token_lines.append(tkns)
                # 1. Count tokens in every line except the last one
                for i in range(len(token_lines) - 1):
                    # 1a. Count all the tokens (except for the last one) in the line 
                    for token in token_lines[i][:-1]:
                        count_token(token, token_counts)
                    # 1b. Check if the boundary tokens form a valid token when concatenated
                    spanning_token = token_lines[i][-1] + token_lines[i+1][0]
                    if(spanning_token in words.words()):
                        count_token(spanning_token, token_counts)
                        token_lines[i+1].pop(0) #removes the first elem of next line
                    else:
                        count_token(token_lines[i][-1], token_counts) #count the last token as a standalone
                # 2. Count the tokens in the last line
                for token in token_lines[-1]:
                    count_token(token, token_counts)

    sorted_t_counts = sorted(token_counts.items(), key=lambda x:x[1], reverse=True)

    with open('results.txt','w') as fp:
        for i in sorted_t_counts:
            fp.write(str(i) + "\n")