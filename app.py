from flask import Flask, render_template, request, session
from utils import generate_synonyms, process_input
from werkzeug.utils import secure_filename
import os
import csv

from prompt import gpt3_5, prompt_from_vocab, distinct_prompt_from_vocab

app = Flask(__name__)
app.secret_key = "sdhgfvsjhdfsdyfhgieyrtgeyutg78w4cr5iu3vwntuyw98ytgladygaga"

# folder 'uploads' should be in the root directory
app.config['UPLOAD_FOLDER'] = 'uploads'

# NOTE: questions are hardcoded for now
QUESTIONS = [
    {"question": "The ___ alleyway made her feel uneasy as she walked home late at night.", "options": ["dark", "gloomy", "dim"], "answer": "dark"},
    {"question": "The ___ lighting in the restaurant created a cozy and intimate atmosphere.", "options": ["dim", "gloomy", "dark"], "answer": "dim"},
    {"question": "The weather that day was ___, matching his melancholic mood.", "options": ["gloomy", "dark", "dim"], "answer": "gloomy"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_words', methods=['POST'])
def save_words():
    words = []  # Initialize the words list

    # Check if a file is present in the request
    file = request.files.get('file')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with open(filepath, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                words.extend(row)  # Assuming each row contains one word
    else:
        # When no file is uploaded, process the text input
        words_text = request.form.get('words', '')
        if words_text:
            words = process_input(words_text)

    # Generate synonyms
    synonyms = [generate_synonyms(word) for word in words]
    word_synonyms_pairs = list(zip(words, synonyms))
    # store words in session
    session['words'] = words
    return render_template('display_words.html', word_synonyms_pairs=word_synonyms_pairs)

@app.route('/quiz', methods=['POST', 'GET'])
def generate_quiz():
    #TODO: implement quiz generation, doesnt have to be in this format, thats just for testing
    model_response = gpt3_5(prompt_from_vocab(session['words'])).split("\n")
    questions = [{"question": q.replace(session['words'][i], "__________"), "options": [session['words'][i], generate_synonyms(session['words'][i]), generate_synonyms(session['words'][i])], "answer": session['words'][i]} for i, q in enumerate(model_response)]
    questions = [{"id": i, "data": question} for i, question in enumerate(questions)]
    return render_template('quiz.html', questions=questions)


@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    # Calculate the score and gather feedback
    score = 0
    feedback = []
    for i, question in enumerate(QUESTIONS):
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

    total_questions = len(QUESTIONS)
    percentage = round((score / total_questions) * 100)

    # Determine the message based on the score
    message = "PERFECTION!!!" if score == total_questions else \
              "THAT WAS REALLY GOOD!!!" if percentage >= 75 else \
              "GOOD JOB!!!" if percentage >= 50 else \
              "NOT BAD!!!" if percentage >= 25 else \
              "NEED MORE PRACTICE!!!" if score > 0 else ":("

    return render_template('score.html', score=score, total=total_questions, message=message, feedback=feedback)




if __name__ == '__main__':
    app.run(debug=True)
