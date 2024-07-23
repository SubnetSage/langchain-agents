from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import tool
from PyPDF2 import PdfReader

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
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text()
    return text

# Load the NIST Special Publication 800-37
nist_guide_text = read_pdf("NIST.SP.800-37r2.pdf")

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

# Get the crew to start working on the initial research tasks
results = crew.kickoff()

# Extract the outputs from the initial research tasks
network_report = results[0]['output']
app_security_report = results[1]['output']
data_security_report = results[2]['output']
compliance_report = results[3]['output']
user_access_control_report = results[4]['output']

# Define the Writer agent
writer_role = 'Writer'
writer_goal = 'Compile the research from all specialists into a comprehensive cyber risk management plan in markdown format.'
writer_backstory = """
    You are a highly experienced technical writer with a strong background in cybersecurity and risk management. Your expertise lies in distilling complex technical research into clear, concise, and well-organized documents. 
    You have a meticulous eye for detail and a knack for transforming intricate data into accessible, actionable plans. Your role is to synthesize the provided research and compile it into a comprehensive, user-friendly cyber risk management plan, formatted in markdown for ease of use and distribution. 
    Your goal is to ensure that the plan is thorough, understandable, and practical for implementation.
"""
writer_tools = []

writer = create_agent(writer_role, writer_goal, writer_backstory, writer_tools, ollama_llm)

# Create the writing task for the Writer agent
writing_task_description = f"""
Compile the following research into a comprehensive cyber risk management plan in markdown format:

## Network Infrastructure Security
{network_report}

## Application Security
{app_security_report}

## Data Security
{data_security_report}

## Compliance Requirements
{compliance_report}

## User Access Control
{user_access_control_report}
"""
writing_task_expected_output = "A markdown formatted document containing the comprehensive cyber risk management plan."

writing_task = create_task(writer, writing_task_description, writing_task_expected_output)

# Add the writing task to a new Crew and kick it off
writing_crew = Crew(
    agents=[writer],
    tasks=[writing_task],
    verbose=2
)

writing_results = writing_crew.kickoff()

# Get the final markdown content from the writer
final_report = writing_results[0]['output']

# Print the final report
print(final_report)
