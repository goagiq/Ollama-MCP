import requests
from praisonaiagents import Agent, MCP
import gradio as gr

# Load environment variables from .env
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

OLLAMA_URL = "http://localhost:11434"  # Default Ollama URL

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

def get_ollama_models_html(models):
    html = '<div id="ollama-model-list">\n'
    for model in models:
        html += f'  <button type="button" class="ollama-model-btn" value="{model}">{model}</button>\n'
    html += '</div>'
    return html
    return html

ollama_models = get_ollama_models_http() if get_ollama_models_http() else ['gpt-4o-mini']

def search_airbnb_apartment(query, ollama_model):
    # If no Ollama model is selected, use default OpenAI model
    if not ollama_model or ollama_model == "gpt-4o-mini":
        agent = Agent(
            instructions="""
            You help book an apartment on Airbnb. 
            Provide a list of apartments based on price per night, location, and amenities.
            Check the availability for given dates.
            """,
            llm="openai/gpt-4o-mini",
            tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
        )
    else:
        agent = Agent(
            instructions="""
            You help book an apartment on Airbnb. 
            Provide a list of apartments based on price per night, location, and amenities.
            Check the availability for given dates.
            """,
            llm=f"ollama/{ollama_model}",
            tools=MCP("npx -y @openbnb/mcp-server-airbnb")
        )
        
    result = agent.start(query)
    return f"## Airbnb Search Results\n\n{result}"

def select_model_interface():
    def select_model(query, openai_model, ollama_model):
        # Use Ollama model if selected, otherwise use OpenAI model
        model = ollama_model if ollama_model else openai_model
        return search_airbnb_apartment(query, model)
    return gr.Interface(
        fn=select_model,
        inputs=[
            gr.Textbox(
                label="Search Query",
                placeholder="Enter your search query for Airbnb apartments, e.g., '2 bedroom apartment in New York from 2023-10-01 to 2023-10-07'."
            ),
            gr.Radio(choices=["gpt-4o-mini"], label="OpenAI", value="gpt-4o-mini"),
            gr.Radio(choices=ollama_models, label="Ollama Model")
        ],
        outputs=gr.Textbox(),
        title="🏠 AI-Powered Airbnb Search Assistant",
        description=(
            "Find the perfect apartment on Airbnb using AI. Enter your search "
            "criteria including location, dates, and preferences, and let our AI "
            "agent help you discover available properties with detailed "
            "information about pricing, amenities, and availability."
        ),
    )

if __name__ == "__main__":
    select_model_interface().launch(
        debug=True,
        app_kwargs={"title": "AI-Powered Airbnb Search Assistant"}
    )

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

ollama_models = get_ollama_models_http() if get_ollama_models_http() else ['gpt-4o-mini']

def search_airbnb_apartment(query, ollama_model):
    if not ollama_model:
        return "Please select an Ollama Model."
    
    agent = Agent(
        instructions="""
        You help book an apartment on Airbnb. 
        Provide a list of apartments based on price per night, location, and amenities.
        Check the availability for given dates.
        """,
        llm=f"ollama/{ollama_model}",
        tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
    )
    
    result = agent.start(query)
    return f"## Airbnb Search Results\n\n{result}"

ollama_models = ollama_models if ollama_models else ['gpt-4o-mini']

demo = gr.Interface(
    fn=search_airbnb_apartment,
    inputs=[
        gr.Textbox(
            label="Search Query",
            placeholder="Enter your search query for Airbnb apartments, e.g., '2 bedroom apartment in New York from 2023-10-01 to 2023-10-07'."
        ),
        gr.Dropdown(choices=ollama_models, label="Ollama Model", value='gpt-4o-mini', elem_id="ollama-model-select")
    ],
    outputs=gr.Textbox(),
    title="🏠 AI-Powered Airbnb Search Assistant",
    description=(
        "Find the perfect apartment on Airbnb using AI. Enter your search "
        "criteria including location, dates, and preferences, and let our AI "
        "agent help you discover available properties with detailed "
        "information about pricing, amenities, and availability."
    ),
)

if __name__ == "__main__":
    demo.launch(
        debug=True,
        reload_on_change=True,
        app_kwargs={"title": "AI-Powered Airbnb Search Assistant"}
    )
