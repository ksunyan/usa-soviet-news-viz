from flask import Flask, render_template, request
from datetime import date
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/word-vector")
def word_vector():
    return render_template('heatmap.html')

@app.route("/faq")
def faq():
    return render_template('FAQ.html')

@app.route("/word-frequency")
def word_freq():
    return render_template("word_freq.html")

@app.post("/query")
def word_freq_query():
    data = request.form

    data_type = data['data_type']
    raw_words = data['words']
    datestring1 = data['date1'] + "-01"
    datestring2 = data['date2'] + "-01"

    word_list = [w.strip() for w in raw_words.split(',')]

    db_con = sqlite3.connect('../word_freq/ChronAmWords.db')
    db_cur = db_con.cursor()

    # query the database for monthly totals
    if(data_type == "frequency"):
        pass

    output_array = []
    for word in word_list:
        sql = ("SELECT * FROM token WHERE string='" + word + 
            "' AND (month BETWEEN '" + datestring1 + 
            "' AND '" + datestring2 + "') ORDER BY month ASC")
        print(sql)
        res = db_cur.execute(sql)
        result_array = [{"month":row[1], "value":row[2]} 
            for row in res.fetchall()] 
        output_array.append({"word":word,"series":result_array})

    return {"dataset":output_array, "data_date_range":[datestring1, datestring2]}
