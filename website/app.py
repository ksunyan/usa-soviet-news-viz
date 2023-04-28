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
        val = {"datestring1":datestring1, "datestring2":datestring2}
        sql = ("SELECT month, SUM(num_tokens) as sum_tokens FROM source "
            "WHERE (month BETWEEN :datestring1 AND :datestring2)"
            "GROUP BY month")
        res = db_cur.execute(sql, val)
        monthly_totals = {row[0]:row[1] for row in res.fetchall()}

    output_array = []
    for word in word_list:
        val = {
            "word":word,
            "datestring1":datestring1,
            "datestring2":datestring2
        }
        sql = ("SELECT * FROM token WHERE string=:word "
            "AND (month BETWEEN :datestring1 AND :datestring2) "
            "ORDER BY month ASC")
        res = db_cur.execute(sql, val)
        if(data_type == "frequency"):
            result_array = [{"month":row[1], "value":100 * row[2]/(monthly_totals[row[1]])} 
                for row in res.fetchall()]
        else:
            result_array = [{"month":row[1], "value":row[2]} 
                for row in res.fetchall()] 
        output_array.append({"word":word,"series":result_array})

    return {"dataset":output_array, 
        "data_date_range":[datestring1, datestring2], 
        "data_type":data_type}

@app.post("/metadata")
def retrieve_metadata():
    data = request.form

    word = data['word']
    month = data['month'][:7]
    print(month)

    db_con = sqlite3.connect('../word_freq/ChronAmWords.db')
    db_cur = db_con.cursor()

    val = {"word":word, "month":month+"___"}
    sql = ("SELECT DISTINCT * FROM occurrence WHERE string=:word "
    "AND date LIKE :month")

    res = db_cur.execute(sql, val)

    result_array = [
        {"date":row[1], 
        "lccn":row[2], 
        "ed":row[3], 
        "seq":row[4]}
        for row in res.fetchall()]

    return {"metadata":result_array}