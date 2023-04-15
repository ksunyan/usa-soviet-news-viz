from flask import Flask, render_template
import mysql.connector

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
