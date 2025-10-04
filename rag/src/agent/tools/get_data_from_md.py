from llama_index.core.tools import FunctionTool
import os

# Path to your markdown file (update as needed)
MD_FILE_PATH = "./data/md_files/sample.md"

def get_data_from_md(query_text: str = None) -> str:
    """
    Reads the full content of a markdown file and returns it as a string.
    The query_text parameter is ignored (kept only for compatibility).
    """
    print(f"Tool 'get_data_from_md' called")

    if not os.path.exists(MD_FILE_PATH):
        return f"Error: Markdown file not found at {MD_FILE_PATH}"

    try:
        with open(MD_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        return f"Full content of {MD_FILE_PATH}:\n\n{content}"

    except Exception as e:
        print(f"Error in get_data_from_md tool: {e}")
        return f"An error occurred while reading the markdown file: {e}"


# Create FunctionTool for llama_index
get_data_from_md_tool = FunctionTool.from_defaults(
    fn=get_data_from_md,
    name="get_data_from_md",
    description=(
        "Use this tool to retrieve the full content about Rextro Exhibition of a markdown file. "
        "It ignores the query text and simply returns the raw text from the file."
    )
)
