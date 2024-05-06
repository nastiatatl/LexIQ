from openai import OpenAI
import os
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


if __name__ == "__main__":
    print(gpt3_5(prompt_from_vocab("describe help decide maintain polish".split(" "))))
