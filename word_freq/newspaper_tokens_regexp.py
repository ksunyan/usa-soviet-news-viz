from nltk.tokenize import RegexpTokenizer
from nltk.corpus import words, stopwords
from os import path, walk, environ
from argparse import ArgumentParser
from datetime import date
import mysql.connector
import config

def count_token(token, date, token_dict):
    if((token, date) in token_dict):
        token_dict[(token, date)] += 1
    else:
        token_dict[(token, date)] = 1

def date_from_path(filepath):
    for i in range(2):
        filepath = path.split(filepath)[0]
    date_list = []
    for i in range(3):
        head_tail = path.split(filepath)
        date_list.append(int(head_tail[1]))
        filepath = head_tail[0]
    return date(date_list[2], date_list[1], date_list[0])

if __name__ == "__main__":

    # Command line interface
    parser = ArgumentParser()
    
    parser.add_argument('root')
    parser.add_argument('-k','--keywords')

    args = parser.parse_args()

    # Connect to database
    mydb = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
    )
    mycursor = mydb.cursor()

    # Load keywords (if enabled)
    if(args.keywords):
        with open(args.keywords) as fp:
            keywords = set(line.strip() for line in fp)

    # Traverse the subdirectories of root and tokenize
    token_counts = {}
    tokenizer = RegexpTokenizer(r'[a-zA-Z\-]+')
    for root, dirs, files in walk(args.root):
        if 'ocr.txt' in files:
            filedate = date_from_path(root)
            filename = path.join(root, 'ocr.txt')
            print(filename)
            # with open(filename) as fp:
            #     # Algorithm to resolve words that span two lines
            #     tokens = []
            #     # Tokenize every line, skipping empty lines. 
            #     # Reintroduce newline characters between lines. 
            #     for line in fp:
            #         t = tokenizer.tokenize(line)
            #         if t:
            #             tokens += t
            #             tokens.append('\n')
            #     if(tokens):
            #         ptr = 0
            #         while(ptr < len(tokens)-2):
            #             # Case 1: The current token is a newline
            #             if(tokens[ptr] == '\n'):
            #                 ptr += 1
            #             # Case 2: The next token is a newline
            #             elif(tokens[ptr+1] == '\n'):
            #                 spanning_token = tokens[ptr] + tokens[ptr+2]
            #                 if(spanning_token in words.words()):
            #                     count_token(spanning_token, filedate, token_counts)
            #                     ptr += 3
            #                 else: 
            #                     count_token(tokens[ptr], filedate, token_counts)
            #                     ptr += 2
            #             # Case 3: Neither the current nor the next token is a newline
            #             else:
            #                 count_token(tokens[ptr], filedate, token_counts)
            #                 ptr += 1
            #         # Handle the final token (unless it was already handled as part of
            #         # a spanning token). 
            #         if(tokens[ptr] != '\n'):
            #             count_token(tokens[ptr], filedate, token_counts)
            with open(filename) as fp:
                text = fp.read()
                tokens = tokenizer.tokenize(text)
                for token in tokens:
                    count_token(token, filedate, token_counts)


    # Write to database
    print("Writing to database")
    val =[(k[0][:50], k[1], v) for k,v in token_counts.items()]
    sql = ("INSERT INTO token "
            "(string, date, count) "
            "VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE "
            "count=count+VALUES(count)")
    
    for i in range(0, len(val), 100):
        print("Executing from: " + str(i))
        mycursor.executemany(sql,val[i:i+100])

    mydb.commit()


    # sorted_t_counts = sorted(token_counts.items(), key=lambda x:x[1], reverse=True)

    # with open('results.txt','w') as fp:
    #     for i in sorted_t_counts:
    #         fp.write(str(i) + "\n")