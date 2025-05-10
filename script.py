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



def read(file):
    reader = PdfReader(file)
    content = ""

    for page in reader.pages:
        content+=page.extract_text()

    generate_notes(content)


def generate_notes(content):
    output = client.models.generate_content(
    model="gemini-2.0-flash", contents=f"This is the content from a source PDF, generate descriptive and explanatory notes in beautiful markdown. Every page in the PDF is separated by \"--\". Content: {content}"
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
    subprocess.run(['open', file], check=True)

if __name__ == "__main__":
    pdf_file_path = sys.argv[1]
    read(pdf_file_path)