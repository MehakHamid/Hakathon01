from pypdf import PdfReader
from pathlib import Path

pdf = Path("../textbook/book.pdf")  # change name if needed
output = Path("textbook.txt")

reader = PdfReader(str(pdf))
text = ""

for page in reader.pages:
    text += page.extract_text() + "\n\n"

output.write_text(text, encoding="utf-8")
print("DONE → textbook.txt created.")
