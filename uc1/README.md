# UC1 Directory

## Objective
The objective of the code in the `uc1` directory is to connect to a network device, execute specific commands, parse the output, and save the results to a file.

## How to Run
1. Ensure you have the necessary pre-requisites installed (see below).
2. Run the `sh_cmds.py` script to connect to the device, execute commands, and save the output to a file:
    ```sh
    python sh_cmds.py
    ```

## Pre-requisites
1. **Python 3.12**: Ensure you have Python 3.12 installed on your system.
2. **Requirements**: Install the Genie and PyATS libraries for network automation:
    ```sh
    pip install pyats genie
    ```
3. **Testbed File**: Ensure the [testbed.yml](./testbed.yml) file is correctly configured with the device details and credentials.
4. **Logging Configuration**: The script uses Python's logging module for debug information.

## Files
- [sh_cmds.py](./sh_cmds.py): Main script to connect to the device, execute commands, parse the output, and save it to a file.
- [testbed.yml](./testbed.yml): Configuration file containing device details and credentials.
- [device_output_20250119_231336.txt](./device_output_20250119_231336.txt): Sample output file generated by the script.
- [prompt.md](./prompt.md): Markdown file with instructions for the script.

## Example Usage
1. Ensure the [testbed.yml](./testbed.yml) file is correctly configured with your device details.
2. Run the [sh_cmds.py](./sh_cmds.py) script:
    ```sh
    python sh_cmds.py
    ```
3. The output will be saved to a file with the current date and time in the filename.

## Logging
The script uses Python's logging module to provide detailed debug information. Logs are printed to the console with timestamps and log levels.

## Notes
- Ensure the device credentials and IP addresses in the [testbed.yml](./testbed.yml) file are correct.
- The script handles connection and command execution errors gracefully, logging any issues encountered.