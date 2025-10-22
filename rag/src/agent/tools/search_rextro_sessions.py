from llama_index.core.tools import FunctionTool
import requests
import json
from typing import List, Optional

def search_rextro_sessions(
    query: Optional[str] = None, 
    tags: Optional[List[str]] = None, 
    page: int = 1, 
    limit: int = 10, 
    sortBy: str = "time", 
    sortOrder: str = "desc"
) -> str:
    """
    Searches for sessions on the Rextro API based on a query, tags,
    pagination, and sorting criteria.
    """
    print(f"Tool 'search_rextro_sessions' called with query={query}, tags={tags}, page={page}, limit={limit}")
    
    api_url = "https://rextro-api.internalbuildtools.online/sessions/search"
    headers = {"accept": "application/json"}
    
    # Start with pagination and sorting params
    params = {
        "page": page,
        "limit": limit,
        "sortBy": sortBy,
        "sortOrder": sortOrder
    }
    print(f"Constructed params so far: {params}")
    # Add optional filters only if they are provided
    if query:
        params["query"] = query
    
    if tags:
        # The API expects a comma-separated string for tags
        params["tags"] = ",".join(tags)

    try:
        response = requests.get(api_url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        data = response.json()
        return json.dumps(data, indent=2)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return f"HTTP Error: {http_err.response.status_code} - {http_err.response.text}"
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred: {req_err}")
        return f"Request Error: An error occurred while trying to reach the API. {req_err}"
    except Exception as e:
        print(f"An unexpected error occurred in search_rextro_sessions: {e}")
        return f"An unexpected error occurred: {e}"


search_rextro_sessions_tool = FunctionTool.from_defaults(
    fn=search_rextro_sessions,
    name="search_rextro_sessions",
    description=(
        "Use this tool to search for Rextro Exhibition sessions. "
        "You can optionally filter by a 'query' string and/or a list of 'tags'. "
        "You can also control pagination ('page', 'limit') and sorting ('sortBy', 'sortOrder')."
        "do not say these things in the response: "
    )
)

