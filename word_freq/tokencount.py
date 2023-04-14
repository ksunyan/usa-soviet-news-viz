from nltk.tokenize import RegexpTokenizer
from nltk.corpus import brown
from os import path, walk, environ
from argparse import ArgumentParser
from datetime import date
import sqlite3
import config


def count_token(token, date, token_dict, corpus):
    """Checks if a token is valid (is in a corpus or begins with a capital
    letter) and updates a dictionary of token counts accordingly. Returns
    True if the token is valid and False otherwise.
    
    Keyword arguments:
    token -- the token to be checked and counted
    date -- date object representing the date of token occurrence
    token_dict -- dict containing count values for keys of format (token,date)
    corpus -- the corpus of valid words
    """
    if((token in corpus) or (token[0].isupper())):
        if((token, date) in token_dict):
            token_dict[(token, date)] += 1
        else:
            token_dict[(token, date)] = 1
        return True
    else:
        return False

def date_from_path(filepath):
    for i in range(2):
        filepath = path.split(filepath)[0]
    date_list = []
    for i in range(3):
        head_tail = path.split(filepath)
        date_list.append(int(head_tail[1]))
        filepath = head_tail[0]
    return date(date_list[2], date_list[1], date_list[0])

def lccn_from_path(filepath):
    for i in range(5):
        filepath = path.split(filepath)[0]
    head_tail = path.split(filepath)
    return head_tail[1]

if __name__ == "__main__":

    # Command line interface
    parser = ArgumentParser()
    
    parser.add_argument('root')
    parser.add_argument('-k','--keywords')

    args = parser.parse_args()

    # Connect to database
    db_con = sqlite3.connect('ChronAmWords.db')
    db_cur = db_con.cursor()

    # Create database tables if they don't already exist
    db_cur.execute("CREATE TABLE IF NOT EXISTS token("
    "string, month, count, "
    "PRIMARY KEY (string, month))")
    # db_cur.execute("CREATE TABLE IF NOT EXISTS occurrence("
    # "string, date, newspaper_id, ed, seq, snippet, "
    # "PRIMARY KEY (string, date))")
    db_cur.execute("CREATE TABLE IF NOT EXISTS source("
    "filepath, month, num_tokens)")

    # Load keywords (if enabled)
    if(args.keywords):
        with open(args.keywords) as fp:
            keywords = set(line.strip() for line in fp)

    # Load in English corpus
    corpus = set(brown.words())

    # Traverse the subdirectories of root and tokenize
    token_counts = {}
    tokenized_files = []
    tokenizer = RegexpTokenizer(r'[a-zA-Z\-]+')
    for root, dirs, files in walk(args.root):
        if 'ocr.txt' in files:
            filedate = date_from_path(root)
            filename = path.join(root, 'ocr.txt')
            print(filename)
            with open(filename) as fp:
                # Algorithm to resolve words that span two lines
                tokens = []
                # Tokenize every line, skipping empty lines. 
                # Reintroduce newline characters between lines. 
                for line in fp:
                    t = tokenizer.tokenize(line)
                    if t:
                        tokens += t
                        tokens.append('\n')
                if(tokens):
                    ptr = 0
                    while(ptr < len(tokens)-2):
                        # Case 1: The current token is a newline
                        if(tokens[ptr] == '\n'):
                            ptr += 1
                        # Case 2: The next token is a newline (check spanning token)
                        elif(tokens[ptr+1] == '\n'):
                            spanning_token = tokens[ptr] + tokens[ptr+2]
                            if(count_token(spanning_token, filedate, token_counts, corpus)):
                                ptr += 3
                            else:
                                count_token(tokens[ptr], filedate, token_counts, corpus)
                                ptr += 2
                        # Case 3: Neither the current nor the next token is a newline
                        else:
                            count_token(tokens[ptr], filedate, token_counts, corpus)
                            ptr += 1
                    # Handle the final token (unless it was already handled as part of
                    # a spanning token). 
                    if(tokens[ptr] != '\n'):
                        count_token(tokens[ptr], filedate, token_counts, corpus)
            # Count total number of valid tokens in file 
            count_sum = sum(token_counts.values()) 
            # Add to our running list of processed files
            tokenized_files.append({
                "filepath":filename, 
                "month":filedate.replace(day=1), 
                "num_tokens":count_sum})

    # Write to database
    print("Writing to database")
    val =[{
            "string":k[0][:50], 
            "month":k[1].replace(day=1), 
            "count":v} 
        for k,v in token_counts.items()]
    sql = ("INSERT INTO token "
            "(string, month, count) "
            "VALUES(:string, :month, :count) "
            "ON CONFLICT DO UPDATE SET "
            "count=count+token.count")
    
    for i in range(0, len(val), 100):
        print("Executing from: " + str(i))
        db_cur.executemany(sql,val[i:i+100])

    val = tokenized_files
    sql = ("INSERT INTO source "
            "(filepath, month, num_tokens) "
            "VALUES(:filepath, :month, :num_tokens)")
    
    for i in range(0, len(val), 100):
        print("Executing from: " + str(i))
        db_cur.executemany(sql,val[i:i+100])

    db_con.commit()
