from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from utils import process_input, create_score_message
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import csv
import os
import random
from prompt import unified_prompt, gpt4

# load in OpenAI API key
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("OPENAI_API_KEY")

# folder 'uploads' should be in the root directory
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "7843dfhjbsiursuv4r7n4e8yvni8409"
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Question('{self.text}', '{self.option1}', '{self.option2}', '{self.option3}', '{self.option4}', '{self.correct_answer}')"


with app.app_context():
    db.create_all()

# landing page
@app.route('/')
def index():
    return render_template('index.html')

# page to display stored questions
@app.route('/display_questions')
def display_questions():
    # retrieve questions from database
    questions = Question.query.all()
    # print(questions)
    return render_template('display_questions.html', questions=questions)

@app.route('/delete_question/<int:qid>', methods=['POST', 'GET'])
def delete_question(qid):
    # delete a question from the database
    question = Question.query.get(qid)
    db.session.delete(question)
    db.session.commit()
    return redirect('/display_questions')


# processes the input words after submitting the form
@app.route('/save_words', methods=['POST'])
def save_words():
    words = []  # Initialize the words list
    # Check if a file is present in the request
    file = request.files.get('file')
    if file and file.filename != '':
        if file.filename.endswith('.csv'): # Check if it is a CSV file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            with open(filepath, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    words.extend(row)  # Assuming each row contains one word
        else:
            return "Unsupported file format", 415
    else:
        # When no file is uploaded, process the text input
        words_text = request.form.get('words', '')
        if words_text:
            words = process_input(words_text)

    # If no words are provided
    if not words:
        return "No words provided", 400

    # store words in session
    # print("STORED:", words)
    session['words'] = words

    # split by word
    model_response = gpt4(unified_prompt(session['words'])).split("\n\n")

    # split into question and answer choices
    model_response = [q.split("\n") for q in model_response]

    # remove number from question if present (example: 1. how are you? -> how are you?)
    model_response = [[q[0].split(".")[1].strip()] + q[1:] for q in model_response]


    # package questions and send to page
    old_questions = [{"question": q[0].replace(session['words'][i], "__________"),
                      "options": random.sample([_.strip().split(" ")[-1] for _ in q[1:]] + [session['words'][i]],
                                               len(q)),
                      "answer": session['words'][i]} for i, q in enumerate(model_response)]
    db_questions = [Question(text=q["question"],
                             option1=q["options"][0],
                             option2=q["options"][1],
                             option3=q["options"][2],
                             option4=q["options"][3],
                             correct_answer=q["answer"]) for q in old_questions]
    db.session.add_all(db_questions)
    db.session.commit()
    # store questions
    session['questions'] = [{"id": i,
                             "answer": question["answer"],
                             "question": question["question"],
                             "options": question["options"]}
                            for i, question in enumerate(old_questions)]

    # display answer choices to user
    words_options = [(w, " ".join(o["options"]).replace(o["answer"], "")) for w, o in zip(words, old_questions)]

    return render_template('display_words.html', word_synonyms_pairs=words_options)


@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    # generate quiz from stored questions
    if 'questions' not in session:
        questions = []
    else:
        questions = session['questions']
    return render_template('quiz.html', questions=questions)

@app.route('/saved_quiz', methods=['POST'])
def saved_quiz():
    responses = []
    # print(request.form.keys())
    for key in request.form.keys():
        if key.startswith('add'):
            responses.append(request.form.getlist(key)[0])

    # create a quiz with the questions with the IDs in responses from sqlite
    db_questions = Question.query.all()
    # for q in db_questions:
        # print(q.id)
    # print(responses)
    questions = [{"id": i,
                  "question": q.text,
                  "options": [q.option1, q.option2, q.option3, q.option4],
                  "answer": q.correct_answer} for i, q in enumerate(db_questions) if str(q.id) in responses]
    session['questions'] = questions

    return render_template('quiz.html', questions=questions)


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    # Calculate the score and gather feedback
    score = 0
    feedback = []
    for i, question in enumerate(session['questions']):
        user_answer = request.form.get(f'question{question["id"]}')
        is_correct = user_answer == question['answer']
        if is_correct:
            score += 1
        feedback.append({
            'question': question['question'],
            'options': question['options'],
            'user_answer': user_answer,
            'is_correct': is_correct
        })

    total_questions = len(session['questions'])
    message = create_score_message(score, total_questions)

    return render_template('score.html', score=score, total=total_questions, message=message, feedback=feedback)


if __name__ == '__main__':
    app.run(debug=True)
