#  File input
#  API key (Gemini)
#  Instructions
#  Terminal-based
#  Summary output (new file or terminal)
#  Libraries?
#  Push to GitHub
#  Support for multiple file types – e.g. .txt, .pdf, .docx.
#  Error handling – e.g. invalid API key, empty file, or bad file path.
#  Requirements file (requirements.txt) – list libraries like requests, openai, pdfplumber, etc.

from google import genai
from dotenv import load_dotenv
import os
import docx
import pdfplumber

# Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

client = genai.Client(api_key=api_key)

file_path = input("Enter the path to your text file: ")

# Read the file based on file type
text = ""
if file_path.endswith(".txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

elif file_path.endswith(".pdf"):
    with pdfplumber.open(file_path) as f:
        text = "\n".join(page.extract_text() for page in f.pages if page.extract_text())

elif file_path.endswith(".docx"):
    f = docx.Document(file_path)
    text = "\n".join([para.text for para in f.paragraphs])

else:
    print("Please choose a .txt or .pdf or .docx file!")
    exit()

# Summarise using Gemini
if not text.strip():
    print("File appears to be empty.")
    exit()

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=f"Summarise this file in a few sentences:\n\n{text}"
)

# Print and save result
summary = response.text
print("\nSummary:\n", summary)

with open("summary.txt", "w", encoding="utf-8") as out:
    out.write(summary)
print("\nSummary saved to file: summary.txt")