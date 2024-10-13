from pypdf import PdfReader
import scispacy
import spacy

# from pdf_reader import read_pdf

nlp = spacy.load("en_core_sci_lg")


def scratch_read_pdf(file: str) -> str:
    reader = PdfReader(file)
    res = []
    number_of_pages = len(reader.pages)
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        # text = text.replace("\n", " ")
        res.append(text)
    output_text = " ".join(res)
    return output_text


def extract_medical_text(input_text: str):
    # text = "The patient was diagnosed with diabetes and was prescribed metformin."
    # medical_entities = ["DISEASE", "CHEMICAL"]  # You can expand this list as needed
    doc = nlp(input_text)

    for ent in doc.ents:
        # if ent.label_ in medical_entities:
        print(f"Entity: {ent.text}")


if __name__ == "__main__":
    text = scratch_read_pdf("april_health.pdf")
    extract_medical_text(text)
