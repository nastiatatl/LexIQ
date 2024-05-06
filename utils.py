from typing import List

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


