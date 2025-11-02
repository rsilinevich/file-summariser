from google import genai
from dotenv import load_dotenv
import os
import docx
import pdfplumber
from pathlib import Path

# Load .env file
load_dotenv()

# Retrieve and validate API key
def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env file")
    return api_key


# Read the file based on file type
def read_file(file_path):
    path = Path(file_path)

    # Check file exists
    if not path.exists():
        raise FileNotFoundError(f"file not found: {file_path}")

    # Check file size (max 10MB)
    if path.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("File too large (max 10MB)")
    
    text = ""

    try:           
        if file_path.endswith(".txt"):
            print("Extracting text...")
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        elif file_path.endswith(".pdf"):
            print("Extracting text...")
            with pdfplumber.open(file_path) as f:
                text = "\n".join(page.extract_text() for page in f.pages if page.extract_text())

        elif file_path.endswith(".docx"):
            print("Extracting text...")
            f = docx.Document(file_path)
            text = "\n".join([para.text for para in f.paragraphs if para.text.strip()])

        else:
            raise ValueError("Unsupported file type. Use .txt, .pdf, or .docx!")

    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")
    
    return text

# Summarise using Gemini API
def summarise_text(client, text, instructions):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=f"{instructions}:\n\n{text}"
    )
    return response.text

def main():
    try:
        api_key = get_api_key()
        client = genai.Client(api_key=api_key)

        file_path = input("Enter the path to your file(.txt, .pdf or .docx): ").strip()

        # Custom instructions option
        use_custom = input("Use custom instructions? (y/n, default=n): ").strip().lower()
        if use_custom == 'y':
            instructions = input("Enter your instructions (e.g., 'Summarise in 3 bullet points'): ").strip()
        else:
            instructions = "Summarise this file in a few sentences"

        text = read_file(file_path)

        # Validate content
        if not text.strip():
            print("File appears to be empty.")
            return

        print(f"Extracted {len(text)} characters, generating summary...")
        summary = summarise_text(client, text, instructions)

        print("\n" + "="*60)
        print(summary)
        print("="*60)

        # Save option
        save = input("\nSave to file? (y/n, default=y): ").strip().lower()
        if save != 'n':
            output_file = input("Output filename (default=summary.txt): ").strip() or "summary.txt"
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(f"Summary of: {file_path}\n\n")
                out.write(summary)
            print(f"✓ Summary saved to: {output_file}")
        
        print("\nDone!")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()