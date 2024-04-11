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



