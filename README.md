# File Summarizer with Gemini AI

A simple Python command-line tool that summarizes text files, PDFs, and Word documents using Google's Gemini AI.

## Features

- 📄 Supports multiple file formats: `.txt`, `.pdf`, `.docx`
- 🤖 Powered by Google Gemini AI (gemini-2.5-flash)
- ⚙️ Custom summarization instructions
- 💾 Save summaries to file or view in terminal
- 🛡️ Error handling for missing files, empty content, and API issues

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
```

4. Open `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the script:
```bash
python file-summariser.py
```

Follow the prompts:
1. Enter the path to your file
2. Choose whether to use custom instructions (optional)
3. View the summary
4. Choose whether to save to a file

### Example

```
Enter the path to your file (.txt, .pdf or .docx): document.pdf
Use custom instructions? (y/n, default=n): n
Extracting PDF text...
Extracted 1234 characters, generating summary...

============================================================
This document outlines the key principles of sustainable 
development, focusing on environmental protection, economic 
growth, and social equity...
============================================================

Save to file? (y/n, default=y): y
Output filename (default=summary.txt): 
Summary saved to: summary.txt

Done!
```

## Custom Instructions

You can customize how the AI summarizes your document:

```
Use custom instructions? (y/n, default=n): y
Enter your instructions: Summarize in 3 bullet points focusing on main arguments
```

## Project Structure

```
.
├── file-summariser.py              # Main application script
├── requirements.txt     # Python dependencies
├── .env                # Your API key
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Dependencies

- `google-genai` - Google Gemini AI SDK
- `python-dotenv` - Environment variable management
- `python-docx` - Word document processing
- `pdfplumber` - PDF text extraction

## Error Handling

The tool handles common errors gracefully:
- ❌ Missing or invalid API key
- ❌ File not found
- ❌ Unsupported file type
- ❌ Empty files
- ❌ File reading errors
