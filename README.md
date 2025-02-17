<h1 align="center">BRKOPS-1726: Learn Network Automation with Github Copilot</h1>

---

# Project Overview

## Summary
This project contains three use-case directories (`uc1`, `uc2`, and `uc3`) that demonstrate various network automation tasks using Python scripts and tools.

Refer to the [BRKOPS-1726.pdf](./BRKOPS-1726.pdf) PDF document for session presentation details.

### UC1 Directory
**Objective:**  
The objective of the code in the `uc1` directory is to showcase how to use simple prompts with Github Copilot to create simple scripts. The sh_cmd.py script connects to a network device, execute specific commands, parse the output, and save the results to a file.


### UC2 Directory
**Objective:**  
The objective of the code in the `uc2` directory is to showcase how to create workflows using Github Actions. This example workflow automates the creation of VLANs on a network device, execute precheck and postcheck scripts, and validate the change on the switch.


### UC3 Directory
**Objective:**  
The objective of the code in the `uc3` directory is to create a simple ReAct Agent that can interact with the Cisco Catalyst Center (DNAC) controller using REST APIs. It utilizes OpenAI ChatGPT LLM as the main agent and a simple python based ReAct Agents for Catalyst center, and shows how LLms can perform thought-action-observation reasoning cycles to retrieve information from the Catalyst Center based on user queries.


## Pre-requisites
1. **Python 3.12**: Ensure you have Python 3.12 installed on your system.
2. **Required Libraries**: Install the required libraries for each use-case directory:
    - For `uc1` and `uc2`:
        ```sh
        pip install pyats genie
        ```
    - For `uc3`:
        ```sh
        pip install -r uc3/requirements.txt
        ```
3. **Environment Variables**: Ensure the [.env](http://_vscodecontentref_/15) file in `uc3` is correctly configured with your DNAC credentials and OpenAI API key.
4. **Testbed File**: Ensure the `testbed.yml` file in each directory is correctly configured with the device details and credentials.

## Authors
- Gowtham Tamilselvan
- Praveen Poojary

## Date
Feb 17, 2025
