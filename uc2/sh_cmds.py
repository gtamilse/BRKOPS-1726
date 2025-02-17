from genie.testbed import load
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Load the testbed file
        testbed = load('/Users/gtamilse/Downloads/GITHUB/BRKOPS-1726/uc1/demo/testbed.yml')
        logging.info("Testbed loaded successfully")

        # Log the current time
        logging.info(f"Testbed loaded at {datetime.now()}")

        # Connect to the device "FE1" and set prompt_recovery to True
        device = testbed.devices['FE1']
        device.connect(prompt_recovery=True)
        logging.info(f"Connected to {device.name} with prompt_recovery set to True")

        # Run commands and parse the output
        commands = ["show version", "show version", "show ip interface brief", "show vlan"]
        outputs = {}

        for command in commands:
            try:
                outputs[command] = device.parse(command)
                logging.info(f"Executed command: {command}")
            except Exception as e:
                logging.error(f"Failed to execute command '{command}': {e}")

        # Save the output to a file with the current date
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"command_outputs_{current_date}.txt"

        with open(output_file, 'w') as f:
            for command, output in outputs.items():
                f.write(f"Command: {command}\n")
                f.write(f"Output: {output}\n\n")

        logging.info(f"Command outputs saved to {output_file}")

        #device disconnect
        device.disconnect()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()