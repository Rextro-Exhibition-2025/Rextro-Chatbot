from llama_index.core.tools import FunctionTool
import requests
import json
from typing import List, Optional


def get_zones(
    page: int = 1, 
    limit: int = 10, 
    sortBy: str = "createdAt", 
    sortOrder: str = "desc"
) -> str:
    """
    Fetches a list of zones from the Rextro API based on pagination and sorting.
    """
    print(f"Tool 'get_zones' called with page={page}, limit={limit}, sortBy={sortBy}, sortOrder={sortOrder}")
    
    api_url = "https://rextro-api.internalbuildtools.online/zones"
    headers = {"accept": "application/json"}
    
    # Parameters for the request, using the defaults from your curl command
    params = {
        "page": page,
        "limit": limit,
        "sortBy": sortBy,
        "sortOrder": sortOrder
    }

    try:
        response = requests.get(api_url, headers=headers, params=params, verify=False)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()
        return json.dumps(data, indent=2)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return f"HTTP Error: {http_err.response.status_code} - {http_err.response.text}"
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        return f"Request Error: An error occurred while trying to reach the API. {req_err}"
    except Exception as e:
        print(f"An unexpected error occurred in get_zones: {e}")
        return f"An unexpected error occurred: {e}"





get_zones_tool = FunctionTool.from_defaults(
    fn=get_zones,
    name="get_zones",
    description=(
        "Use this tool to retrieve a list of Rextro Exhibition zones. "
        "You can control pagination ('page', 'limit') and sorting ('sortBy', 'sortOrder')."
               "do not say these things in the response: "
    )
)

