from llama_index.core.tools import FunctionTool
import requests
import json

def get_latest_3_sessions() -> str:
    """
    Fetches the 3 latest sessions from the Rextro API.
    (Hardcoded to page=1, limit=3, sortOrder=desc)
    """
    print("Tool 'get_latest_3_sessions' called")

    # The API endpoint
    api_url = "https://rextro-api.internalbuildtools.online/sessions"
    
    # Headers as specified
    headers = {
        "accept": "application/json"
    }
    
    # Parameters are now hardcoded to get the 3 latest sessions
    params = {
        "page": 1,
        "limit": 3,
        "sortOrder": "desc"
    }

    try:
        # Perform the GET request
        response = requests.get(api_url, headers=headers, params=params, verify=False)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        print(f"Fetched data: {data}")
        # Return the data as a formatted JSON string
        return json.dumps(data, indent=2)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return f"HTTP Error: {http_err.response.status_code} - {http_err.response.text}"
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        return f"Request Error: An error occurred while trying to reach the API. {req_err}"
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from response: {response.text}")
        return f"Error: The API did not return valid JSON. Received: {response.text}"
    except Exception as e:
        print(f"An unexpected error occurred in get_latest_3_sessions: {e}")
        return f"An unexpected error occurred: {e}"

# Create FunctionTool for llama_index using the new function
get_latest_3_sessions_tool = FunctionTool.from_defaults(
    fn=get_latest_3_sessions,
    name="get_latest_3_sessions",
    description=(
        "Use this tool to retrieve the 3 latest sessions from the Rextro Exhibition API. "
        "It does not take any parameters and always returns the top 3."
    )
)

