import os
from main import redact_text_in_pdf

def test_name_redaction():
    input_pdf = "resources/test1in.pdf"
    output_dir = "redacted"
    names_to_redact = ["Bill", "Carter"]

    os.makedirs(output_dir, exist_ok=True)
    redacted_tokens = redact_text_in_pdf(input_pdf, output_dir, names_to_redact)

    assert any(token == "Bill" for _, _, token, _, _ in redacted_tokens), "Bill not redacted"
    assert any(token == "Carter" for _, _, token, _, _ in redacted_tokens), "Carter not redacted"
