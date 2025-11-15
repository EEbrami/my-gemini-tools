# my-gemini-tools

A collection of tools for Gemini CLI.

## How It Works

When you add a new tool file to this repository, a GitHub Actions workflow automatically:
1. Detects the new file
2. Extracts a description from the file's comments/docstrings
3. Updates this README with the file and its description

### Supported Description Formats

The workflow can extract descriptions from:
- **Python**: Docstrings (`"""description"""`)
- **JavaScript**: Comments (`// description` or `/* description */`)
- **Shell scripts**: Comments (`# description`)
- **Other files**: Default descriptions based on file extension

### Usage

Simply commit your Gemini CLI tool file to this repository. The workflow will run on push to main/master and update the README automatically.
## Files

- `my_academic_tools.py`: Extracts all text from a given PDF file.
- `render.yaml`: YAML configuration file
- `requirements.txt`: Text file
