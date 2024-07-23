from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import tool
import PyPDF2

# Initialize the LLM model
ollama_llm = Ollama(model="llama3")

# Define the DuckDuckGo Search tool
@tool("Duck_Duck_Go_Search")
def ddgsearch(question: str) -> str:
    """This tool performs a DuckDuckGo search to find relevant information on the given question."""
    return DuckDuckGoSearchRun().run(question)

# Function to read the PDF guide
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

# Load the NIST Special Publication 800-37
nist_guide_text = read_pdf("path/to/NIST_SP_800-37.pdf")

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

# Define the roles and tasks for the cyber risk management plan

# Network Infrastructure Specialist
network_specialist_role = 'Network Infrastructure Specialist'
network_specialist_goal = 'Research and identify best practices for securing network infrastructure in small businesses.'
network_specialist_backstory = f"""
    You are a network infrastructure specialist responsible for researching the best practices for securing network infrastructure, tailored for small businesses. 
    Ensure all findings and recommendations comply with the NIST Special Publication 800-37.
    Here is the guide for reference: {nist_guide_text[:500]}... (truncated)
    Use the DuckDuckGoSearch tool to assist in your research.
"""
network_specialist_tools = [ddgsearch]

# Application Security Specialist
app_security_specialist_role = 'Application Security Specialist'
app_security_specialist_goal = 'Research best practices for securing enterprise applications used by small businesses.'
app_security_specialist_backstory = f"""
    You are an application security specialist focusing on researching the best practices for securing enterprise applications used by small businesses. 
    Ensure all findings and recommendations comply with the NIST Special Publication 800-37.
    Here is the guide for reference: {nist_guide_text[:500]}... (truncated)
    Use the DuckDuckGoSearch tool to assist in your research.
"""
app_security_specialist_tools = [ddgsearch]

# Data Security Specialist
data_security_specialist_role = 'Data Security Specialist'
data_security_specialist_goal = 'Research best practices for securing data storage and handling processes in small businesses.'
data_security_specialist_backstory = f"""
    You are a data security specialist responsible for researching the best practices for securing data storage, transmission, and handling processes in small businesses. 
    Ensure all findings and recommendations comply with the NIST Special Publication 800-37.
    Here is the guide for reference: {nist_guide_text[:500]}... (truncated)
    Use the DuckDuckGoSearch tool to assist in your research.
"""
data_security_specialist_tools = [ddgsearch]

# Compliance Specialist
compliance_specialist_role = 'Compliance Specialist'
compliance_specialist_goal = 'Research compliance requirements and best practices for small businesses to follow relevant regulations and standards.'
compliance_specialist_backstory = f"""
    You are a compliance specialist responsible for researching compliance requirements and best practices for small businesses to ensure adherence to relevant regulations and industry standards. 
    Ensure all findings and recommendations comply with the NIST Special Publication 800-37.
    Here is the guide for reference: {nist_guide_text[:500]}... (truncated)
    Use the DuckDuckGoSearch tool to assist in your research.
"""
compliance_specialist_tools = [ddgsearch]

# User Access Control Specialist
user_access_control_specialist_role = 'User Access Control Specialist'
user_access_control_specialist_goal = 'Research best practices for implementing effective user access controls and policies in small businesses.'
user_access_control_specialist_backstory = f"""
    You are a user access control specialist focusing on researching the best practices for implementing effective user access controls and policies in small businesses. 
    Ensure all findings and recommendations comply with the NIST Special Publication 800-37.
    Here is the guide for reference: {nist_guide_text[:500]}... (truncated)
    Use the DuckDuckGoSearch tool to assist in your research.
"""
user_access_control_specialist_tools = [ddgsearch]

# Create agents using the template
network_specialist = create_agent(network_specialist_role, network_specialist_goal, network_specialist_backstory, network_specialist_tools, ollama_llm)
app_security_specialist = create_agent(app_security_specialist_role, app_security_specialist_goal, app_security_specialist_backstory, app_security_specialist_tools, ollama_llm)
data_security_specialist = create_agent(data_security_specialist_role, data_security_specialist_goal, data_security_specialist_backstory, data_security_specialist_tools, ollama_llm)
compliance_specialist = create_agent(compliance_specialist_role, compliance_specialist_goal, compliance_specialist_backstory, compliance_specialist_tools, ollama_llm)
user_access_control_specialist = create_agent(user_access_control_specialist_role, user_access_control_specialist_goal, user_access_control_specialist_backstory, user_access_control_specialist_tools, ollama_llm)

# Create tasks using the template
task1 = create_task(network_specialist, "Research and identify best practices for securing network infrastructure in small businesses.", "A detailed report on best practices for securing network infrastructure tailored for small businesses.")
task2 = create_task(app_security_specialist, "Research best practices for securing enterprise applications used by small businesses.", "A comprehensive report on best practices for securing enterprise applications used by small businesses.")
task3 = create_task(data_security_specialist, "Research best practices for securing data storage and handling processes in small businesses.", "A thorough report on best practices for securing data storage and handling processes in small businesses.")
task4 = create_task(compliance_specialist, "Research compliance requirements and best practices for small businesses to follow relevant regulations and standards.", "A detailed report on compliance requirements and best practices for small businesses.")
task5 = create_task(user_access_control_specialist, "Research best practices for implementing effective user access controls and policies in small businesses.", "A comprehensive report on best practices for implementing effective user access controls and policies in small businesses.")

# Instantiate the Crew with a collaborative process
crew = Crew(
    agents=[network_specialist, app_security_specialist, data_security_specialist, compliance_specialist, user_access_control_specialist],
    tasks=[task1, task2, task3, task4, task5],
    verbose=2  # Adjust the logging level as needed (1 or 2)
)

# Get the crew to start working
result = crew.kickoff()

# Combine all recommendations into a single markdown file
report_content = """
# Cyber Risk Management Plan for Small Business

## Network Infrastructure Security
{}

## Application Security
{}

## Data Security
{}

## Compliance Requirements
{}

## User Access Control
{}
"""

network_report = task1.get_output()
app_security_report = task2.get_output()
data_security_report = task3.get_output()
compliance_report = task4.get_output()
user_access_control_report = task5.get_output()

final_report = report_content.format(network_report, app_security_report, data_security_report, compliance_report, user_access_control_report)

# Save the report to a .md file
report_filename = "Cyber_Risk_Management_Plan.md"
with open(report_filename, "w") as report_file:
    report_file.write(final_report)

print(f"Cyber risk management plan has been saved to {report_filename}")
