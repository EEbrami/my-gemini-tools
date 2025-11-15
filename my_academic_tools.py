import subprocess
import os
import fitz  # from PyMuPDF
from fastapi import FastAPI
import uvicorn
from google.adk import BaseAgent, agents
from google.adk.tools import Tool  # <--- FIX 1: Correct import

# Tool function to extract text from a PDF file
def extract_pdf_text(file_path: str) -> str:
    """
    Extracts all text from a given PDF file.

    Args:
        file_path: The absolute or relative path to the PDF file.

    Returns:
        A single string containing all the extracted text from the PDF.
        Returns an error message if the file cannot be processed.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

# Tool function to compile a LaTeX file to a PDF
def compile_latex_to_pdf(file_path: str) -> str:
    """
    Compiles a .tex file into a PDF using the pdflatex engine.

    Args:
        file_path: The absolute or relative path to the LaTeX .tex file.

    Returns:
        A string indicating "Success" if the compilation is successful,
        or "Error" followed by the compiler output if it fails.
    """
    try:
        directory, filename = os.path.split(file_path)
        if not directory:
            directory = "."
            
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'-output-directory={directory}', file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return "Success"
        else:
            return f"Error: {result.stdout}\n{result.stderr}"
    except FileNotFoundError:
        return "Error: 'pdflatex' command not found. Is LaTeX installed and in your PATH?"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- CORRECTED CODE ---

# Wrap the functions into Tool objects
pdf_tool = Tool(  # <--- FIX 2: Removed 'google.adk.'
    name="extract_pdf_text",
    description="Extracts all text from a given PDF file.",
    fn=extract_pdf_text,  # <--- FIX 3: Changed 'func' to 'fn'
)

latex_tool = Tool(  # <--- FIX 2: Removed 'google.adk.'
    name="compile_latex_to_pdf",
    description="Compiles a .tex file into a PDF using the pdflatex engine.",
    fn=compile_latex_to_pdf, # <--- FIX 3: Changed 'func' to 'fn'
)

# Define a BaseAgent that includes the tools
class AcademicAgent(BaseAgent):  # <--- FIX 2: Removed 'google.adk.'
    def __init__(self):
        super().__init__(tools=[pdf_tool, latex_tool])

# Define the FastAPI app
app = FastAPI()

# Mount the AcademicAgent to the app
agents.mount_agent_to_app(AcademicAgent, app, path="/mcp") # <--- FIX 2: Removed 'google.adk.'

# Main block to run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
