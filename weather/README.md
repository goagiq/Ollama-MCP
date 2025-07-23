# Weather MCP Server

A Model Context Protocol (MCP) server that provides real-time weather information using the National Weather Service (NWS) API. This server offers weather alerts and detailed forecasts for locations within the United States.

## Features

- Real-time weather alerts for US states
- Detailed weather forecasts for specific coordinates
- Integration with official National Weather Service API
- MCP tool integration for use with AI assistants
- Async HTTP client for efficient API requests
- Comprehensive error handling and timeout management
- User-friendly formatted weather data

## Prerequisites

- Python 3.13 or higher
- Internet connection for NWS API access
- No API key required (uses free NWS API)

## Installation

1. Clone or download this project
2. Install dependencies using uv:
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install httpx mcp[cli]
   ```

## Usage

### Running the MCP Server

Start the weather MCP server:

```bash
python main.py
```

This will start the MCP server using stdio transport, making it available for MCP-compatible clients.

### Available Tools

The server exposes two main tools:

#### 1. Get Weather Alerts (`get_alerts`)

Retrieves active weather alerts for a US state.

**Parameters:**
- `state` (string): Two-letter US state code (e.g., "CA", "NY", "TX")

**Example Usage:**
```python
# Get alerts for California
get_alerts("CA")

# Get alerts for New York
get_alerts("NY")
```

**Sample Output:**
```
Event: Severe Thunderstorm Warning
Area: Los Angeles County
Severity: Severe
Description: A severe thunderstorm warning has been issued...
Instructions: Move to an interior room on the lowest floor of a building...
---
Event: Heat Advisory
Area: San Fernando Valley
Severity: Moderate
Description: Hot temperatures are expected...
Instructions: Drink plenty of fluids, stay in an air-conditioned room...
```

#### 2. Get Weather Forecast (`get_forecast`)

Retrieves detailed weather forecast for specific coordinates.

**Parameters:**
- `latitude` (float): Latitude of the location (e.g., 34.0522)
- `longitude` (float): Longitude of the location (e.g., -118.2437)

**Example Usage:**
```python
# Get forecast for Los Angeles, CA
get_forecast(34.0522, -118.2437)

# Get forecast for New York, NY
get_forecast(40.7128, -74.0060)
```

**Sample Output:**
```
Today:
Temperature: 75°F
Wind: 10 mph W
Forecast: Partly cloudy with scattered showers in the afternoon...
---
Tonight:
Temperature: 60°F
Wind: 5 mph SW
Forecast: Mostly clear skies with light winds...
---
Tomorrow:
Temperature: 78°F
Wind: 12 mph NW
Forecast: Sunny with a few clouds developing in the late afternoon...
```

## API Integration

This server integrates with the **National Weather Service (NWS) API**, which provides:

- **Base URL**: `https://api.weather.gov`
- **No Authentication Required**: Free public API
- **Coverage**: United States and its territories
- **Data Format**: GeoJSON and standard JSON responses
- **Update Frequency**: Real-time updates from NWS stations

### API Endpoints Used

1. **Alerts Endpoint**: `/alerts/active/area/{state}`
   - Retrieves active weather alerts for a specific state
   - Returns alerts with severity, description, and instructions

2. **Points Endpoint**: `/points/{latitude},{longitude}`
   - Gets weather grid information for coordinates
   - Returns forecast URLs for the location

3. **Forecast Endpoint**: `/gridpoints/{office}/{gridX},{gridY}/forecast`
   - Provides detailed weather forecasts
   - Returns periods with temperature, wind, and detailed descriptions

## Supported US State Codes

The weather alerts tool supports all US states and territories:

**States:**
- AL (Alabama), AK (Alaska), AZ (Arizona), AR (Arkansas)
- CA (California), CO (Colorado), CT (Connecticut), DE (Delaware)
- FL (Florida), GA (Georgia), HI (Hawaii), ID (Idaho)
- IL (Illinois), IN (Indiana), IA (Iowa), KS (Kansas)
- KY (Kentucky), LA (Louisiana), ME (Maine), MD (Maryland)
- MA (Massachusetts), MI (Michigan), MN (Minnesota), MS (Mississippi)
- MO (Missouri), MT (Montana), NE (Nebraska), NV (Nevada)
- NH (New Hampshire), NJ (New Jersey), NM (New Mexico), NY (New York)
- NC (North Carolina), ND (North Dakota), OH (Ohio), OK (Oklahoma)
- OR (Oregon), PA (Pennsylvania), RI (Rhode Island), SC (South Carolina)
- SD (South Dakota), TN (Tennessee), TX (Texas), UT (Utah)
- VT (Vermont), VA (Virginia), WA (Washington), WV (West Virginia)
- WI (Wisconsin), WY (Wyoming)

**Territories:**
- DC (District of Columbia), PR (Puerto Rico), VI (Virgin Islands)
- GU (Guam), AS (American Samoa), MP (Northern Mariana Islands)

## Error Handling

The server includes comprehensive error handling:

- **Network Timeouts**: 30-second timeout for API requests
- **API Failures**: Graceful handling of NWS API downtime
- **Invalid Coordinates**: Proper error messages for out-of-bounds locations
- **Invalid State Codes**: Handling of non-existent state codes
- **Data Parsing**: Safe handling of malformed API responses

