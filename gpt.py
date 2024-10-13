import openai
from pdf_reader import read_pdf
from openai import OpenAI
import os
# Set up your API key
openai.api_key = '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'

client = OpenAI(
    api_key = openai.api_key
)
    
models = client.models.list()

print(models)

def summarize_text(text):
    # Call the OpenAI GPT-4 API for text summarization
    response = openai.completions.create(
        model="gpt-4o-mini",
        prompt="Summarize this text",
        max_tokens=200
    )

    # Extract the summary from the response
    summary = response['choices'][0]['message']['content']
    return summary

# Example usage
if __name__ == "__main__":
    text_lst = read_pdf('april_health.pdf','april health')
    text = ' '.join(text_lst)
    long_text = text
    
    summary = summarize_text(long_text)
    print("Summary:")
    print(summary)
