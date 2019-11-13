from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from str2json import str2json

import sys
sys.path.insert(0, 'BiDAF')
from model_prediction import predict

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    para = request.form['para']
    Q1 = request.form['Q1']
    Q2 = request.form['Q2']
    Q3 = request.form['Q3']

    questions = [Q1, Q2, Q3]
    try:
        questions = [x for x in questions if x != '']
    except:
        pass
    str2json(para, questions)
    answers = predict()
    return_answer = {}

    for answer_index in range(len(answers)):
        return_answer['ans{}'.format(answer_index+1)] = answers[answer_index]

    return jsonify(return_answer)


if __name__ == '__main__':
    app.run(debug=True)
