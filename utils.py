from wordhoard import Synonyms
from typing import List
from typeguard import typechecked
import random


@typechecked
def generate_synonyms(word: str) -> str:
    # FIXME: synonyms are in alphabetical order, for now sample randomly
    # in the future, might select the ones with the highest similarity scores
    # might take too long though
    # NOTE: need to take care of part-of-speech mismatch, potential test case
    all_synonyms = Synonyms(search_string=word).find_synonyms()
    random_synonym = all_synonyms[random.randint(0, len(all_synonyms) - 1)]
    return random_synonym

def process_input(input_str: str) -> List[str]:
    # NOTE: potential unit test: various inputs
    cleaned_input = input_str.replace(',', ' ').replace('\n', ' ')
    words = cleaned_input.split()
    return words

def create_score_message(score: int, total_questions: int) -> str:
    # Determine the message based on the score
    percentage = round((score / total_questions) * 100)
    message = "PERFECTION!!!" if score == total_questions else \
              "THAT WAS REALLY GOOD!!!" if percentage >= 75 else \
              "GOOD JOB!!!" if percentage >= 50 else \
              "NOT BAD!!!" if percentage >= 25 else \
              "NEED MORE PRACTICE!!!" if score > 0 else ":("
    return message

if __name__ == '__main__':
    from nltk.corpus import wordnet as wn
    print(wn.synonyms('strong'))


