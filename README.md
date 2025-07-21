# Ollama-MCP: Airbnb Search with PraisonAI Agents

A Python project that integrates **PraisonAI Agents** with **Ollama** and **Model Context Protocol (MCP)** to create an intelligent Airbnb apartment search system. The project provides both command-line and web-based interfaces for searching and booking apartments through AI agents.

## 🚀 Features

- **AI-Powered Search**: Uses PraisonAI agents with local Ollama models for intelligent apartment searches
- **MCP Integration**: Leverages Model Context Protocol with `@openbnb/mcp-server-airbnb` for real-time Airbnb data
- **Multiple Interfaces**: 
  - Command-line interface (`app.py`)
  - Web interface with Gradio (`airbnb.py` and `airbnb_formatted.py`)
- **Dynamic Model Selection**: Automatically detects available Ollama models
- **Flexible Search**: Natural language queries for apartment searches with date ranges and budgets

## 📋 Prerequisites

Before running this project, ensure you have:

1. **Python 3.12+** installed
2. **Ollama** running locally on `http://localhost:11434`
3. **Node.js and npm** (for MCP server)
4. **uv** package manager (recommended) or pip

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/goagiq/Ollama-MCP.git
   cd Ollama-MCP
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Ensure Ollama is running:**
   ```bash
   ollama serve
   ```

4. **Pull an Ollama model (if not already available):**
   ```bash
   ollama pull llama3.2:latest
   # or
   ollama pull mistral
   ```

## 📁 Project Structure

```
Ollama-MCP/
├── app.py                 # Simple command-line interface
├── airbnb.py             # Basic Gradio web interface
├── airbnb_formatted.py   # Enhanced Gradio interface with formatting
├── main.py               # Basic entry point
├── pyproject.toml        # Project dependencies
├── uv.lock              # Dependency lock file
└── README.md            # Project documentation
```

## 🎯 Usage

### Command Line Interface

Run the simple command-line version:

```bash
python app.py
```

This will execute a predefined search: *"Search for an apartment in Paris from 2025-08-01 to 2025-08-15 with a budget of $100 per night."*

### Web Interface (Basic)

Launch the basic Gradio interface:

```bash
python airbnb.py
```

### Web Interface (Enhanced)

Launch the enhanced Gradio interface with debugging and result formatting:

```bash
python airbnb_formatted.py
```

The web interface will be available at `http://localhost:7860` (or another port if 7860 is busy).

## 💡 Example Queries

Here are some example search queries you can try:

- `"Find a 2-bedroom apartment in New York from 2025-09-01 to 2025-09-07 under $150 per night"`
- `"Search for a studio in San Francisco with wifi and kitchen for one week in August"`
- `"Look for family-friendly apartments in London near tourist attractions for 5 nights"`
- `"Find pet-friendly accommodations in Barcelona with parking for a weekend stay"`

## 🔧 Configuration

### Ollama Models

The application automatically detects available Ollama models. You can:

1. **List available models:**
   ```bash
   ollama list
   ```

2. **Pull additional models:**
   ```bash
   ollama pull codellama
   ollama pull llama2
   ```

### MCP Server

The project uses the `@openbnb/mcp-server-airbnb` MCP server with the `--ignore-robots-txt` flag. This is automatically handled by the PraisonAI agent configuration.

## 🧩 Code Components

### PraisonAI Agent Configuration

```python
agent = Agent(
    instructions="""
    You help book an apartment on Airbnb. 
    Provide a list of apartments based on price per night, location, and amenities.
    Check the availability for given dates.
    """,
    llm="ollama/mistral",  # or any available Ollama model
    tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
)
```

### Key Features

- **Dynamic Model Detection**: Automatically discovers available Ollama models
- **Error Handling**: Graceful handling of connection issues and missing models
- **Result Formatting**: Enhanced parsing and presentation of search results
- **Debug Mode**: Comprehensive logging in the formatted version

## 🐛 Troubleshooting

### Common Issues

1. **"ImportError: No module named 'praisonaiagents'"**
   ```bash
   pip install praisonaiagents[knowledge,llm]
   ```

2. **"Error connecting to Ollama"**
   - Ensure Ollama is running: `ollama serve`
   - Check if models are available: `ollama list`

3. **"No Ollama models found"**
   ```bash
   ollama pull llama3.2:latest
   ```

4. **MCP Server Issues**
   - Ensure Node.js is installed
   - Check npm global packages: `npm list -g`

## 📚 Dependencies

Key dependencies include:

- **praisonaiagents**: AI agent framework
- **gradio**: Web interface framework
- **requests**: HTTP client for Ollama API
- **ollama**: Ollama Python client
- **asyncio**: Asynchronous programming support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🔗 Related Links

- [PraisonAI Documentation](https://docs.praison.ai/)
- [Ollama Official Site](https://ollama.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Gradio Documentation](https://gradio.app/docs/)

---

**Note**: This project is for educational and development purposes. Always respect Airbnb's terms of service and rate limits when using their data.