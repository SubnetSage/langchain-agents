from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from PyPDF2 import PdfReader

# Initialize the LLM model
ollama_llm = Ollama(model="llama3.1")

# Function to read and summarize each page of the PDF
def summarize_pdf(file_path, llm_model):
    reader = PdfReader(file_path)
    summaries = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # Wrap the text in a list
            response = llm_model.generate(prompts=[f"Summarize the following text:\n\n{text}"])
            # Access the correct part of the response
            summary = response.generations[0][0].text
            summaries.append(f"Page {i+1} Summary:\n{summary}\n")
    return "\n".join(summaries)

# Load the document and summarize each page
pdf_summary = summarize_pdf("your_pdf_file.pdf", ollama_llm)

# Define the summarization tool function
@tool("PDF_Summarizer")
def pdf_summarizer_tool(pdf_path: str) -> str:
    """This tool summarizes the content of a given PDF file."""
    return summarize_pdf(pdf_path, ollama_llm)

# Template for agent creation
def create_agent(role, goal, backstory, tools, llm, verbose=True, allow_delegation=True):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        llm=llm,
        verbose=verbose,
        allow_delegation=allow_delegation
    )

# Template for task creation
def create_task(agent, description, expected_output):
    return Task(
        agent=agent,
        description=description,
        expected_output=expected_output
    )

# Define the role for the PDF summarization agent
pdf_summarizer_role = 'Document Summarization Agent'
pdf_summarizer_goal = 'Summarize each page of the provided PDF document.'
pdf_summarizer_backstory = """
    You are an expert document summarization agent who excels at simplifying complex content. 
    Your task is to read and summarize each page of the given PDF document.
"""
pdf_summarizer_tools = [pdf_summarizer_tool]

# Create the summarization agent using the template
pdf_summarizer_agent = create_agent(pdf_summarizer_role, pdf_summarizer_goal, pdf_summarizer_backstory, pdf_summarizer_tools, ollama_llm)

# Create the summarization task using the template
summarization_task = create_task(pdf_summarizer_agent, "Summarize each page of the provided PDF document.", "A summary of each page of the PDF document.")

# Instantiate the Crew with the summarization process
crew = Crew(
    agents=[pdf_summarizer_agent],
    tasks=[summarization_task],
    verbose=2  # Adjust the logging level as needed (1 or 2)
)

# Get the crew to start working on the summarization task
results = crew.kickoff()

# Extract the summary from the task result
final_summary = results[0].output

# Print the final summary
print(final_summary)
