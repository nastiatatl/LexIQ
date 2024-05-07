import random

from flask import Flask, render_template, request, session
from utils import process_input, create_score_message
from werkzeug.utils import secure_filename
import csv
import os
from dotenv import load_dotenv

from prompt import gpt3_5, unified_prompt, gpt4

# load in OpenAI API key
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("OPENAI_API_KEY")

# folder 'uploads' should be in the root directory
app.config['UPLOAD_FOLDER'] = 'uploads'

# landing page
@app.route('/')
def index():
    return render_template('index.html')

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
    print("STORED:", words)
    session['words'] = words

    # split by word
    model_response = gpt4(unified_prompt(session['words'])).split("\n\n")

    # split into question and answer choices
    model_response = [q.split("\n") for q in model_response]

    # package questions and send to page
    old_questions = [{"question": q[0].replace(session['words'][i], "__________"),
                      "options": random.sample([_.strip().split(" ")[-1] for _ in q[1:]] + [session['words'][i]],
                                               len(q)),
                      "answer": session['words'][i]} for i, q in enumerate(model_response)]

    # store questions
    session['questions'] = [{"id": i,
                             "data": question,
                             "answer": question["answer"],
                             "question": question["question"],
                             "options": question["options"]}
                            for i, question in enumerate(old_questions)]

    # display answer choices to user
    words_options = [(w, " ".join(o["options"]).replace(o["answer"], "")) for w, o in zip(words, old_questions)]

    return render_template('display_words.html', word_synonyms_pairs=words_options)

@app.route('/quiz', methods=['POST', 'GET'])
def generate_quiz():
    # generate quiz from stored questions
    questions = session['questions']
    return render_template('quiz.html', questions=questions)


@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    # Calculate the score and gather feedback
    score = 0
    feedback = []
    for i, question in enumerate(session['questions']):
        user_answer = request.form.get(f'question{i}')
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
