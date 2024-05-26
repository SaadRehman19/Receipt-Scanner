import spacy

def perform_ner(text):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the input text with the NLP pipeline
    doc = nlp(text)

    # Extract and print named entities
    for ent in doc.ents:
        print(f"Entity: {ent.text} - Type: {ent.label_}")

if __name__ == "__main__":
    sample_text = (
        "Welcare STORE I0 KFC 's Finger PNTN # '' Hix '' eere ihIusivelbi16 % Yourr order number 2215 22108/2021 2215 9 * 40 PM Cashier Trainee2 Trans # : 2215 MICHTY ZINGER BURC Rs . 596 CHEESE 40 200 MIGHTY BURGER COM 785 ZINGER cOMB ? 66C Rs . 660 ZINGER BURGER @ 47 Rs 940 CHICKEN 43 : Rs 435 3 PCS 3,615 Rs_ Eat ALFALAH CREDIT change Thank Town Bahria KFc 0181 Good Lickin 0819531-5 [ ax ] Sales 3,615 3,615"
    )

    perform_ner(sample_text)
