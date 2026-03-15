import pdfplumber
import re


def extract_compliance_rules(pdf_path):

    rules = []
    seen = set()

    obligation_words = [
        "must",
        "shall",
        "shall be",
        "must be",
        "required to",
        "is required to"
    ]

    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + " "

    sentences = re.split(r'[.!?]', full_text)

    for sentence in sentences:

        clean = re.sub(r"\(cid:\d+\)", "", sentence).strip()

        if len(clean) < 50:
            continue

        if len(clean) > 180:
            continue

        lower = clean.lower()

        if any(word in lower for word in obligation_words):

            # remove section references
            if any(x in lower for x in ["section", "clause", "schedule", "chapter"]):
                continue

            # remove duplicates
            key = lower[:120]

            if key not in seen:
                rules.append(clean)
                seen.add(key)

    return rules