# Exchange Rate MCP Server

A Model Context Protocol (MCP) server that provides real-time currency exchange rate conversion using the ExchangeRate.host API. This server integrates with FastMCP and includes a Gradio web interface for easy testing and interaction.

## Features

- Real-time currency conversion using ExchangeRate.host API
- MCP tool integration for use with AI assistants
- Gradio web interface for interactive testing
- Environment variable configuration for API keys
- Support for multiple currency codes (USD, EUR, GBP, JPY, etc.)

## Prerequisites

- Python 3.13 or higher
- An API key from [ExchangeRate.host](https://exchangerate.host/) (free tier available)

## Installation

1. Clone or download this project
2. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Configuration

1. Create a `.env` file in the project root:
   ```env
   ACCESS_KEY=your_exchangerate_host_api_key_here
   ```

2. Get your free API key from [ExchangeRate.host](https://exchangerate.host/):
   - Sign up for a free account
   - Copy your API key to the `.env` file

## Usage

### Running the MCP Server

To run the exchange rate conversion server:

```bash
python exchangerate.py
```

This will launch both the MCP server and a Gradio web interface accessible at `http://localhost:7860`.

### Using the Gradio Interface

1. Enter the source currency code (e.g., "USD")
2. Enter the target currency code (e.g., "EUR")
3. Enter the amount to convert
4. Click submit to get the converted amount

### Using as an MCP Tool

The server exposes a `get_exchange_rate` tool that can be used by MCP-compatible clients:

**Function:** `get_exchange_rate(from_currency, to_currency, amount)`

**Parameters:**
- `from_currency` (string): Source currency code (e.g., "USD")
- `to_currency` (string): Target currency code (e.g., "EUR")
- `amount` (number): Amount to convert

**Returns:** Converted amount as a number

### Example Usage

```python
# Using the tool directly
result = get_exchange_rate("USD", "EUR", 100)
print(f"100 USD = {result} EUR")
```

## Supported Currency Codes

The API supports all major world currencies. Common examples include:
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)
- CHF (Swiss Franc)
- CNY (Chinese Yuan)

For a complete list, refer to the [ExchangeRate.host documentation](https://exchangerate.host/).

## API Response Format

The ExchangeRate.host API returns responses in the following format:

**Success Response:**
```json
{
  "success": true,
  "query": {
    "from": "USD",
    "to": "EUR",
    "amount": 100
  },
  "info": {
    "rate": 0.85
  },
  "result": 85.0
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": 101,
    "info": "Invalid API key"
  }
}
```

## Error Handling

The server includes error handling for:
- Invalid API keys
- Unsupported currency codes
- Network connectivity issues
- API rate limits

Error messages are returned in a user-friendly format.

## Development

### Testing

The project includes several test files:

- `test.py` - Basic functionality test with Gradio interface
- `test2_httpx.py` - Alternative implementation using httpx instead of requests
- `test3_stream.py` - Streaming implementation example

### Dependencies

Key dependencies include:
- `fastmcp` - FastMCP server framework
- `gradio` - Web interface for testing
- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management
- `mcp` - Model Context Protocol library

## Troubleshooting

### Common Issues

1. **"Invalid API key" error**
   - Verify your API key is correct in the `.env` file
   - Ensure you've signed up at ExchangeRate.host

2. **"Currency not supported" error**
   - Check that you're using valid 3-letter currency codes
   - Refer to the ExchangeRate.host documentation for supported currencies

3. **Network connection errors**
   - Check your internet connection
   - Verify the API endpoint is accessible

### Debug Mode

To enable debug logging, modify the code to include:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues and enhancement requests!

## API Rate Limits

The free tier of ExchangeRate.host includes:
- 1,000 API calls per month
- Real-time exchange rates
- 170+ currencies supported

For higher usage, consider upgrading to a paid plan.
