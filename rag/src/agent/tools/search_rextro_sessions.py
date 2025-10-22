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


from llama_index.core.tools import FunctionTool

search_rextro_sessions_tool = FunctionTool.from_defaults(
    fn=search_rextro_sessions,
    name="search_rextro_sessions",
    description=(
        "Searches the Rextro Exhibition sessions API. "
        "You can optionally specify a free-text 'query' to match session titles or descriptions, "
        "and/or a list of 'tags' to filter by topic. "
        "Additionally, you can control the pagination (page number, items per page) and sorting (field and order). "
        "Returns the JSON response as a formatted string."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Optional search term to match session titles/descriptions."
            },
            "tags": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Optional list of tag identifiers to filter sessions by topic."
            },
            "page": {
                "type": "integer",
                "description": "Which page of results to return. Default is 1."
            },
            "limit": {
                "type": "integer",
                "description": "How many results to return per page. Default is 10."
            },
           
            "sortOrder": {
                "type": "string",
                "enum": ["asc", "desc"],
                "description": "Sorting direction: 'asc' for ascending, 'desc' for descending. Default is 'desc'."
            }
        },
        "required": []
    }
)

