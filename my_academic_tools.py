import subprocess
import os
import fitz  # from PyMuPDF
from fastapi import FastAPI
import uvicorn

# --- CORRECTED IMPORTS (Confirmed) ---
from google.adk import agents
from google.adk.agents import BaseAgent
from google.adk.tools import FunctionTool
# -----------------------------------

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


# --- CORRECTED TOOL DEFINITION (v5) ---
# The FunctionTool constructor only takes the function itself.
# It automatically uses the function's name and docstring.
pdf_tool = FunctionTool(func=extract_pdf_text)
latex_tool = FunctionTool(func=compile_latex_to_pdf)
# ------------------------------------

# Define a BaseAgent that includes the tools
class AcademicAgent(BaseAgent):
    def __init__(self):
        super().__init__(tools=[pdf_tool, latex_tool])

# Define the FastAPI app
app = FastAPI()

# Mount the AcademicAgent to the app
agents.mount_agent_to_app(AcademicAgent, app, path="/mcp")

# Main block to run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
