Here's a `README.md` file for your script:

```markdown
# PDF Summarizer Script

This script summarizes the content of each page in a given PDF document using the Llama 3.1 language model. It leverages the `crew` framework for managing agents and tasks. The summarized content is saved to a text file, with a separator line between the summaries for each page.

## Features

- Summarizes each page of a PDF document.
- Uses the Llama 3.1 language model for generating summaries.
- Tracks and prints the elapsed time for the summarization process.
- Saves the summarized content to a text file with separators between page summaries.

## Requirements

- Python 3.x
- `crewai`
- `langchain_community`
- `PyPDF2`
- `time` (standard Python library)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pdf-summarizer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pdf-summarizer
   ```
3. Install the required Python packages:
   ```bash
   pip install crewai langchain_community PyPDF2
   ```

## Usage

1. Place the PDF document you want to summarize in the project directory.
2. Update the script to point to your PDF file:
   ```python
   pdf_summary = summarize_pdf("your_pdf_file.pdf", ollama_llm)
   ```
3. Run the script:
   ```bash
   python summarize_pdf.py
   ```
4. The script will generate summaries for each page and save them to a text file named `pdf_summaries.txt`.

## Script Breakdown

### Initialization

- Initializes the Llama 3.1 language model using the `Ollama` class.

### Summarization Function

- The `summarize_pdf` function reads the PDF and generates summaries for each page using the language model.

### Timing

- Tracks the start and end time of the summarization process and calculates the elapsed time in minutes.

### Save Summaries

- Saves the summarized content to `pdf_summaries.txt`, with a separator line between each page's summary.

### Crew Framework

- Defines a summarization tool function `pdf_summarizer_tool`.
- Uses templates to create an agent and a task for summarizing the PDF.
- Instantiates a `Crew` object to manage the summarization process and extracts the final summary.

## Example Output

```plaintext
Page 1 Summary:
...
----------------------------------------
Page 2 Summary:
...
----------------------------------------
...

Script took X.XX minutes to run.
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

```

Feel free to customize this `README.md` file further to suit your project's specifics.
