import openai  # Replace with the GPT API you're using
import json
from .pdf_to_text import read_pdf

# Replace 'your_api_key' with your actual GPT API key
openai.api_key = "replace your api key here"


def predict_cpt_codes(messages):
    """
    This function takes input text from a product deck, sends it to the GPT API,
    and returns a dictionary of CPT codes and their descriptions.
    """

    try:
        # API call to the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-4o", messages=messages  # Use "gpt-4o" as LLM
        )

        # Extract the response content
        cpt_data = response["choices"][0]["message"]["content"].strip()

        # Attempt to parse the output into a dictionary format
        cpt_dict = json.loads(cpt_data)  # Use json.loads for safer parsing
        return cpt_dict

    except json.JSONDecodeError:
        print("Failed to parse JSON response. Here is the raw output:", cpt_data)
        return {}
    except Exception as e:
        print("An error occurred:", e)
        return {}


def pdf_to_cpt(file: str, company: str) -> str:
    extracted_texts = read_pdf(file=file, company=company)
    messages = [
        {
            "role": "system",
            "content": "You are an assistant skilled in extracting relevant healthcare CPT codes.",
        },
        {
            "role": "user",
            "content": (
                "Analyze the following text extracted from a healthcare startup’s pitch deck to identify the most relevant CPT codes based on the services described. Match CPT codes that reflect the types of services, care models, or healthcare management approaches detailed in the text. "
                "Rank the top 5 matched CPT codes by relevance to the startup's offerings and output the result in the following JSON format: "
                """{
    "code": "Description of this CPT Code",
    "code": "Description of this CPT Code",
    "code": "Description of this CPT Code",
    "code": "Description of this CPT Code",
    "code": "Description of this CPT Code"
}"""
                "please just output the json, no triple backticks!"
                "in json you should only include the CPT code's number, please do not include the characters 'CPT code'..."
                f"Text: {extracted_texts}\n\n"
                "If available and relevant, prioritize codes that are central to the services highlighted in the text."
            ),
        },
    ]
    cpt_codes = predict_cpt_codes(messages)
    return cpt_codes


# if __name__ == "__main__":
#     print(
#         pdf_to_cpt(
#             file="../data/April+Health+Introduction+Deck.pdf", company="april health"
#         )
#     )
