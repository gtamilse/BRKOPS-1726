import logging
from datetime import datetime
from genie.testbed import load

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        # Load the testbed file
        testbed = load('/Users/gtamilse/Downloads/GITHUB/brkops1726v/uc1/testbed.yml')
        logger.info("Testbed loaded successfully")

        # Connect to the device
        device = testbed.devices['FE1']
        device.connect(prompt_recovery=True)
        logger.info("Connected to device FE1 successfully")

        # Run commands and parse the output
        commands = ["show version", "show ip interface brief", "show vlan"]
        outputs = {}

        for command in commands:
            try:
                outputs[command] = device.parse(command)
                logger.debug(f"Output for '{command}': {outputs[command]}")
            except Exception as e:
                logger.error(f"Failed to execute '{command}': {e}")

        # Get current date and time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save output to file
        output_file = f"device_output_{current_time}.txt"
        with open(output_file, 'w') as f:
            for command, output in outputs.items():
                f.write(f"{command} Output:\n")
                f.write(str(output))
                f.write("\n\n")
        logger.info(f"Output saved to {output_file}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Disconnect from the device
        if 'device' in locals() and device.connected:
            device.disconnect()
            logger.info("Disconnected from device FE1 successfully")

if __name__ == "__main__":
    main()
