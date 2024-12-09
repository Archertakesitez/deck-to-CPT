import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from .pdf_to_text import read_pdf_with_cname
from .data_loader import load_cpt_data

# Initialize data once when module is loaded
cpt_data = load_cpt_data()
vectorizer = TfidfVectorizer(stop_words="english")


# Corpus: combine description for the CPT in this row and pitch text
def find_relevant_cpt_codes_tfidf(
    file: str, cpt_data: pd.DataFrame = cpt_data, top_n: int = 5
) -> dict:
    try:
        # Get pitch text from PDF
        pitch_text = "".join(read_pdf_with_cname(file=file))

        # Create corpus with all CPT descriptions and pitch text
        descriptions = cpt_data["Description"].tolist()
        corpus = descriptions + [pitch_text]

        # Vectorize all texts at once
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Calculate similarities between pitch text and all descriptions at once
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()

        # Create dictionary of top_n results
        result_dict = {
            code: desc
            for code, desc, score in sorted(
                zip(cpt_data["Code"], descriptions, similarities),
                key=lambda x: x[2],  # Sort by similarity score
                reverse=True,
            )[
                :top_n
            ]  # Get only top_n results
        }

        return result_dict  # Return dictionary instead of JSON string

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
