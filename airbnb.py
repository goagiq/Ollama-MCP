import requests 
from praisonaiagents import Agent, MCP
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")  # Default Ollama URL
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_ollama_models_http():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        model_names = [model['name'] for model in data['models']]
        return model_names
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return []

ollama_models = get_ollama_models_http() if get_ollama_models_http() else ['llama3.2:latest']

def search_airbnb_apartment(query, ollama_model):
    if not OPENAI_API_KEY and not ollama_model:
        return "Please set OPENAI_API_KEY in .env file or select an Ollama Model."
    
    # Use OpenAI if API key is available, otherwise use Ollama
    if OPENAI_API_KEY:
        llm_config = "gpt-4o-mini"
    else:
        llm_config = f"ollama/{ollama_model}"
    
    agent = Agent(
        instructions="""
        You help book an apartment on Airbnb. 
        Provide a list of apartments based on price per night, location, and amenities.
        Check the availability for given dates.
        """,
        llm=llm_config,
        tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
    )
    
    result = agent.start(query)
    return f"## Airbnb Search Results\n\n{result}"

ollama_models = ollama_models if ollama_models else ['llama3.2:latest']

demo = gr.Interface(
    fn=search_airbnb_apartment,
    inputs=[
        gr.Textbox(
            label="Search Query",
            placeholder="Enter your search query for Airbnb apartments, e.g., '2 bedroom apartment in New York from 2023-10-01 to 2023-10-07'."
        ),
        gr.Dropdown(choices=ollama_models, label="Ollama Model (used only if no OpenAI API key)", value='llama3.2:latest')
    ],
    outputs=gr.Textbox(),
    title="Airbnb Apartment Search",
    description=f"Search for an apartment on Airbnb. {'Using OpenAI API' if OPENAI_API_KEY else 'Using Ollama local models'}.",
)

if __name__ == "__main__":
    demo.launch(server_port=8002)