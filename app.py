from flask import Flask, render_template, request
from utils import generate_synonyms, process_input

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_words', methods=['POST'])
def save_words():
    words = process_input(request.form['words'])

    synonyms = []
    for word in words:
        synonyms.append(generate_synonyms(word))

    word_synonyms_pairs = list(zip(words, synonyms))
    return render_template('display_words.html', word_synonyms_pairs=word_synonyms_pairs)

@app.route('/quiz', methods=['POST', 'GET'])
def generate_quiz():
     #TODO: implement quiz generation, doesnt have to be in this format, thats just for testing
    questions = [
        {"question": "The ___ alleyway made her feel uneasy as she walked home late at night.",
         "options": ["dark", "gloomy", "dim"], "answer": "dark"},
        {"question": "The weather that day was ___, matching his melancholic mood.",
         "options": ["gloomy", "dark", "dim"], "answer": "gloomy"},
        {"question": "The ___ lighting in the restaurant created a cozy and intimate atmosphere.",
         "options": ["dim", "gloomy", "dark"], "answer": "dim"}
    ]
    questions = [{"id": i, "data": question} for i, question in enumerate(questions)]
    return render_template('quiz.html', questions=questions)


@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    # NOTE: questions are hardcoded for now
    questions = [
        {"question": "The ___ alleyway made her feel uneasy as she walked home late at night.", "options": ["dark", "gloomy", "dim"], "answer": "dark"},
        {"question": "The weather that day was ___, matching his melancholic mood.", "options": ["gloomy", "dark", "dim"], "answer": "gloomy"},
        {"question": "The ___ lighting in the restaurant created a cozy and intimate atmosphere.", "options": ["dim", "gloomy", "dark"], "answer": "dim"}
    ]

    # Calculate the score
    score = 0
    for i, question in enumerate(questions):
        user_answer = request.form.get(f'question{i}')
        if user_answer == question['answer']:
            score += 1

    total_questions = len(questions)
    percentage = round((score / total_questions) * 100)

    # Determine the message based on the score
    message = ""
    if score == total_questions:
        message = "PERFECTION!!!"
    elif percentage >= 75:
        message = "THAT WAS REALLY GOOD!!!"
    elif percentage >= 50:
        message = "GOOD JOB!!!"
    elif percentage >= 25:
        message = "NOT BAD!!!"
    elif score > 0:
        message = "NEED MORE PRACTICE!!!"
    else:
        message = ":("

    return render_template('score.html', score=score, total=total_questions, message=message)



if __name__ == '__main__':
    app.run(debug=True)
