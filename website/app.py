from flask import Flask, render_template, request
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

    raw_words = data['words']
    date1 = data['date1']
    date2 = data['date2']

    word_list = [w.strip() for w in raw_words.split(',')]

    db_con = sqlite3.connect('ChronAmWords.db')
    db_cur = db_con.cursor()

    output_array = []
    for word in word_list:
        sql = ("SELECT * FROM token WHERE string='" + word + "'" )
        res = db_cur.execute(sql)
        result_array = [{"month":row[1], "value":row[2]} for row in res.fetchall()]
        output_array.append({"word":word,"series":result_array})

    return {"dataset":output_array}
