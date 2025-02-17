import logging
from genie.testbed import load
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_vlan(device, vlan_id, vlan_name):
    try:
        # Enter configuration mode
        device.configure([
            f'vlan {vlan_id}',
            f'name {vlan_name}'
        ])
        logging.info(f"Configured VLAN {vlan_id} with name {vlan_name}")
    except Exception as e:
        logging.error(f"Failed to configure VLAN {vlan_id}: {e}")

def main():
    try:
        # Load the testbed file
        testbed = load('/Users/gtamilse/Downloads/GITHUB/BRKOPS-1726/uc1/demo/testbed.yml')
        logging.info("Testbed loaded successfully")

        # Connect to the device "FE1"
        device = testbed.devices['FE1']
        device.connect(prompt_recovery=True)
        logging.info(f"Connected to {device.name} with prompt_recovery set to True")

        # Configure VLAN
        vlan_id = 1111
        vlan_name = "Test_VLAN"
        configure_vlan(device, vlan_id, vlan_name)

        # Save the configuration
        device.execute('write memory')
        logging.info("Configuration saved")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()