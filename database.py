'''
This script will handle saving and retrieving data.
This is a part of answers_assistant.py project.

Developer: Irfan Ahmad
github: https://github.com/irfan-ahmad-byte/
fiverr: https://www.fiverr.com/irfanmlka
twitter: https://twitter.com/IrfanAhmad1707
date: July 3, 2022
'''


import sqlite3 as sql
from sqlite3 import Error
import spacy
import nltk
import subprocess

try:
    from nltk.corpus import stopwords
except:
    nltk.download("stopwords")
    nltk.download("wordnet")
    from nltk.corpus import stopwords

try:
    nlp = spacy.load("en_core_web_sm")        
    stop_words = set(stopwords.words("english"))
except:
    subprocess.run("python -m spacy download en_core_web_sm", shell=True)
    nlp = spacy.load("en_core_web_sm")        
    stop_words = set(stopwords.words("english"))


def dbconnect(db_file):
    # '''create a database connection'''
    conn = None
    try:
        conn = sql.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
    
def save_ans(conn, data:tuple):
    '''
    function to save question and answer in the database
    '''
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO questions(question, answer) VALUES(?, ?)''', data)
        conn.commit()
        return 'Question and answer saved.'
    except Error as e:
        print(e)
        return 'Something went wrong while saving data'

def clean_query(query:str) -> set:
    '''
    function to tokenize and clean a question from stop words
    '''

    quest_nlp = nlp(query)
    lemmatized_question = [token.lemma_ for token in quest_nlp]
    cleaned_question = [word for word in lemmatized_question if word.casefold() not in stop_words]  # remove stop words from the question

    return set(cleaned_question)

def get_ans(conn, question:str) -> str:
    '''
    function to get answer of the query/question
    '''
    ans = None
    data = (question,)
    cleaned_question = clean_query(question)  # remove stop words from the question
    try:
        cleaned_question.remove('?')
    except:
        ...
    # print('========>: ', cleaned_question)
    cur = conn.cursor()
    # cur.execute('''SELECT answer FROM questions WHERE question=?''', data)
    cur.execute('''SELECT question FROM questions''')
    conn.commit()
    questions = cur.fetchall()
    q_map = {}
    for qu in questions:
        question_tokens = clean_query(qu[0].lower())
        try:
            question_tokens.remove('?')
        except:
            ...
        # print('************=>: ', question_tokens)
        if question_tokens==cleaned_question:
            try:
                cur.execute('''SELECT answer FROM questions WHERE question=?''', qu)
                ans = cur.fetchone()[0]
                return ans
            except Error as e:
                print(e)
                return 'Something went wrong while getting your answer, try again.'
    if not ans:
        ans = 'No answer was found for your question. Perhaps you did not save an answer.'
    return ans

def create_table(conn, table):
    # '''create table in the database'''
    try:
        cur = conn.cursor()
        cur.execute(table)
    except:
        print('problem creating table')

# if __name__ == "__main__":
#     table = '''CREATE TABLE IF NOT EXISTS questions(
#                 id integer PRIMARY KEY,
#                 question text NOT NUll,
#                 answer text NOT NUll);
#                 '''
#     conn = dbconnect('database/questions.db')
#     with conn:
#         if conn is not None:
#             create_table(conn, table)
#             print('table created')
