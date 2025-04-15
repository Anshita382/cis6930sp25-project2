import argparse
import glob
import os
import fitz  # PyMuPDF
import spacy
import requests

nlp = spacy.load("en_core_web_sm")

def get_coref_mapping(text):
    try:
        response = requests.post(
            "http://gpu002.cm.cluster:65535/resolve_coref",
            headers={"Content-Type": "application/json"},
            json={"text": text}
        )
        return response.json().get("coreference_mapping", [])
    except Exception as e:
        print(f"Coref API error: {e}")
        return []

def redact_text_in_pdf(input_file, output_dir, names, redact_entities, redact_coref):
    doc = fitz.open(input_file)
    redacted_tokens = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        tokens_to_redact = []

        # Redact exact names
        if names:
            tokens_to_redact.extend([(name, "Name") for name in names])

        # Redact named entities
        if redact_entities:
            doc_nlp = nlp(text)
            for ent in doc_nlp.ents:
                if ent.label_ in {"PERSON", "ORG", "GPE"}:
                    tokens_to_redact.append((ent.text, ent.label_))

        # Redact coreference
        if redact_coref:
            corefs = get_coref_mapping(text)
            for group in corefs:
                for _, token in group.items():
                    tokens_to_redact.append((token, "Coref"))

        # Apply redactions
        for token, token_type in tokens_to_redact:
            matches = page.search_for(token)
            for match in matches:
                page.add_redact_annot(match, text="[REDACTED]", fill=(0, 0, 0))
                redacted_tokens.append((input_file, f"{page_num}", token, len(token), token_type))

        page.apply_redactions()

    output_path = os.path.join(output_dir, os.path.basename(input_file))
    doc.save(output_path)
    doc.close()

    return redacted_tokens

def write_stats(stats_file, redacted_tokens):
    with open(stats_file, "a", encoding="utf-8") as f:
        for file, location, token, length, token_type in redacted_tokens:
            f.write(f"{file}\t{location}\t{token}\t{length}\t{token_type}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--names", nargs="+")
    parser.add_argument("--entities", action="store_true")
    parser.add_argument("--coref", action="store_true")
    parser.add_argument("--stats")

    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)

    input_files = []
    for pattern in args.input:
        input_files.extend(glob.glob(pattern))

    all_redacted = []
    for file in input_files:
        redacted = redact_text_in_pdf(
            file,
            args.output,
            names=args.names or [],
            redact_entities=args.entities,
            redact_coref=args.coref
        )
        all_redacted.extend(redacted)

    if args.stats:
        write_stats(args.stats, all_redacted)

if __name__ == "__main__":
    main()
