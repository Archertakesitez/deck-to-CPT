import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from .pdf_to_text import read_pdf_with_cname
from .data_loader import load_cpt_data

# Initialize data once when module is loaded
cpt_data = load_cpt_data()
vectorizer = TfidfVectorizer(stop_words="english")

# pitch_text = "Behavioral Health Support for Primary Care Integrated, Virtual Mental Health Care for Family Medicine, Pediatrics and OBGYN OUR  MISSION Increasing Access to Mental Health Services in Underresourced Areas  While about a quarter of adults have a mental illness, 50 %  of the US population lives in a mental health shortage area.  [company name] sets out to help patients in areas where support is otherwise unavailable.  THE PROBLEM 25% 80% 50%  of PCP visits involve mental health Patients overwhelmingly bring their mental health concerns to primary care providers instead of going directly to specialty care. PCPs act as the de facto triage point but have limited support.of patients with mental health concerns seek support from primary care PCPs work in 15-minute appointments and typically have limited resources and training, putting a strain both on them and their patients.Of the US population lives in a mental health shortage area Given massive shortages, there are frequently 6 +  month waitlists for patients who need specialty mental health support.Communities Lack Access to Mental Healthcare Patients look to primary care as their front line of support, however providers are poorly equipped Collaborative Care ([name]) [name]  integrates physical and mental health care in the primary care setting through counseling and consulting psychiatry.  There have been 80 +  academic studies *  showing :  [name] is highly effective (2x vs. usual care) 1. [name] reduces cost of care substantially 2. [name] drives up patient and provider satisfaction 3. *See details here THE CARE MODEL [company name] Has Aligned Incentives With Primary Care Clinics Improve Outcomes  & Patient Satisfaction Studies of the [name] Model have shown that it is more than 2x as effective as usual care in driving mental health symptoms to remission.  Moreover, 75 %  of patients who are treated through [name] models are highly satisfied with their care. Activate A New  FFS Revenue Stream Collaborative care can generate significant new revenue for partner practices through FFS reimbursement. [company name] generates ~$ 10k in contrbution margin per engaged PCP / year. Improve Risk Adjustments & Reduce Cost of Care We can drive an additional increase in revenue through refining mental health diagnoses and improving risk adjustments. Additionally, [name] has been proven to reduce patient cost of care by $ 3,400 over 4 years. VALUE PROPOSITION. Thank you For more info, contact : [email]"


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


# relevant_codes = find_relevant_cpt_codes_tfidf(file=)

# Display the relevant CPT codes
# if __name__ == "__main__":
#     file = "../data/April+Health+Introduction+Deck.pdf"

#     print(find_relevant_cpt_codes_tfidf(file=file))
