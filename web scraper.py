import requests
from bs4 import BeautifulSoup
import openai

# Set your OpenAI API key here
openai.api_key = 'your-openai-api-key'

def scrape_website(url):
    # Fetch the webpage
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract relevant text content (you can adjust this to target specific tags)
    text_content = soup.get_text(separator="\n", strip=True)
    
    return text_content

def generate_ai_persona(website_content):
    # Define the persona template
    persona_template = """
    Create an AI persona based on the following structure using the provided content:

    1. Main Parts of the Persona
    1.1 Role: {role}
    1.2 Identity: {identity}
    1.3 Personality: {personality}
    1.4 Background: {background}
    1.5 Communication Style: {communication_style}
    1.6 Lifestyle: {lifestyle}
    1.7 Relationships: {relationships}
    1.8 Motivations and Goals: {motivations_and_goals}

    Here's the content to use:
    {website_content}
    """

    # Use OpenAI's ChatGPT to generate the persona
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=persona_template.format(
            role="(Define the role based on the content)",
            identity="(Define the identity based on the content)",
            personality="(Define the personality based on the content)",
            background="(Define the background based on the content)",
            communication_style="(Define the communication style based on the content)",
            lifestyle="(Define the lifestyle based on the content)",
            relationships="(Define the relationships based on the content)",
            motivations_and_goals="(Define the motivations and goals based on the content)",
            website_content=website_content
        ),
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    persona = response.choices[0].text.strip()
    return persona

def main():
    # URL of the website to scrape
    url = 'https://example.com'
    
    # Scrape the website content
    website_content = scrape_website(url)
    
    # Generate the AI persona
    ai_persona = generate_ai_persona(website_content)
    
    # Output the generated AI persona
    print("Generated AI Persona:")
    print(ai_persona)

if __name__ == "__main__":
    main()
