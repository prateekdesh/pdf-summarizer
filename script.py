#!/Users/prateek/projects/scripts/summarizer/venv/bin/python

from pypdf import PdfReader
from google import genai
import sys
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("token"))

destination = "/Users/prateek/notes"

default = "gemini-2.5-flash-preview-04-17"
pro = "gemini-2.5-pro-exp-03-25"

def read(file, model):
    reader = PdfReader(file)
    content = ""
    print("Reading pdf...")
    for page in reader.pages:
        content+=page.extract_text()

    generate_notes(content, model)


def generate_notes(content, model):
    print(f"Generating using {model}..")
    output = client.models.generate_content(
    model=model, contents=f"This is the content from a source PDF, generate descriptive and explanatory notes in beautiful markdown. If you encounter a page with only title but no other content, assume there is an image in that page and elaborate from your knowledge base on that title. Content: {content}"
    )
    response = output.text
    if response.startswith("```markdown\n"):
        response = response[len("```markdown\n"):]
    if response.endswith("\n```"):
        response = response[:-len("\n```")]
    elif response.endswith("```"):
        response = response[:-len("```")]
    save(response)

def save(content):
    notes = f"{destination}/note.md"
    with open(notes, "w") as file:
        file.write(content)
    final(notes)

def final(file):
    print("Completed. Opening..")
    subprocess.run(['open', file], check=True)

if __name__ == "__main__":
    pdf_file_path = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2] == "-p":
            model = pro
        else:
            model = default
    else:
        model = default
    read(pdf_file_path, model)