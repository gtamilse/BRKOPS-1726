import os
import logging
import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import urllib3

# Import the tools and prompt templates for the main agent
from dnac_agent import dnac_tools, dnac_prompt_template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv(find_dotenv())

# Initialize OpenAI LLM
try:
    llm = ChatOpenAI(model="gpt-4o-mini")
    logger.info("Initialized OpenAI LLM successfully.")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI LLM: {e}")
    raise

# Initialize the DNAC agent
try:
    dnac_agent = initialize_agent(
        tools=dnac_tools,
        llm=llm,
        agent='zero-shot-react-description',
        prompt=dnac_prompt_template,
        verbose=True
    )
    logger.info("Initialized DNAC agent successfully.")
except Exception as e:
    logger.error(f"Failed to initialize DNAC agent: {e}")
    raise

def dnac_agent_func(input_text: str) -> str:
    """
    Wrapper function to invoke the DNAC agent with the given input text.
    """
    try:
        response = dnac_agent.run(input_text)
        logger.info(f"DNAC agent response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in DNAC agent function: {e}")
        raise

# Define the DNAC tool for the main agent
dnac_tool = Tool(
    name="DNAC Agent",
    func=dnac_agent_func,
    description="Use for Interacting with Cisco DNAC Controller via RESTAPIs"
)

# List of tools for the main agent
main_agent_tools = [dnac_tool]

# Initialize the main agent
try:
    main_agent = initialize_agent(
        tools=main_agent_tools,
        llm=llm,
        agent='zero-shot-react-description',
        verbose=True
    )
    logger.info("Initialized main agent successfully.")
except Exception as e:
    logger.error(f"Failed to initialize main agent: {e}")
    raise

######################
# Streamlit Interface
######################

# Initialize Streamlit
st.title("Cisco Networking Agent")
st.write("Ask your network questions here:")

# Get user input
user_input = st.text_input("Enter your question:")

# Save session state in chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Streamlit button to send the question
if st.button("Send"):
    if user_input:
        # Add user input to conversation history
        st.session_state.conversation.append({"role": "user", "content": user_input})
        logger.info(f"User input: {user_input}")

        # Invoke the main agent with the user input
        try:
            response = main_agent.run(user_input)
            logger.info(f"Main agent response: {response}")

            # Display the question and response
            st.write(f"**Question:** {user_input}")
            st.write(f"**Answer:** {response}")

            # Add response to conversation history
            st.session_state.conversation.append({"role": "agent", "content": response})

            # Update chat history
            st.session_state.chat_history = "\n".join(
                [f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.conversation]
            )
        except Exception as e:
            logger.error(f"An error occurred while processing the user input: {e}")
            st.write(f"An error occurred: {str(e)}")

# Show the entire conversation history
if st.session_state.conversation:
    st.write("## Conversation History")
    for entry in st.session_state.conversation:
        st.write(f"**{entry['role'].capitalize()}:** {entry['content']}")