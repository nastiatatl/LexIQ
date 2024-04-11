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

if __name__ == '__main__':
    app.run(debug=True)
