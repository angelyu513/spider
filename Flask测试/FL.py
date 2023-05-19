from flask import Flask, render_template
import csv
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return index()
@app.route('/book')
def book():
    datali = []
    with open("./book.csv", 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        title = next(data)
        for item in data:
            datali.append(item)
    return render_template('book.html',book=datali)
@app.route('/money')
def money():
    return render_template('money.html')
@app.route('/word')
def word():
    return render_template('score.html')
@app.route('/team')
def team():
    return render_template('team.html')
if __name__ =='__main__':
    app.run(debug=True)