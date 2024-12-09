# Convert Deck To CPT Codes
> Rosy Xu, Tracy Zhao, Albert Kong, Erchi Zhang
<p align = "center">
      <img src="https://github.com/Archertakesitez/deck-to-CPT/blob/main/readme_resource/first_page.png" alt="Convert Deck To CPT Codes" width="700"/>
</p>
Capstone Project for NYU's graduate course: DS-GA 1006

## Abstract 🎄
This project is a web application that helps match healthcare-related PDF documents (such as pitch decks or medical documentation) with appropriate CPT (Current Procedural Terminology) codes. Users can upload PDF documents through a web interface and choose between two analysis methods: a keyword-based matching system using TF-IDF, or an AI-powered analysis using GPT-4. The application processes the uploaded documents, removes sensitive information (like emails, phone numbers, and personal names), and returns the top 5 most relevant CPT codes with their descriptions. This tool is particularly useful for healthcare startups and medical professionals who need to quickly identify appropriate medical billing codes based on service descriptions.

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
Then you can visit our website running on http://127.0.0.1:8000/


