# UC2 Directory

## Objective
Objective: Create a workflow to automate a method of procedure (MOP) for device provisioning

Workflow automation steps:
1. Connect to Cisco switch
2. Collect pre-check commands 
3. Configure new Vlan -> vlan 1111
4. Collect post-check commands
5. Ensure configuration was successful

## How to Run Workflow
1. Ensure you have the necessary pre-requisites installed (see below).
2. Ensure you have setup your runner in github actions
3. Ensure github-ci.yml is configured with the correctly and inside .github/workflows directory
4. Push the changes to the repository to trigger the workflow


## Pre-requisites
1. **Python 3.12**: Ensure you have Python 3.12 installed on your system.
2. **Requirements**: Install the Genie and PyATS libraries for network automation:
    ```sh
    pip install pyats genie
    ```
3. **Testbed File**: Ensure the testbed.yml file is correctly configured with the device details and credentials.
4. **GitHub Actions**: Ensure you have setup your runner in github actions
5. **Github-ci.yml**: Ensure the github-ci.yml is configured with the correct sequence of steps
6. **Logging Configuration**: The scripts use Python's logging module for debug information.

## Files
- [sh_cmds.py](./sh_cmds.py): Script to connect to the device, execute commands, parse the output, and save it to a file.
- [create_vlan.py](/.create_vlan.py): Script to create a VLAN on the device.
- [diff_compare.sh](./diff_compare.sh): Script to compare the outputs before and after VLAN creation.
- [testbed.yml](./testbed.yml): Configuration file containing device details and credentials.
- [github-ci.yml](./github-ci.yml): GitHub Actions configuration file for CI/CD pipeline; needs to be placed in the .github/workflows directory.

## Example Usage for Manual Testing
1. Ensure the [testbed.yml](./testbed.yml) file is correctly configured with your device details.
2. Run the [sh_cmds.py](./sh_cmds.py) script to connect to the device, execute commands, and save the output to a file (PRE):
    ```sh
    python sh_cmds.py
    ```
3. Run the [create_vlan.py](/.create_vlan.py) script to create a VLAN on the device:
    ```sh
    python create_vlan.py
    ```
4. Run the [sh_cmds.py](./sh_cmds.py) script again to capture the output after VLAN creation (POST):
    ```sh
    python sh_cmds.py
    ```
5. Run the [diff_compare.sh](./diff_compare.sh) script to compare the outputs before and after VLAN creation:
    ```sh
    ./diff_compare.sh
    ```

## Logging
The scripts use Python's logging module to provide detailed debug information. Logs are printed to the console with timestamps and log levels.

## Notes
- Ensure the device credentials and IP addresses in the testbed.yml file are correct.
- The scripts handle connection and command execution errors gracefully, logging any issues encountered.