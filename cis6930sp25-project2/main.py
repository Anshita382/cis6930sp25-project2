import argparse
import glob
import os
import fitz  # PyMuPDF

def redact_text_in_pdf(input_file, output_dir, names):
    # Open PDF
    doc = fitz.open(input_file)
    redacted_tokens = []

    for page_num, page in enumerate(doc):
        for name in names:
            matches = page.search_for(name)
            for match in matches:
                page.add_redact_annot(match, text="[REDACTED]", fill=(0, 0, 0))
                redacted_tokens.append((input_file, f"{page_num}", name, len(name), "Name"))

        page.apply_redactions()

    # Save redacted file
    filename = os.path.basename(input_file)
    output_path = os.path.join(output_dir, filename)
    doc.save(output_path)
    doc.close()

    return redacted_tokens


def write_stats(stats_file, redacted_tokens):
    with open(stats_file, "a", encoding="utf-8") as f:
        for file, location, token, length, token_type in redacted_tokens:
            f.write(f"{file}\t{location}\t{token}\t{length}\t{token_type}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+", help="Input file patterns (PDFs)", required=True)
    parser.add_argument("--output", help="Output directory", required=True)
    parser.add_argument("--names", nargs="+", help="Case-sensitive names to redact")
    parser.add_argument("--entities", action="store_true", help="Redact all named entities")
    parser.add_argument("--coref", action="store_true", help="Redact all coreferences")
    parser.add_argument("--stats", help="Output path for redaction stats")

    args = parser.parse_args()

    # Collect input PDFs
    input_files = []
    for pattern in args.input:
        input_files.extend(glob.glob(pattern))

    os.makedirs(args.output, exist_ok=True)
    all_redacted = []

    for file in input_files:
        redacted = redact_text_in_pdf(file, args.output, args.names or [])
        all_redacted.extend(redacted)

    if args.stats:
        write_stats(args.stats, all_redacted)


if __name__ == "__main__":
    main()
