import asyncio
import requests
from praisonaiagents import Agent, MCP
import gradio as gr

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

ollama_models = get_ollama_models_http() if get_ollama_models_http() else ['llama3.2:latest']

def search_airbnb_apartment(query, ollama_model):
    if not ollama_model:
        return "Please select an Ollama Model."

    print(f"Selected Ollama Model: {ollama_model}")
    print(f"Search Query: {query}")

    agent = Agent(
        instructions="""
        You help book an apartment on Airbnb.
        Provide a list of apartments based on price per night, location, and amenities.
        Check the availability for given dates.
        """,
        llm=f"ollama/{ollama_model}",
        tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
    )

    # Debugging: Print the agent configuration
    print(f"Agent Configuration: {agent}")

    result = agent.start(query)
    print(f"Agent Result: {result}")

    formatted_result = format_airbnb_results(result)
    print(f"Formatted Result: {formatted_result}")  # Debugging statement
    return formatted_result

def format_airbnb_results(result):
    if not isinstance(result, dict) or 'data' not in result:
        return "No results found."

    formatted_results = []
    for item in result['data']['results']:
        try:
            listing_id = item.get('id', '')
            name = item.get('name', '')
            latlng = item.get('latlng', '')
            icon = item.get('icon', '')

            formatted_result = (
                f"ID: {listing_id}\n"
                f"Name: {name}\n"
                f"Location: Latitude {latlng}, Icon URL: {icon}\n"
            )
            formatted_results.append(formatted_result)
        except KeyError:
            continue

    return "\n".join(formatted_results)

ollama_models = ollama_models if ollama_models else ['llama3.2:latest']

demo = gr.Interface(
    fn=search_airbnb_apartment,
    inputs=[
        gr.Textbox(label="Search Query", placeholder="Enter your search query here..."),
        gr.Dropdown(choices=ollama_models, label="Ollama Model", value='llama3.2:latest')
    ],
    outputs=gr.Textbox(),
    title="Airbnb Apartment Search",
    description="Search for an apartment on Airbnb.",
)

if __name__ == "__main__":
    demo.launch()