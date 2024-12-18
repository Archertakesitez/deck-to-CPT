# Convert Deck To CPT Codes
> [**Paper**](https://archertakesitez.github.io/static/assets/papers/Deck_To_CPT_Report.pdf)
>
> Rosy Xu, Tongyu Zhao, Albert Kong, Erchi Zhang
> 
> Sponsored by Maccabee Ventures
<p align = "center">
      <img src="https://github.com/Archertakesitez/deck-to-CPT/blob/main/readme_resource/after_parsing.png" alt="Convert Deck To CPT Codes" width="700"/>
</p>
Capstone Project for NYU's graduate course: DS-GA 1006

[Project Poster](https://archertakesitez.github.io/static/assets/papers/21-Franklin.pdf)

## Hightlights ⭐️
- two approaches to analyze your PDF document
- data privacy ensured
- a dataset containing CPT codes and their correspondinng descriptions provided for you

## Abstract
This project is a web application that helps match healthcare-related PDF documents (such as pitch decks or medical documentation) with appropriate CPT (Current Procedural Terminology) codes. Users can upload PDF documents through a web interface and choose between two analysis methods: a keyword-based matching system using TF-IDF, or an AI-powered analysis using GPT-4. The application processes the uploaded documents, and returns the top 5 most relevant CPT codes with their descriptions. This tool is particularly useful for healthcare startups and medical professionals who need to quickly identify appropriate medical billing codes based on service descriptions.

## Implementation
<p align = "center">
      <img src="https://github.com/Archertakesitez/deck-to-CPT/blob/main/readme_resource/workflow_1.png" alt="workflow" width="600"/>
</p>

On our website, you can find two tabs on the left — "Keyword Matching" and "AI Analysis". 

When the user uploads a PDF file through the "Keyword Matching" option, our function processes it using TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to analyze the document's content, and matches it against a database of CPT code descriptions. The function calculates similarity scores between the PDF content and CPT descriptions, and shows the top 5 most relevant matches.

When a user uploads a PDF file and provides a company name through the "AI Analysis" option, our function processes the PDF by first removing sensitive information (like emails, phone numbers, and company names), then sends the sanitized text to GPT-4 through the OpenAI API. The AI model analyzes the content and returns the top 5 most relevant CPT codes based on the healthcare services or procedures described in the document. Please note that if you want to use the AI Analysis option, **you need to populate this line:**
```
openai.api_key = "replace your api key here"
```
in [LLM_matching/text_to_CPY.py](https://github.com/Archertakesitez/deck-to-CPT/blob/main/LLM_matching/text_to_CPT.py) with your own OPENAI API key.

## Getting Started 🚀
### Installation
**1.** Set up Conda environment:
```
conda create --name deck_to_CPT_env python=3.9
conda activate deck_to_CPT_env
```

**2.** Clone the repo and install packages:
```
git clone git@github.com:Archertakesitez/deck-to-CPT.git
cd deck-to-CPT
pip install -r requirements.txt
```
Then you are ready to go!

### Run the website
```
cd web_app
python main.py
```
Now you can visit our website running on http://127.0.0.1:8000/

## Authors
- **[Rosy Xu](https://github.com/yinyin0916)**
- **[Tracy Zhao](https://github.com/Tongyu-Zhao)**
- **[Albert Kong](https://github.com/AlbertKong0827)**
- **[Erchi Zhang](https://github.com/Archertakesitez)**

