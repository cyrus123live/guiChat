import openai
import os

def main():

    openai.api_key = "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"
    model_engine = "text-davinci-002" 

    prompt = ""
    n = 1
    temperature = 1

    convo = ""

    while True:

        prompt = input("Prompt: ")
        if prompt == "q":
            exit()
        elif prompt == "r":
            convo = ""
            continue
        elif prompt == "":
            continue

        convo = convo + "\nPrompt: " + prompt

        response = openai.Completion.create(engine=model_engine,
            prompt=convo,
            max_tokens=1000,
            n = int(n),
            temperature = float(temperature)
            ).choices[0].text.strip()

        print(response)

        convo = convo + "\n" + response

if __name__ == "__main__":
    main()
