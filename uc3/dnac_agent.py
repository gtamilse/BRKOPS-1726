import os
import json
import logging
import difflib
import re
import requests
from requests.auth import HTTPBasicAuth
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool, render_text_description
import urllib3
from dotenv import load_dotenv, find_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Load environment variables from a .env file
load_dotenv(find_dotenv())

# Retrieve DNAC credentials from environment variables
dnac_url = os.getenv('DNAC_URL')
dnac_usr = os.getenv('DNAC_USERNAME')
dnac_pwd = os.getenv('DNAC_PASSWORD')

if not dnac_url or not dnac_usr or not dnac_pwd:
    logger.error("DNAC credentials are not set in the environment variables.")
    raise EnvironmentError("DNAC credentials are not set in the environment variables.")

class DNACController:
    """
    A class to interact with the Cisco DNAC controller.
    """

    def __init__(self, dnac_url, username, password):
        """
        Initialize the DNACController with the given URL, username, and password.
        """
        self.dnac = dnac_url.rstrip('/')
        self.username = username
        self.password = password
        self.cookie = self.get_token()

    def get_token(self):
        """
        Authenticate with the DNAC controller and retrieve a token.
        """
        url = f"{self.dnac}/dna/system/api/v1/auth/token"
        try:
            response = requests.post(url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
            response.raise_for_status()
            token = response.json()['Token']
            logger.info("Successfully retrieved token from DNAC")
            return token
        except requests.HTTPError as e:
            logger.error(f"HTTP error occurred while retrieving token: {e}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while retrieving token: {e}")
            raise

    def get_api(self, api_url: str):
        """
        Perform a GET request to the specified DNAC API URL.
        """
        try:
            headers = {
                'X-Auth-Token': self.cookie,
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{self.dnac}{api_url}", headers=headers, verify=False)
            response.raise_for_status()
            logger.info(f"Successfully retrieved data from DNAC API: {api_url}")
            return response.json()
        except requests.HTTPError as e:
            logger.error(f"HTTP error occurred while fetching data from DNAC API: {e}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while fetching data from DNAC API: {e}")
            raise

def load_urls(file_path='dnac_urls.json'):
    """
    Load supported URLs from a JSON file.
    """
    if not os.path.exists(file_path):
        error_message = f"File not found: {file_path}"
        logger.error(error_message)
        return {"error": error_message}
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        url_list = [(entry['URL'], entry.get('Name', '')) for entry in data]
        return url_list
    except Exception as e:
        error_message = f"Error loading URLs: {str(e)}"
        logger.error(error_message)
        return {"error": error_message}

def check_url_support(api_url: str) -> dict:
    """
    Check if the given API URL or Name is supported by the DNAC controller.
    """
    url_list = load_urls()
    if "error" in url_list:
        return url_list

    urls = [entry[0] for entry in url_list]
    names = [entry[1] for entry in url_list]

    close_url_matches = difflib.get_close_matches(api_url, urls, n=1, cutoff=0.6)
    close_name_matches = difflib.get_close_matches(api_url, names, n=1, cutoff=0.6)

    if close_url_matches:
        closest_url = close_url_matches[0]
        matching_name = [entry[1] for entry in url_list if entry[0] == closest_url][0]
        return {"status": "supported", "closest_url": closest_url, "closest_name": matching_name}
    elif close_name_matches:
        closest_name = close_name_matches[0]
        closest_url = [entry[0] for entry in url_list if entry[1] == closest_name][0]
        return {"status": "supported", "closest_url": closest_url, "closest_name": closest_name}
    else:
        return {"status": "unsupported", "message": f"The input '{api_url}' is not supported. Please check the available URLs or Names."}

@tool
def check_url_support_tool(api_url: str) -> dict:
    """
    Tool to check if an API URL or Name is supported by the DNAC controller.
    """
    result = check_url_support(api_url)
    if result.get('status') == 'supported':
        closest_url = result['closest_url']
        closest_name = result['closest_name']
        return {
            "status": "supported",
            "message": f"The closest supported API URL is '{closest_url}' ({closest_name}).",
            "action": {
                "next_tool": "get_dnac_data_tool",
                "input": closest_url
            }
        }
    return result

@tool
def get_dnac_data_tool(api_url: str) -> dict:
    """
    Tool to fetch data from the DNAC controller using the specified API URL.
    """
    try:
        sanitized_url = api_url.strip()  # Remove leading and trailing whitespace
        sanitized_url = re.sub(r'[\n\r\t]', '', sanitized_url)  # Remove newline, tab, and carriage return characters
        sanitized_url = re.sub(r'["\'\s]+$', '', sanitized_url)  # Remove trailing quotes and extra spaces
        logger.info(f"Using sanitized API URL: {sanitized_url}")
        
        dnac_controller = DNACController(dnac_url=dnac_url, username=dnac_usr, password=dnac_pwd)
        data = dnac_controller.get_api(sanitized_url)
    
        # dnac_controller = DNACController(dnac_url=dnac_url, username=dnac_usr, password=dnac_pwd)
        # data = dnac_controller.get_api(api_url)
        logger.info(f"Successfully fetched data from DNAC API: {api_url}")
        return {"status": "success", "data": data}
    except requests.HTTPError as e:
        error_message = f"Failed to fetch data from DNAC Controller: {str(e)}"
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"Error getting data from DNAC Controller: {str(e)}"
        logger.error(error_message)
        return {"status": "error", "message": error_message}

# Create list of tools
dnac_tools = [check_url_support_tool, get_dnac_data_tool]

# Render Text Description for the tools
tool_description = render_text_description(dnac_tools)

# Create OPENAI PROMPT TEMPLATE
template = """
Agent is a network assistant with the capability to manage data from Cisco DNAC, also known as Catalyst Center controllers, using API Requests.

NETWORK INSTRUCTIONS:

Assistant is designed to retrieve information from the Cisco DNAC controller using provided tools. You MUST use these tools for checking available data and fetching that data.

Assistant has access to a list of API URLs and their associated Names provided in a 'urls.json' file. You can use the 'Name' field to find the appropriate API URL to use.

**Important Guidelines:**

1. **If you are certain of the API URL or the Name of the data you want, use the 'get_dnac_data_tool' to fetch data.**
2. **If you are unsure of the API URL or Name, or if there is ambiguity, use the 'check_url_support_tool' to verify the URL or Name or get a list of available ones.**
3. **After observing the output of any tool, analyze it thoroughly to ensure it aligns with the intended purpose before proceeding to the next action.**
4. **If the 'check_url_support_tool' finds a valid URL or Name, automatically use the appropriate tool to perform the action.**
5. **Pause and reflect after every observation to ensure the output is complete and accurate. Consider whether another action is necessary or if the process is complete.**
6. **Do NOT use any unsupported URLs or Names.**
7. If you encounter 404 Client Errors then stop the process and communicate error back to the human.

**Using the Tools:**

- If you are confident about the API URL or Name, use the appropriate tool (e.g., 'get_dnac_data_tool').
- If there is any doubt or ambiguity, always check the URL or Name first with the 'check_url_support_tool'.

To use a tool, follow this format:

Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

**Pause and Analyze:**  
After observing the result, take time to evaluate whether the output aligns with the intended purpose. Reflect on these questions before taking the next action:  
- Does the observation provide the required information or resolve the ambiguity?  
- Are there any inconsistencies or missing details in the output?  
- Is another action required to complete the task?  

If the first tool provides a valid URL or Name, you MUST immediately run the correct tool for the operation (fetch, create, update, or delete) without waiting for another input. Follow the flow like this:

**Example:**

Thought: Do I need to use a tool? Yes
Action: check_url_support_tool
Action Input: "Device List Nodes"
Observation: "The closest supported API URL is '/dna/intent/api/v1/network-device' (Device List)."

Thought: Do I need to use a tool? Yes
Action: get_dnac_data_tool
Action Input: "/dna/intent/api/v1/network-device"
Observation: [retrieved data here]

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

Thought: Do I need to use a tool? No
Final Answer: [your response here]

**Correct Formatting is Essential:** Ensure that every response follows the format strictly to avoid errors.

TOOLS:

Assistant has access to the following tools:

- check_url_support_tool: Checks if an API URL or Name is supported by the DNAC controller.
- get_dnac_data_tool: Fetches data from the DNAC controller using the specified API URL.

**Important:** Always slow down between cycles, analyze the output of the action, and consider all aspects of the observation before proceeding.

Begin!

Previous conversation history:

{chat_history}

New input: {input}

{agent_scratchpad}
"""

# Define input variables
input_variables = ["input", "agent_scratchpad"]

# Create the PromptTemplate
dnac_prompt_template = PromptTemplate(
  template=template,
  input_variables=input_variables,
  partial_variables={
      "tools": tool_description,
      "tool_names": ", ".join([t.name for t in dnac_tools])
  }
)