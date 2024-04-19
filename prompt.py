from openai import OpenAI

client = OpenAI(api_key="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")


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
            f"\n\n{' '.join(vocab)}\n\n---\n\n")


def distinct_prompt_from_vocab(vocab):
    return (f"Given the following words, write a sentence using each word in a sentence"
            f" that highlights the meaning of the word.\nPut each sentence on a new line."
            f"\n\n{' '.join(vocab)}\n\n---\n\nMake sure no word could be used in any other sentence!")


if __name__ == "__main__":
    print(gpt3_5(prompt_from_vocab("describe help decide maintain polish".split(" "))))
