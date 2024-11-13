from pypdf import PdfReader
import re
import spacy

# Load the spaCy model for English
nlp = spacy.load("en_core_web_sm")


def replace_contact_info(text: str) -> str:
    # Regex pattern for email addresses
    email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    # Regex pattern for phone numbers (various formats, e.g., (123) 456-7890, 123-456-7890, +1 123 456 7890)
    phone_pattern = re.compile(
        r"(\+?\d{1,3})?[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}"
    )

    # Replace email addresses with [email]
    text = email_pattern.sub("[email]", text)

    # Replace phone numbers with [phone number]
    text = phone_pattern.sub("[phone number]", text)

    return text


def replace_names_with_placeholders(text: str) -> str:
    # Process the text using spaCy
    doc = nlp(text)

    # Create a list to store the modified text
    new_text = text

    # Iterate through the named entities detected by spaCy
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Replace each detected person name with the placeholder [name]
            new_text = new_text.replace(ent.text, "[name]")

    return new_text


def replace_company_names(text: str, company_names: str) -> str:

    embedded_pattern = re.compile(
        re.escape(company_names.replace(" ", "")), re.IGNORECASE
    )
    embedded_pattern2 = re.compile(
        re.escape(company_names), re.IGNORECASE)
    
    embedded_pattern3 = re.compile(
    re.escape(company_names.replace(" ", r"[\w\W]")), re.IGNORECASE
)

    text = embedded_pattern.sub("[company name]", text)
    text = embedded_pattern2.sub("[company name]", text)
    text = embedded_pattern3.sub("[company name]", text)
    return text



def read_pdf(file: str, company: str) -> list:
    reader = PdfReader(file)
    res = []
    number_of_pages = len(reader.pages)
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        text = text.replace("\n", " ")
        text = replace_contact_info(text)
        text = replace_company_names(text, company)
        text = replace_names_with_placeholders(text)
        if "leadership" in text.lower() or "team" in text.lower() or "founder" in text.lower():
            # print(f"page{i} skipped")
            continue
        res.append(text)
    return res


# if __name__ == "__main__":
#     print(read_pdf("Hera Fertility.pdf", "hera fertility"))