**Common Error Responses:**
- `"Unable to fetch alerts or no alerts found."` - API error or no data
- `"No active alerts for this state."` - No current alerts
- `"Unable to fetch forecast data for this location."` - Invalid coordinates
- `"Unable to fetch detailed forecast."` - Forecast API error

## Location Coverage

### Geographic Limitations

The NWS API only provides weather data for:
- **United States** (all 50 states)
- **US Territories** (Puerto Rico, US Virgin Islands, Guam, etc.)
- **Surrounding Waters** (Atlantic, Pacific, Gulf of Mexico)

**Coordinates outside the US will return errors.**

### Finding Coordinates

To get latitude and longitude for locations:

1. **Google Maps**: Right-click on location, select coordinates
2. **GPS Devices**: Most smartphones show coordinates in location settings
3. **Online Tools**: Use geocoding services to convert addresses
4. **Weather Apps**: Many display coordinates for saved locations

**Example Coordinates:**
- Los Angeles, CA: `34.0522, -118.2437`
- New York, NY: `40.7128, -74.0060`
- Chicago, IL: `41.8781, -87.6298`
- Miami, FL: `25.7617, -80.1918`
- Seattle, WA: `47.6062, -122.3321`

## Development

### Project Structure

```
weather/
├── main.py              # Main MCP server application
├── pyproject.toml       # Project configuration
├── README.md           # This file
├── uv.lock             # Dependency lock file
├── .gitignore          # Git ignore rules
└── .python-version     # Python version specification
```

### Dependencies

- **httpx**: Modern async HTTP client for API requests
- **mcp**: Model Context Protocol library and CLI tools
- **fastmcp**: FastMCP server framework (imported from mcp.server.fastmcp)

### Code Architecture

```python
# Main components:
1. FastMCP server initialization
2. NWS API request helper function
3. Data formatting functions
4. Two main MCP tools:
   - get_alerts(state)
   - get_forecast(latitude, longitude)
```

### Adding New Features

To extend the weather server:

1. **Add new tools**: Use the `@mcp.tool()` decorator
2. **Extend API coverage**: Add new NWS endpoints
3. **Improve formatting**: Enhance data presentation
4. **Add caching**: Implement response caching for performance

## Usage Examples

### MCP Client Integration

```python
# Example of using in an MCP client
import asyncio
from mcp import ClientSession

async def get_weather_info():
    # Get alerts for Texas
    alerts = await client.call_tool("get_alerts", {"state": "TX"})
    print("Texas Weather Alerts:")
    print(alerts)
    
    # Get forecast for Austin, TX
    forecast = await client.call_tool("get_forecast", {
        "latitude": 30.2672,
        "longitude": -97.7431
    })
    print("Austin Weather Forecast:")
    print(forecast)
```

### Command Line Testing

```bash
# Test the server directly
echo '{"method": "tools/call", "params": {"name": "get_alerts", "arguments": {"state": "CA"}}}' | python main.py

# Test forecast tool
echo '{"method": "tools/call", "params": {"name": "get_forecast", "arguments": {"latitude": 34.0522, "longitude": -118.2437}}}' | python main.py
```

## Troubleshooting

### Common Issues

1. **"Unable to fetch alerts" error**
   - Check internet connection
   - Verify the state code is valid (2 letters, uppercase)
   - NWS API may be temporarily unavailable

2. **"Unable to fetch forecast data" error**
   - Verify coordinates are within the United States
   - Check latitude/longitude format (decimal degrees)
   - Ensure coordinates are not over water (some areas unsupported)

3. **Server won't start**
   - Verify Python 3.13+ is installed
   - Check all dependencies are installed: `uv sync`
   - Ensure no other process is using stdio

4. **Timeout errors**
   - Check network connectivity
   - NWS API may be experiencing high load
   - Try again in a few minutes

### Debug Mode

To enable detailed logging, modify the main.py file:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API Status

Check NWS API status at:
- **Status Page**: https://www.weather.gov/
- **API Documentation**: https://www.weather.gov/documentation/services-web-api

## Data Sources and Attribution

This application uses data from:
- **National Weather Service (NWS)**: Official weather data for the US
- **NOAA**: National Oceanic and Atmospheric Administration
- **Weather Forecast Offices**: Local NWS offices nationwide

**Data Attribution**: Weather data provided by the National Weather Service, National Oceanic and Atmospheric Administration.

## Limitations

- **Geographic Coverage**: US and territories only
- **Language**: English only
- **Updates**: Dependent on NWS data refresh rates
- **Historical Data**: Only current and forecast data (no historical)
- **Marine Areas**: Limited coverage for offshore areas

## Contributing

Feel free to submit issues and enhancement requests!

**Potential Improvements:**
- Add weather radar data integration
- Include weather maps and satellite imagery
- Add weather station data
- Implement data caching for performance
- Add international weather support

## License

This project is provided as-is for educational and development purposes.

## Support

For NWS API issues, visit: https://www.weather.gov/documentation/services-web-api

For project-specific issues, please create an issue in this repository.
