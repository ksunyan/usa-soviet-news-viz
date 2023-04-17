from nltk.tokenize import RegexpTokenizer
from nltk.corpus import brown
from os import path, walk, environ
from argparse import ArgumentParser
from datetime import date
import sqlite3
import config

# Helper functions

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

def count_keyword(token, lccn, date, ed, seq, occurrence_list, keywords):
    if(token in keywords):
        occurrence_list.append({
            "string":token,
            "date":date,
            "lccn":lccn,
            "ed":ed,
            "seq":seq
        })

def date_from_path(filepath):
    m = metadata_from_path(filepath)
    return date(int(m[1]), int(m[2]), int(m[3]))

def metadata_from_path(filepath):
    """Given a filepath to a directory containing an ocr.txt file, 
    returns a list of the last 6 directories in the filepath.
    These correspond to the LCCN, year, month, day, edition, and sequence
    values for that ocr.txt file."""
    metadata = ['']*6
    for i in range(6):
        head_tail = path.split(filepath)
        filepath = head_tail[0]
        metadata[5-i] = head_tail[1]
    return metadata

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
    db_cur.execute("CREATE TABLE IF NOT EXISTS occurrence("
    "string, date, lccn, ed, seq)")
    db_cur.execute("CREATE TABLE IF NOT EXISTS source("
    "filepath, month, num_tokens)")

    # Load keywords (if enabled)
    if(args.keywords):
        with open(args.keywords) as fp:
            keywords = set(line.strip() for line in fp)

    # Load in English corpus
    corpus = set(brown.words())
    corpus = corpus.union(keywords)

    # Traverse the subdirectories of root and tokenize
    token_counts = {}
    tokenized_files = []
    keyword_occurrences = []
    tokenizer = RegexpTokenizer(r'[a-zA-Z\-]+')
    for root, dirs, files in walk(args.root):
        if 'ocr.txt' in files:
            filedate = date_from_path(root)
            filename = path.join(root, 'ocr.txt')
            filemetadata = metadata_from_path(root)
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
                        # Case 2: The next token is a newline (check spanning token validity)
                        elif(tokens[ptr+1] == '\n'):
                            spanning_token = tokens[ptr] + tokens[ptr+2]
                            if(count_token(spanning_token, filedate, token_counts, corpus)):
                                if(args.keywords):
                                    count_keyword(spanning_token, 
                                        filemetadata[0], 
                                        filedate,
                                        filemetadata[4],
                                        filemetadata[5], 
                                        keyword_occurrences, 
                                        keywords)
                                ptr += 3
                            else:
                                count_token(tokens[ptr], filedate, token_counts, corpus)
                                if(args.keywords):
                                    count_keyword(tokens[ptr], 
                                        filemetadata[0], 
                                        filedate,
                                        filemetadata[4],
                                        filemetadata[5], 
                                        keyword_occurrences, 
                                        keywords)
                                ptr += 2
                        # Case 3: Neither the current nor the next token is a newline
                        else:
                            count_token(tokens[ptr], filedate, token_counts, corpus)
                            if(args.keywords):
                                    count_keyword(tokens[ptr], 
                                        filemetadata[0], 
                                        filedate,
                                        filemetadata[4],
                                        filemetadata[5], 
                                        keyword_occurrences, 
                                        keywords)
                            ptr += 1
                    # Handle the final token (unless it was already handled as part of
                    # a spanning token). 
                    if(tokens[ptr] != '\n'):
                        count_token(tokens[ptr], filedate, token_counts, corpus)
                        if(args.keywords):
                                    count_keyword(tokens[ptr], 
                                        filemetadata[0], 
                                        filedate,
                                        filemetadata[4],
                                        filemetadata[5], 
                                        keyword_occurrences, 
                                        keywords)
            # Count total number of valid tokens in file 
            count_sum = sum(token_counts.values()) 
            # Add to our running list of processed files
            tokenized_files.append({
                "filepath":filename, 
                "month":filedate.replace(day=1), 
                "num_tokens":count_sum})

    # Write to database
    print("Writing data to database")

    val =[{
            "string":k[0], 
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

    val = keyword_occurrences
    sql = ("INSERT INTO occurrence "
            "(string, date, lccn, ed, seq) "
            "VALUES(:string, :date, :lccn, :ed, :seq)")
    
    for i in range(0, len(val), 100):
        print("Executing from: " + str(i))
        db_cur.executemany(sql,val[i:i+100])

    db_con.commit()
