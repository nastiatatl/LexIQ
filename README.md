# LexIQ

## Introduction

LexIQ is an interactive web application designed for language learners and educators. Its main functionality is quiz generation based on user input: the questions specifically target words with similar meanings but distinct usages. We hope that our app aids its users in building and mastering vocabulary.

## Overview

Upon running the app, the user is prompted with either uploading a csv file with the desired vocabulary or entering the words manually. Once the vocabulary is submitted, the user is able to review the suggested synonyms and choose to go back to the Main page or take a quiz with the entered words. If the user selects the latter option, they will be presented with a multiple-choice quiz. After submitting the answers, the user will see their score, correct answers, and a brief comment. The user can then choose to redo the quiz or come back to the Main page and enter new words.

## Requirements

The code assumes Python version 3.8 or higher.

The `requirements.txt` file contains all modules needed to run this code. To install them, run `pip install -r requirements.txt` in your terminal.

Since our project utilizes the OpenAI API, please make sure to include your API key in the provided .env file:

```bash
OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

Please contact any of us if you run into any issue with the API key. 

## Running the app

Execute the following command to run the Flask server:

```bash
$ python app.py
```

To access the website, point your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Testing module

To run the unit tests for various components of our project, execute the following command:

```bash
$ python test.py
```

