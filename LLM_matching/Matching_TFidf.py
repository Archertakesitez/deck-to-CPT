#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# In[2]:


# Load CPT Codes from Excel File
cpt_file = "cpt_codes.xlsx"
cpt_data = pd.read_excel(cpt_file)

# Extract codes and descriptions
cpt_descriptions = cpt_data["Description"].tolist()


# In[3]:


pitch_text = "Behavioral Health Support for Primary Care Integrated, Virtual Mental Health Care for Family Medicine, Pediatrics and OBGYN OUR  MISSION Increasing Access to Mental Health Services in Underresourced Areas  While about a quarter of adults have a mental illness, 50 %  of the US population lives in a mental health shortage area.  [company name] sets out to help patients in areas where support is otherwise unavailable.  THE PROBLEM 25% 80% 50%  of PCP visits involve mental health Patients overwhelmingly bring their mental health concerns to primary care providers instead of going directly to specialty care. PCPs act as the de facto triage point but have limited support.of patients with mental health concerns seek support from primary care PCPs work in 15-minute appointments and typically have limited resources and training, putting a strain both on them and their patients.Of the US population lives in a mental health shortage area Given massive shortages, there are frequently 6 +  month waitlists for patients who need specialty mental health support.Communities Lack Access to Mental Healthcare Patients look to primary care as their front line of support, however providers are poorly equipped Collaborative Care ([name]) [name]  integrates physical and mental health care in the primary care setting through counseling and consulting psychiatry.  There have been 80 +  academic studies *  showing :  [name] is highly effective (2x vs. usual care) 1. [name] reduces cost of care substantially 2. [name] drives up patient and provider satisfaction 3. *See details here THE CARE MODEL [company name] Has Aligned Incentives With Primary Care Clinics Improve Outcomes  & Patient Satisfaction Studies of the [name] Model have shown that it is more than 2x as effective as usual care in driving mental health symptoms to remission.  Moreover, 75 %  of patients who are treated through [name] models are highly satisfied with their care. Activate A New  FFS Revenue Stream Collaborative care can generate significant new revenue for partner practices through FFS reimbursement. [company name] generates ~$ 10k in contrbution margin per engaged PCP / year. Improve Risk Adjustments & Reduce Cost of Care We can drive an additional increase in revenue through refining mental health diagnoses and improving risk adjustments. Additionally, [name] has been proven to reduce patient cost of care by $ 3,400 over 4 years. VALUE PROPOSITION. Thank you For more info, contact : [email]"


# In[13]:


# Corpus: combine description for the CPT in this row and pitch text
def find_relevant_cpt_codes_tfidf(pitch_text, cpt_data, top_n=5):
    # Create a list to store similarity scores
    relevant_codes = []
    
    # Corpus: combine description for the CPT in this row and pitch text
    # Iterate through each CPT description to compare with the extracted text
    for index, row in cpt_data.iterrows():
        corpus = [row['Description'], pitch_text]
        
        # Convert the corpus into a TF-IDF matrix
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Calculate cosine similarity between the extracted text and the CPT description
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2]).flatten()[0]
        
        # Append the code, description, and similarity score
        relevant_codes.append({
            'Code': row['Code'],
            'Description': row['Description'],
            'Score': cosine_sim
        })
    
    # Sort the relevant codes by similarity score in descending order and return the top matches
    relevant_codes = sorted(relevant_codes, key=lambda x: x['Score'], reverse=True)[:top_n]
    return relevant_codes

relevant_codes = find_relevant_cpt_codes_tfidf(pitch_text, cpt_data)

# Display the relevant CPT codes
for code in relevant_codes:
    print(f"Code: {code['Code']}, Description: {code['Description']}, Score: {code['Score']}")

