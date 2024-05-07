from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# prompt gpt3.5
def gpt3_5(prompt):
    message = {
        'role': 'user',
        'content': prompt
    }

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[message],
        temperature=0.1,
    )
    return response.choices[0].message.content

def gpt4(prompt):
    message = {
        'role': 'user',
        'content': prompt
    }

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[message],
        temperature=0.1,
    )
    return response.choices[0].message.content


def prompt_from_vocab(vocab):
    return (f"Given the following words, write a sentence using each word in a sentence"
            f" that highlights the meaning of the word.\nPut each sentence on a new line."
            f"Do not change the morphology of the word in the sentence."
            f"\n\n{' '.join(vocab)}\n\n---\n\n")


def distinct_prompt_from_vocab(vocab):
    return (f"Given the following words, write a sentence using each word in a sentence"
            f" that highlights the meaning of the word.\nPut each sentence on a new line."
            f"\n\n{' '.join(vocab)}\n\n---\n\nMake sure no word could be used in any other sentence!")


def synonym_prompt(vocab, n=3):
    return (f"Given the following words, provide {n} half-synonyms for each word separated by a space.\n"
            f"Do not repeat the word. Do not use punctuation. Place each set of synonyms on a new line\n\n{' '.join(vocab)}\n\n---\n\n")

# best prompt!!
def unified_prompt(vocab, n=3):
    sent = "His belief that cats can speak human languages is a deviation from normal thinking"
    return (f"You are an SAT vocab question writer. You have a list of words that is the correct answers for a list of questions.\n"
            f"For each word, create a sentence that highlights the meaning of the word. Also, provide {n} words that DO NOT fit in the blank that will be the wrong answer choices\n"
            f"For example, if the word is 'deviation', you could provide the sentence '{sent}.' and the answer choices 'error', 'pause', 'module'.\n"
            f"This is becasue 'deviation' is the correct answer and 'error', 'pause', and 'module' are the wrong answers  because 'error', 'pause' and 'module' do not fit in the sentence where 'deviation' is.\n"
            f"Place each sentence and multiple choice answers on a new line. Separate each question and answer set with two new lines. Such as:\n{sent}\nerror\npause\nmodule\n\n"
            f" Here are the words: {' '.join(vocab)}")


if __name__ == "__main__":
    print(gpt3_5(unified_prompt("special manifest destroy".split(" "))))
    print(gpt4(unified_prompt("special manifest destroy".split(" "))))
