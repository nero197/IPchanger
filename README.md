IPChanger

IPChanger is a Python tool designed to interface with the Tor network, enabling users to change their IP address for enhanced privacy and anonymity during online activities such as web scraping and browsing. This tool also provides functionality to log VPN changes and fetch geolocation data for IP addresses.
Installation

Before using IPChanger, ensure you have Python 3.x installed on your system. You will also need to have Tor installed and properly configured.

    Clone the repository:

    bash

git clone https://github.com/nero197/IPchanger.git
cd IPChanger

Set up a Python virtual environment (optional but recommended):

bash

python3 -m venv venv
source venv/bin/activate

Install required Python packages:

    pip install -r requirements.txt

    Configure Tor:

    Make sure Tor is installed on your system. For installation instructions, refer to the official Tor documentation.

Configuration
Authentication

To use IPChanger, you must configure the change_ip and terminate functions with your Tor ControlPort password. This is essential for allowing IPChanger to interface with Tor and request IP changes.

There are two recommended methods to authenticate with your ControlPort password:

    Direct Input (Not Recommended): Directly insert your password in the controller.authenticate('your_password') line in both the change_ip and terminate functions. This method is not recommended due to security concerns with storing plain text passwords in scripts.

    External File (More Secure): Store your password in an external file outside of your version control system (e.g., Git) and read it from your script. For example, create a file named .tor_auth and store your password there. Then, modify IPChanger to read the password from this file:

    python

    def authenticate_with_tor(self):
        with open('.tor_auth', 'r') as file:
            password = file.read().strip()
        controller.authenticate(password)

    Replace the controller.authenticate('your_password') line with a call to self.authenticate_with_tor() in both the change_ip and terminate methods.

Use Responsibly

IPChanger utilizes the Tor network, which is a shared resource. Misuse can impact other users. Therefore, it is crucial to use IPChanger responsibly. Avoid excessive requests or any activities that could harm the Tor network and its users.
Usage

To use IPChanger, run:

python ipchanger.py

Ensure you have followed the configuration steps above to set up authentication with your Tor ControlPort.
Contributing

Contributions to IPChanger are welcome. Please ensure you follow best practices for code contributions and respect the privacy and security implications of working with Tor.
License

[License type] - Please specify the license under which this project is released, encouraging open and responsible use.

Remember to replace placeholders (e.g., https://github.com/yourusername/IPChanger.git, your_password, [License type]) with actual values relevant to your project.
